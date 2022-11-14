# simple plugin of Adder for VOs with Rucio

import time
import traceback
import datetime
import uuid

from .AdderPluginBase import AdderPluginBase
from pandaserver.dataservice import ErrorCode
from pandaserver.dataservice import DataServiceUtils
from pandaserver.dataservice.DDM import rucioAPI

from rucio.common.exception import FileConsistencyMismatch,DataIdentifierNotFound,UnsupportedOperation,\
InvalidPath,RSENotFound,InsufficientAccountLimit,RSEProtocolNotSupported,InvalidRSEExpression,\
InvalidObject, RSEFileNameNotSupported


class AdderSimplePlugin(AdderPluginBase):
    
    # constructor
    def __init__(self, job, **params):
        AdderPluginBase.__init__(self, job, params)


    # main
    def execute(self):
        try:
            # loop over all files
            fileMap = {}
            for fileSpec in self.job.Files:
                # ignore inputs
                if fileSpec.type not in ['output', 'log']:
                    continue
                # ignore local
                if fileSpec.destinationSE == 'local':
                    continue
                # collect file attributes
                try:
                    fsize = int(fileSpec.fsize)
                except Exception:
                    fsize = None
                # set GUID if empty
                if not fileSpec.GUID:
                    fileSpec.GUID = str(uuid.uuid4())
                fileAttrs = {'guid': fileSpec.GUID,
                             'lfn': fileSpec.lfn,
                             'size': fsize,
                             'checksum': fileSpec.checksum,
                             'ds': fileSpec.destinationDBlock}
                if self.extraInfo:
                    if 'surl' in self.extraInfo and fileSpec.lfn in self.extraInfo['surl']:
                        fileAttrs['surl'] = self.extraInfo['surl'][fileSpec.lfn]
                    if 'nevents' in self.extraInfo and fileSpec.lfn in self.extraInfo['nevents']:
                        fileAttrs['events'] = self.extraInfo['nevents'][fileSpec.lfn]
                fileMap.setdefault(fileSpec.destinationDBlock, [])
                fileMap[fileSpec.destinationDBlock].append(fileAttrs)
            # register files
            if fileMap:
                dstRSE = self.siteMapper.getSite(self.job.computingSite).ddm_output['default']
                destIdMap = {dstRSE: fileMap}
                nTry = 3
                for iTry in range(nTry):
                    isFatal = False
                    isFailed = False
                    regStart = datetime.datetime.utcnow()
                    try:
                        self.logger.debug('{} {}'.format('registerFilesInDatasets', str(destIdMap)))
                        out = rucioAPI.registerFilesInDataset(destIdMap, {})
                    except (DataIdentifierNotFound,
                            FileConsistencyMismatch,
                            UnsupportedOperation,
                            InvalidPath,
                            InvalidObject,
                            RSENotFound,
                            RSEProtocolNotSupported,
                            InvalidRSEExpression,
                            RSEFileNameNotSupported,
                            KeyError) as e:
                        # fatal errors
                        out = 'failed with {}\n {}'.format(str(e), traceback.format_exc())
                        isFatal = True
                        isFailed = True
                    except Exception as e:
                        # unknown errors
                        isFailed = True
                        out = 'failed with unknown error: {}\n {}'.format(str(e), traceback.format_exc())
                        if 'value too large for column' in out or \
                                'unique constraint (ATLAS_RUCIO.DIDS_GUID_IDX) violate' in out or \
                                'unique constraint (ATLAS_RUCIO.DIDS_PK) violated' in out or \
                                'unique constraint (ATLAS_RUCIO.ARCH_CONTENTS_PK) violated' in out:
                            isFatal = True
                        else:
                            isFatal = False
                    regTime = datetime.datetime.utcnow() - regStart
                    self.logger.debug('took %s.%03d sec' % (regTime.seconds, regTime.microseconds / 1000))

                    # failed
                    if isFailed or isFatal:
                        self.logger.error('%s' % out)
                        if (iTry + 1) == nTry or isFatal:
                            self.job.ddmErrorCode = ErrorCode.EC_Adder
                            # extract important error string
                            extractedErrStr = DataServiceUtils.extractImportantError(out)
                            errMsg = "Could not add files to DDM: "
                            if extractedErrStr == '':
                                self.job.ddmErrorDiag = errMsg + out.split('\n')[-1]
                            else:
                                self.job.ddmErrorDiag = errMsg + extractedErrStr
                            if isFatal:
                                self.result.setFatal()
                            else:
                                self.result.setTemporary()
                            return 1
                        self.logger.error("Try:%s" % iTry)
                        # sleep
                        time.sleep(10)
                    else:
                        self.logger.debug('%s' % str(out))
                        break
            # done
            self.result.setSucceeded()
            self.logger.debug("end plugin")
        except Exception as e:
            errStr = 'failed to execute with {}\n'.format(str(e))
            errStr += traceback.format_exc()
            self.logger.error(errStr)
            self.result.setTemporary()
        # return
        return
