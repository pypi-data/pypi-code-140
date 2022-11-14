#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2004-2014 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V.A. Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
import sys
import os
import numpy
import logging

_logger = logging.getLogger(__name__)


class BufferedFile(object):
    def __init__(self, filename):
        f = open(filename, 'r')
        self.__buffer = f.read()
        f.close()
        self.__buffer = self.__buffer.replace("\r", "\n")
        self.__buffer = self.__buffer.replace("\n\n", "\n")
        self.__buffer = self.__buffer.split("\n")
        self.__currentLine = 0

    def readline(self):
        if self.__currentLine >= len(self.__buffer):
            return ""
        line = self.__buffer[self.__currentLine]
        self.__currentLine += 1
        return line

    def close(self):
        self.__buffer = [""]
        self.__currentLine = 0
        return

class ThermoEMSFileParser(object):
    def __init__(self, filename):
        if not os.path.exists(filename):
            raise IOError("File %s does not exists"  % filename)

        _fileObject = BufferedFile(filename)

        #Only one measurement per file
        header = []
        ddict = {}
        line = _fileObject.readline()
        ok = False
        if filename.lower().endswith(".ems"):
            if line.startswith("#FORMAT") or \
               (("EMSA" in line) and ("Spectral" in line)):
                ok = True
        if not ok:
            raise IOError("This does look as a Thermo EMS file")
        while not line.startswith("#SPECTRUM"):
            splitLine = line.split(":")
            if len(splitLine) == 2:
                ddict[splitLine[0][1:].strip()] = splitLine[1] 
            header.append(line)
            line = _fileObject.readline()
        header.append(line)
        line = _fileObject.readline().strip()
        line = line.replace(','," ")
        splitLine = line.split()
        data = []
        while(len(splitLine)):
            if len(splitLine[0]):
                try:
                    data.append([float(x) for x in splitLine if len(x) > 0])
                except ValueError:
                    break
            else:
                break
            line = _fileObject.readline().strip()
            line = line.replace(','," ")
            splitLine = line.split()
        _fileObject.close()
        data = numpy.array(data, dtype=numpy.float64)
        ddict["data"] = data
        interestingMotors = ["VacPressure",
                             "TubeVoltageSet",
                             "AmbientPressure",
                             "Realtime",
                             "Livetime",
                             "FilterPosition",
                             "TubeCurrentMon",
                             "TubeVoltageMon",
                             "ExposureNum",
                             "TubeCurrentSet"]
        self._motorNames = []
        for key in ddict.keys():
            #print("Key = ", key, "ken = ", len(ddict[key]))
            if key in interestingMotors:
                self._motorNames.append(key)
        self._data = ddict

    def __getitem__(self, item):
        if item >= self.scanno():
            raise IndexError("Only %d scans in file" % self.scanno)
        motorValues = []
        for key in self._motorNames:
            motorValues.append(float(self._data[key][item]))
        return ThermoEMSScan(self._data, item, motorValues=motorValues)

    def scanno(self):
        """
        Gives back the number of scans in the file
        """
        return 1

    def list(self):
        return "1:%d" % self.scanno()

    def select(self, key):
        """
        key is of the from s.o
        scan number, scan order
        """
        n = key.split(".")
        return self.__getitem__(int(n[0])-1)

    def allmotors(self):
        return self._motorNames

class ThermoEMSScan(object):
    def __init__(self, data, number, motorValues=None):
        if motorValues is None:
            motorValues = []
        self._data = data
        self._number = number
        self._motorValues = motorValues
        self._scanHeader = ["#S %d %s" % (number + 1,self._data['TITLE'])]
        if ("DATE" in self._data) and ("TIME" in self._data):
            self._scanHeader.append("#D %s %s" % \
                                    (self._data["DATE"], self._data["TIME"]))
        
        #return the life time, the preset the elapsed?
        # to be safe, I return the LiveTime
        if "LIVETIME  -s" in self._data:
            if "REALTIME  -s"  in self._data:
                self._scanHeader.append("#@CTIME %s %s %s" % (self._data["REALTIME  -s"],
                                         self._data["LIVETIME  -s"],
                                         self._data["LIVETIME  -s"]))
            else:
                self._scanHeader.append("#@CTIME %s %s %s" % (self._data["LIVETIME  -s"],
                                         self._data["LIVETIME  -s"],
                                         self._data["LIVETIME  -s"]))
        if ("CHOFFSET" in self._data)  and ("NPOINTS" in self._data):
            self._scanHeader.append("#@CHANN %d %d %d 1" % (int(float(self._data["NPOINTS"])),
                                                            int(float(self._data["CHOFFSET"])),
                                                            int(float(self._data["NPOINTS"])-1)))
        else:
            self._scanHeader.append("#@CHANN %d 0 %d 1" % (self._data["data"].shape[0],
                                           self._data["data"].shape[0]-1))
        if "OFFSET" in self._data:
            if "XPERCHAN" in self._data:
                self._scanHeader.append("#@CALIB %s %s 0.0" % \
                                        (self._data["OFFSET"],
                                         self._data["XPERCHAN"]))

    def nbmca(self):
        return 1

    def mca(self, number):
        # it gives the last column (some files have three columns)
        # corresponding to channels, counts and (probably) corrected counts
        if number <= 0:
            raise IndexError("Mca numbering starts at 1")
        elif number > self.nbmca():
            raise IndexError("Only %d MCA's" % number)
        return self._data['data'][:, 1]

    def alllabels(self):
        return []

    def allmotorpos(self):
        return self._motorValues

    def command(self):
        return self._data['TITLE']

    def date(self):
        return self._data["DATE"] + " " + self._data["TIME"]

    def fileheader(self):
        return self._scanHeader
        #a = "#S %d %s" % (self._number + 1, self.command()) 
        #return [a]

    def header(self, key):
        _logger.debug("Requested key = %s", key)
        if key in ['S', '#S']:
            return self.fileheader()[0]
        elif key == 'N':
            return []
        elif key == 'L':
            return []
        elif key in ['D', '@CTIME', '@CALIB', '@CHANN']:
            for item in self._scanHeader:
                if item.startswith("#" + key):
                    return [item]
            return []
        elif key == "" or key == " ":
            return self._scanHeader
        else:
            return []

    def order(self):
        return 1

    def number(self):
        return self._number + 1

    def lines(self):
        return 0

def isThermoEMSFile(filename):
    f = open(filename, 'r')
    try:
        line = f.readline()
    except:
        f.close()
        return False
    f.close()
    try:
        if filename.lower().endswith(".ems"):
            if line.startswith("#FORMAT") or \
               (("EMSA" in line) and ("Spectral" in line)):
                return True
    except:
        pass
    return False

def test(filename):
    if isThermoEMSFile(filename):
        sf=ThermoEMSFileParser(filename)
    else:
        print("Not a Thermo EMS File")
    print(sf[0].header('S'))
    print(sf[0].header('D'))
    print(sf[0].alllabels())
    #print(sf[0].allmotorsvalues())
    print(sf[0].nbmca())
    print(sf[0].mca(1))

if __name__ == "__main__":
    test(sys.argv[1])
