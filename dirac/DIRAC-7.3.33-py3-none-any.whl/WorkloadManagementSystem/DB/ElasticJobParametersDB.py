""" Module containing a front-end to the ElasticSearch-based ElasticJobParametersDB.
    This module interacts with one ES index: "ElasticJobParametersDB",
    which is a drop-in replacement for MySQL-based table JobDB.JobParameters.
    While JobDB.JobParameters in MySQL is defined as::

      CREATE TABLE `JobParameters` (
        `JobID` INT(11) UNSIGNED NOT NULL,
        `Name` VARCHAR(100) NOT NULL,
        `Value` BLOB NOT NULL,
        PRIMARY KEY (`JobID`,`Name`),
        FOREIGN KEY (`JobID`) REFERENCES `Jobs`(`JobID`)
      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

    Here we define a mapping as::

      "JobID": {"type": "long"},
      "Name": {"type": "keyword"},
      "Value": {"type": "text"}

    which is an "equivalent" representation.

    The reason for switching to a ES-based JobParameters lies in the extended searching
    capabilities of ES (ES will analyze+index text fields, while MySQL won't do that on BLOB types).
    This results in higher traceability for DIRAC jobs.

    The following class methods are provided for public usage
      - getJobParameters()
      - setJobParameter()
      - deleteJobParameters()
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import six

from elasticsearch.exceptions import NotFoundError, RequestError

__RCSID__ = "$Id$"

from DIRAC import S_OK, S_ERROR, gConfig
from DIRAC.Core.Utilities import Time
from DIRAC.ConfigurationSystem.Client.PathFinder import getDatabaseSection
from DIRAC.ConfigurationSystem.Client.Helpers import CSGlobals
from DIRAC.Core.Base.ElasticDB import ElasticDB

name = "ElasticJobParametersDB"  # (base for) old index name


mapping = {
    "properties": {
        "JobID": {"type": "long"},
        "timestamp": {"type": "date"},
        "CPUNormalizationFactor": {"type": "long"},
        "NormCPUTime(s)": {"type": "long"},
        "Memory(kB)": {"type": "long"},
        "TotalCPUTime(s)": {"type": "long"},
        "MemoryUsed(kb)": {"type": "long"},
        "HostName": {"type": "keyword"},
        "GridCE": {"type": "keyword"},
        "ModelName": {"type": "keyword"},
        "Status": {"type": "keyword"},
        "JobType": {"type": "keyword"},
    }
}


class ElasticJobParametersDB(ElasticDB):
    def __init__(self):
        """Standard Constructor"""

        try:
            section = getDatabaseSection("WorkloadManagement/ElasticJobParametersDB")
            indexPrefix = gConfig.getValue("%s/IndexPrefix" % section, CSGlobals.getSetup()).lower()

            # Connecting to the ES cluster
            super(ElasticJobParametersDB, self).__init__(name, "WorkloadManagement/ElasticJobParametersDB", indexPrefix)
        except Exception as ex:
            self.log.error("Can't connect to ElasticJobParametersDB", repr(ex))
            raise RuntimeError("Can't connect to ElasticJobParametersDB")

        self.oldIndexName = "%s_%s" % (self.getIndexPrefix(), name.lower())
        self.indexName_base = "%s_elasticjobparameters_index" % self.getIndexPrefix()

        self.dslSearch = self._Search(self.oldIndexName)
        self.dslSearch.extra(track_total_hits=True)

    def _indexName(self, jobID):
        """construct the index name

        :param jobID: Job ID
        """
        indexSplit = int(jobID / 1e6)
        return "%s_%sm" % (self.indexName_base, str(indexSplit))

    def _createIndex(self, indexName):
        """Create a new index if needed

        :param indexName: index name
        """
        # Verifying if the index is there, and if not create it
        res = self.existingIndex(indexName)
        if not res["OK"] or not res["Value"]:
            result = self.createIndex(indexName, mapping, period=None)
            if not result["OK"]:
                self.log.error(result["Message"])
                raise RuntimeError(result["Message"])
            self.log.always("Index created:", indexName)

    def getJobParameters(self, jobID, paramList=None):
        """Get Job Parameters defined for jobID.
          Returns a dictionary with the Job Parameters.
          If paramList is empty - all the parameters are returned.

        :param self: self reference
        :param jobID: Job ID
        :param paramList: list of parameters to be returned (also a string is treated)
        :return: dict with all Job Parameter values
        """
        if isinstance(paramList, six.string_types):
            paramList = paramList.replace(" ", "").split(",")
        self.log.debug("JobDB.getParameters: Getting Parameters for job %d" % jobID)
        resultDict = {}
        inNewIndex = self.existsDoc(self._indexName(jobID), jobID)
        inOldIndex = self._isInOldIndex(self.oldIndexName, jobID)
        # Case 1: the parameters are stored in both indices
        if inNewIndex and inOldIndex:
            # First we get the parameters from the old index
            self.log.debug(
                "A document with JobID %d was found in the old index %s and in the new index %s"
                % (jobID, self.oldIndexName, self._indexName(jobID))
            )
            resultDict = self._searchInOldIndex(jobID, paramList)

            # Now we get the parameters from the new index
            res = self.getDoc(self._indexName(jobID), jobID)
            if not res["OK"]:
                self.log.error("Could not retrieve the data from the new index!", res["Message"])
            else:
                for key in res["Value"]:
                    # Add new parameters or overwrite the old ones
                    resultDict[key] = res["Value"][key]

        # Case 2: only in the old index
        elif inOldIndex:
            self.log.debug("A document with JobID %d was found in the old index %s" % (jobID, self.oldIndexName))
            resultDict = self._searchInOldIndex(jobID, paramList)

        # Case 3: only in the new index
        else:
            self.log.debug(
                "The searched parameters with JobID %d exists in the new index %s" % (jobID, self._indexName(jobID))
            )
            res = self.getDoc(self._indexName(jobID), jobID)
            if not res["OK"]:
                return res
            resultDict = res["Value"]
            if paramList:
                for k in list(resultDict):
                    if k not in paramList:
                        resultDict.pop(k)

        return S_OK({jobID: resultDict})

    def setJobParameter(self, jobID, key, value):
        """
        Inserts data into ElasticJobParametersDB index

        :param self: self reference
        :param jobID: Job ID
        :param key: parameter key
        :param value: parameter value
        :returns: S_OK/S_ERROR as result of indexing
        """
        data = {"JobID": jobID, key: value, "timestamp": Time.toEpochMilliSeconds()}

        # The _id in ES can't exceed 512 bytes, this is a ES hard-coded limitation.

        # If a record with this jobID update and add parameter, otherwise create a new record
        if self.existsDoc(self._indexName(jobID), docID=str(jobID)):
            self.log.debug("A document for this job already exists, it will now be updated")
            result = self.updateDoc(index=self._indexName(jobID), docID=str(jobID), body={"doc": data})
        else:
            self.log.debug("No document has this job id, creating a new document for this job")
            self._createIndex(self._indexName(jobID))
            result = self.index(indexName=self._indexName(jobID), body=data, docID=str(jobID))
        if not result["OK"]:
            self.log.error("Couldn't insert or update data", result["Message"])
        return result

    def setJobParameters(self, jobID, parameters):
        """
        Inserts data into ElasticJobParametersDB index using bulk indexing

        :param self: self reference
        :param jobID: Job ID
        :param parameters: list of tuples (name, value) pairs
        :returns: S_OK/S_ERROR as result of indexing
        """
        parametersDict = dict(parameters)
        parametersDict["JobID"] = jobID
        parametersDict["timestamp"] = int(Time.toEpochMilliSeconds())

        if self.existsDoc(self._indexName(jobID), docID=str(jobID)):
            self.log.debug("A document for this job already exists, it will now be updated")
            result = self.updateDoc(index=self._indexName(jobID), docID=str(jobID), body={"doc": parametersDict})
        else:
            self.log.debug("Creating a new document for this job")
            self._createIndex(self._indexName(jobID))
            result = self.index(self._indexName(jobID), body=parametersDict, docID=str(jobID))
        if not result["OK"]:
            self.log.error("Couldn't insert or update data", result["Message"])
        return result

    def deleteJobParameters(self, jobID, paramList=None):
        """Deletes Job Parameters defined for jobID.
          Returns a dictionary with the Job Parameters.
          If paramList is empty - all the parameters for the job are removed

        :param self: self reference
        :param jobID: Job ID
        :param paramList: list of parameters to be returned (also a string is treated)
        :return: S_OK()/S_ERROR()
        """

        if isinstance(paramList, six.string_types):
            paramList = paramList.replace(" ", "").split(",")
        inNewIndex = self.existsDoc(self._indexName(jobID), str(jobID))
        inOldIndex = self._isInOldIndex(self.oldIndexName, jobID)

        # 3 Cases as in GetJobParameters
        if inNewIndex and inOldIndex:
            # Delete first in the old index, then in the new one
            self._deleteInOldIndex(jobID, paramList)
            res = self._deleteInNewIndex(jobID, paramList)
            if not res["OK"]:
                return S_ERROR(res)

        elif inOldIndex:
            self._deleteInOldIndex(jobID, paramList)

        else:
            self.log.debug(
                "The searched parameters with JobID %d exists in the new index %s" % (jobID, self._indexName(jobID))
            )
            res = self._deleteInNewIndex(jobID, paramList)
            if not res["OK"]:
                return S_ERROR(res)

        return S_OK()

    def _isInOldIndex(self, old_index, jobID):
        """Checks if a document with this jobID exists in the old index"""
        query = {
            "query": {
                "bool": {
                    "filter": {  # no scoring
                        "term": {"JobID": jobID}  # term level query, does not pass through the analyzer
                    }
                }
            }
        }
        try:
            # See a document with this jobID is stored in the old index
            self.query(old_index, query)
            return True
        except (RequestError, NotFoundError):
            return False

    def _searchInOldIndex(self, jobID, paramList):
        """Searches for a document with this jobID in the old index"""
        if paramList:
            if isinstance(paramList, six.string_types):
                paramList = paramList.replace(" ", "").split(",")
        else:
            paramList = []

        resultDict = {}

        # the following should be equivalent to
        # {
        #   "query": {
        #     "bool": {
        #       "filter": {  # no scoring
        #         "term": {"JobID": jobID}  # term level query, does not pass through the analyzer
        #       }
        #     }
        #   }
        # }

        s = self.dslSearch.query("bool", filter=self._Q("term", JobID=jobID))

        res = s.scan()

        for hit in res:
            pname = hit.Name
            if paramList and pname not in paramList:
                continue
            resultDict[pname] = hit.Value
        return resultDict

    def _deleteInOldIndex(self, jobID, paramList):
        """Deletes a document with this jobID in the old index"""
        jobFilter = self._Q("term", JobID=jobID)

        if not paramList:
            s = self.dslSearch.query("bool", filter=jobFilter)
            s.delete()
            return S_OK()

        # the following should be equivalent to
        # {
        #   "query": {
        #     "bool": {
        #       "filter": [  # no scoring
        #         {"term": {"JobID": jobID}},  # term level query, does not pass through the analyzer
        #         {"term": {"Name": param}},  # term level query, does not pass through the analyzer
        #       ]
        #     }
        #   }
        # }
        for param in paramList:
            paramFilter = self._Q("term", Name=param)
            combinedFilter = jobFilter & paramFilter

            s = self.dslSearch.query("bool", filter=combinedFilter)
            s.delete()

    def _deleteInNewIndex(self, jobID, paramList):
        """Deletes a document with this jobID in the new index"""
        if not paramList:
            # Deleting the whole record
            self.log.debug("Deleting record of job", jobID)
            result = self.deleteDoc(self._indexName(jobID), docID=str(jobID))
        else:
            # Deleting the specific parameters
            self.log.debug("JobDB.getParameters: Deleting Parameters %s for job %d" % (paramList, jobID))
            for paramName in paramList:
                result = self.updateDoc(
                    index=self._indexName(jobID),
                    docID=str(jobID),
                    body={"script": "ctx._source.remove('" + paramName + "')"},
                )
                self.log.debug("Deleted parameter %s" % paramName)
        if not result["OK"]:
            return S_ERROR(result)
        self.log.debug("Parameters successfully deleted.")
        return S_OK()

    # TODO: Add query by value (e.g. query which values are in a certain pattern)
