##
# File: CyanaMRParserListener.py
# Date: 27-Jan-2022
#
# Updates:
# Generated from CyanaMRParser.g4 by ANTLR 4.11.1
""" ParserLister class for CYANA MR files.
    @author: Masashi Yokochi
"""
import sys
import itertools
import numpy
import re

from antlr4 import ParseTreeListener

try:
    from wwpdb.utils.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from wwpdb.utils.nmr.mr.CyanaMRParser import CyanaMRParser
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (toNpArray,
                                                       checkCoordinates,
                                                       extendCoordinatesForExactNoes,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       isLongRangeRestraint,
                                                       hasIntraChainResraint,
                                                       isCyclicPolymer,
                                                       getRestraintName,
                                                       getValidSubType,
                                                       incListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       getRow,
                                                       ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR,
                                                       RDC_RESTRAINT_RANGE,
                                                       RDC_RESTRAINT_ERROR,
                                                       PCS_RESTRAINT_RANGE,
                                                       PCS_RESTRAINT_ERROR,
                                                       KNOWN_ANGLE_NAMES,
                                                       KNOWN_ANGLE_ATOM_NAMES,
                                                       KNOWN_ANGLE_SEQ_OFFSET,
                                                       KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                                       KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                                       CYANA_MR_FILE_EXTS)
    from wwpdb.utils.nmr.ChemCompUtil import ChemCompUtil
    from wwpdb.utils.nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from wwpdb.utils.nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from wwpdb.utils.nmr.AlignUtil import (MAJOR_ASYM_ID_SET,
                                           monDict3,
                                           updatePolySeqRst,
                                           sortPolySeqRst,
                                           alignPolymerSequence,
                                           assignPolymerSequence,
                                           trimSequenceAlignment,
                                           retrieveAtomIdentFromMRMap,
                                           retrieveAtomIdFromMRMap,
                                           retrieveRemappedSeqId,
                                           splitPolySeqRstForMultimers,
                                           splitPolySeqRstForExactNoes,
                                           retrieveRemappedChainId,
                                           splitPolySeqRstForNonPoly,
                                           retrieveRemappedNonPoly,
                                           splitPolySeqRstForBranch,
                                           retrieveOriginalSeqIdFromMRMap)
except ImportError:
    from nmr.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from nmr.mr.CyanaMRParser import CyanaMRParser
    from nmr.mr.ParserListenerUtil import (toNpArray,
                                           checkCoordinates,
                                           extendCoordinatesForExactNoes,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           isLongRangeRestraint,
                                           hasIntraChainResraint,
                                           isCyclicPolymer,
                                           getRestraintName,
                                           getValidSubType,
                                           incListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           getRow,
                                           ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS,
                                           REPRESENTATIVE_MODEL_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR,
                                           RDC_RESTRAINT_RANGE,
                                           RDC_RESTRAINT_ERROR,
                                           PCS_RESTRAINT_RANGE,
                                           PCS_RESTRAINT_ERROR,
                                           KNOWN_ANGLE_NAMES,
                                           KNOWN_ANGLE_ATOM_NAMES,
                                           KNOWN_ANGLE_SEQ_OFFSET,
                                           KNOWN_ANGLE_CARBO_ATOM_NAMES,
                                           KNOWN_ANGLE_CARBO_SEQ_OFFSET,
                                           CYANA_MR_FILE_EXTS)
    from nmr.ChemCompUtil import ChemCompUtil
    from nmr.BMRBChemShiftStat import BMRBChemShiftStat
    from nmr.NEFTranslator.NEFTranslator import NEFTranslator
    from nmr.AlignUtil import (MAJOR_ASYM_ID_SET,
                               monDict3,
                               updatePolySeqRst,
                               sortPolySeqRst,
                               alignPolymerSequence,
                               assignPolymerSequence,
                               trimSequenceAlignment,
                               retrieveAtomIdentFromMRMap,
                               retrieveAtomIdFromMRMap,
                               retrieveRemappedSeqId,
                               splitPolySeqRstForMultimers,
                               splitPolySeqRstForExactNoes,
                               retrieveRemappedChainId,
                               splitPolySeqRstForNonPoly,
                               retrieveRemappedNonPoly,
                               splitPolySeqRstForBranch,
                               retrieveOriginalSeqIdFromMRMap)


DIST_RANGE_MIN = DIST_RESTRAINT_RANGE['min_inclusive']
DIST_RANGE_MAX = DIST_RESTRAINT_RANGE['max_inclusive']

DIST_ERROR_MIN = DIST_RESTRAINT_ERROR['min_exclusive']
DIST_ERROR_MAX = DIST_RESTRAINT_ERROR['max_exclusive']


ANGLE_RANGE_MIN = ANGLE_RESTRAINT_RANGE['min_inclusive']
ANGLE_RANGE_MAX = ANGLE_RESTRAINT_RANGE['max_inclusive']

ANGLE_ERROR_MIN = ANGLE_RESTRAINT_ERROR['min_exclusive']
ANGLE_ERROR_MAX = ANGLE_RESTRAINT_ERROR['max_exclusive']


RDC_RANGE_MIN = RDC_RESTRAINT_RANGE['min_inclusive']
RDC_RANGE_MAX = RDC_RESTRAINT_RANGE['max_inclusive']

RDC_ERROR_MIN = RDC_RESTRAINT_ERROR['min_exclusive']
RDC_ERROR_MAX = RDC_RESTRAINT_ERROR['max_exclusive']


PCS_RANGE_MIN = PCS_RESTRAINT_RANGE['min_inclusive']
PCS_RANGE_MAX = PCS_RESTRAINT_RANGE['max_inclusive']

PCS_ERROR_MIN = PCS_RESTRAINT_ERROR['min_exclusive']
PCS_ERROR_MAX = PCS_RESTRAINT_ERROR['max_exclusive']


# This class defines a complete listener for a parse tree produced by CyanaMRParser.
class CyanaMRParserListener(ParseTreeListener):

    __verbose = None
    __lfh = None
    __debug = False
    __remediate = False

    __createSfDict = False
    __omitDistLimitOutlier = True
    __allowZeroUpperLimit = False
    __correctCircularShift = True
    __applyPdbStatCap = False

    # atom name mapping of public MR file between the archive coordinates and submitted ones
    __mrAtomNameMapping = None

    # CCD accessing utility
    __ccU = None

    # BMRB chemical shift statistics
    __csStat = None

    # NEFTranslator
    __nefT = None

    # Pairwise align
    __pA = None

    # reasons for re-parsing request from the previous trial
    __reasons = None

    __upl_or_lol = None  # must be one of (None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl')

    __file_ext = None  # must be one of (None, 'upl', 'lol', 'aco', 'rdc', 'pcs', 'upv', 'lov', 'cco')
    __cur_dist_type = ''
    __local_dist_types = []  # list items must be one of ('upl', 'lol')

    # CIF reader
    __cR = None
    __hasCoord = False

    # data item name for model ID in 'atom_site' category
    __modelNumName = None

    # data item names for auth_asym_id, auth_seq_id, auth_atom_id in 'atom_site' category
    __authAsymId = None
    __authSeqId = None
    __authAtomId = None
    # __altAuthAtomId = None

    # coordinates information generated by ParserListenerUtil.checkCoordinates()
    __polySeq = None
    __altPolySeq = None
    __nonPoly = None
    __branch = None
    __nonPolySeq = None
    __coordAtomSite = None
    __coordUnobsRes = None
    __labelToAuthSeq = None
    __authToLabelSeq = None

    __representativeModelId = REPRESENTATIVE_MODEL_ID
    __hasPolySeq = False
    __hasNonPoly = False
    __hasBranch = False
    __hasNonPolySeq = False
    __preferAuthSeq = True
    __gapInAuthSeq = False

    # chain number dictionary
    __chainNumberDict = None

    # polymer sequence of MR file
    __polySeqRst = None

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    __cur_subtype = ''
    __cur_subtype_altered = False
    __cur_comment_inlined = False
    __cur_rdc_orientation = 0

    # column_order of distance restraints with chain
    __col_order_of_dist_w_chain = {}

    # RDC parameter dictionary
    rdcParameterDict = None

    # PCS parameter dictionary
    pcsParameterDict = None

    # collection of atom selection
    atomSelectionSet = []

    # collection of number selection
    numberSelection = []

    # collection of auxiliary atom selection
    auxAtomSelectionSet = ''

    # current residue name for atom name mapping
    __cur_resname_for_mapping = ''

    # unambigous atom name mapping
    unambigAtomNameMapping = {}

    # ambigous atom name mapping
    ambigAtomNameMapping = {}

    # collection of general atom name extended with ambig code
    genAtomNameSelection = []

    warningMessage = ''

    reasonsForReParsing = {}

    # original source MR file name
    __originalFileName = '.'

    # list id counter
    __listIdCounter = {}

    # entry ID
    __entryId = '.'

    # dictionary of pynmrstar saveframes
    sfDict = {}

    def __init__(self, verbose=True, log=sys.stdout,
                 representativeModelId=REPRESENTATIVE_MODEL_ID,
                 mrAtomNameMapping=None,
                 cR=None, cC=None, ccU=None, csStat=None, nefT=None,
                 reasons=None, upl_or_lol=None, file_ext=None):
        self.__verbose = verbose
        self.__lfh = log

        self.__representativeModelId = representativeModelId
        self.__mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.__cR = cR
        self.__hasCoord = cR is not None

        if self.__hasCoord:
            ret = checkCoordinates(verbose, log, representativeModelId, cR, cC)
            self.__modelNumName = ret['model_num_name']
            self.__authAsymId = ret['auth_asym_id']
            self.__authSeqId = ret['auth_seq_id']
            self.__authAtomId = ret['auth_atom_id']
            # self.__altAuthAtomId = ret['alt_auth_atom_id']
            self.__polySeq = ret['polymer_sequence']
            self.__altPolySeq = ret['alt_polymer_sequence']
            self.__nonPoly = ret['non_polymer']
            self.__branch = ret['branch']
            self.__coordAtomSite = ret['coord_atom_site']
            self.__coordUnobsRes = ret['coord_unobs_res']
            self.__labelToAuthSeq = ret['label_to_auth_seq']
            self.__authToLabelSeq = ret['auth_to_label_seq']

        self.__hasPolySeq = self.__polySeq is not None and len(self.__polySeq) > 0
        self.__hasNonPoly = self.__nonPoly is not None and len(self.__nonPoly) > 0
        self.__hasBranch = self.__branch is not None and len(self.__branch) > 0
        if self.__hasNonPoly or self.__hasBranch:
            self.__hasNonPolySeq = True
            if self.__hasNonPoly and self.__hasBranch:
                self.__nonPolySeq = self.__nonPoly
                self.__nonPolySeq.extend(self.__branch)
            elif self.__hasNonPoly:
                self.__nonPolySeq = self.__nonPoly
            else:
                self.__nonPolySeq = self.__branch

        if self.__hasPolySeq:
            self.__gapInAuthSeq = any(ps for ps in self.__polySeq if ps['gap_in_auth_seq'])

        # CCD accessing utility
        self.__ccU = ChemCompUtil(verbose, log) if ccU is None else ccU

        # BMRB chemical shift statistics
        self.__csStat = BMRBChemShiftStat(verbose, log, self.__ccU) if csStat is None else csStat

        # NEFTranslator
        self.__nefT = NEFTranslator(verbose, log, self.__ccU, self.__csStat) if nefT is None else nefT

        # Pairwise align
        if self.__hasPolySeq:
            self.__pA = PairwiseAlign()
            self.__pA.setVerbose(verbose)

        if reasons is not None and 'model_chain_id_ext' in reasons:
            self.__polySeq, self.__altPolySeq, self.__coordAtomSite, self.__coordUnobsRes, self.__labelToAuthSeq, self.__authToLabelSeq =\
                extendCoordinatesForExactNoes(reasons['model_chain_id_ext'],
                                              self.__polySeq, self.__altPolySeq,
                                              self.__coordAtomSite, self.__coordUnobsRes,
                                              self.__labelToAuthSeq, self.__authToLabelSeq)

        # reasons for re-parsing request from the previous trial
        self.__reasons = reasons
        self.__preferLabelSeqCount = 0

        self.reasonsForReParsing = {}  # reset to prevent interference from the previous run

        self.__upl_or_lol = upl_or_lol

        if upl_or_lol not in (None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl'):
            msg = f"The argument 'upl_or_lol' must be one of {(None, 'upl_only', 'upl_w_lol', 'lol_only', 'lol_w_upl')}"
            log.write(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}\n")
            raise ValueError(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")

        self.__file_ext = file_ext

        if file_ext not in CYANA_MR_FILE_EXTS:
            msg = f"The argument 'file_ext' must be one of {CYANA_MR_FILE_EXTS}"
            log.write(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}\n")
            raise ValueError(f"'+CyanaMRParserListener.__init__() ++ ValueError  -  {msg}")

        if upl_or_lol is None and file_ext is not None:

            if file_ext == 'upl':
                self.__upl_or_lol = 'upl_w_lol'

            if file_ext == 'lol':
                self.__upl_or_lol = 'lol_w_upl'

        self.__max_dist_value = DIST_ERROR_MIN
        self.__min_dist_value = DIST_ERROR_MAX

        self.__dihed_lb_greater_than_ub = False
        self.__dihed_ub_always_positive = True

        self.distRestraints = 0      # CYANA: Distance restraint file (.upl or .lol)
        self.dihedRestraints = 0     # CYANA: Torsion angle restraint file (.aco)
        self.rdcRestraints = 0       # CYANA: Residual dipolar coupling restraint file (.rdc)
        self.pcsRestraints = 0       # CYANA: Pseudocontact shift restraint file (.pcs)
        self.noepkRestraints = 0     # CYANA: NOESY volume restraint file (.upv or .lov)
        self.jcoupRestraints = 0     # CYANA: Scalar coupling constant restraint file (.cco)
        self.geoRestraints = 0       # CYANA: Coordinate geometry restraints
        self.hbondRestraints = 0     # CYANA: Hydrogen bond geometry restraints
        self.ssbondRestraints = 0    # CYANA: Disulfide bond geometry restraints
        self.fchiralRestraints = 0   # CYANA: Floating chiral stereo assignments

    def setDebugMode(self, debug):
        self.__debug = debug

    def setRemediateMode(self, remediate):
        self.__remediate = remediate

    def createSfDict(self, createSfDict):
        self.__createSfDict = createSfDict

    def setOriginaFileName(self, originalFileName):
        self.__originalFileName = originalFileName

    def setListIdCounter(self, listIdCounter):
        self.__listIdCounter = listIdCounter

    def setEntryId(self, entryId):
        self.__entryId = entryId

    # Enter a parse tree produced by CyanaMRParser#cyana_mr.
    def enterCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument
        self.__chainNumberDict = {}
        self.__polySeqRst = []

    # Exit a parse tree produced by CyanaMRParser#cyana_mr.
    def exitCyana_mr(self, ctx: CyanaMRParser.Cyana_mrContext):  # pylint: disable=unused-argument
        if self.__hasPolySeq and self.__polySeqRst is not None:
            sortPolySeqRst(self.__polySeqRst,
                           None if self.__reasons is None or 'non_poly_remap' not in self.__reasons else self.__reasons['non_poly_remap'])

            file_type = 'nm-res-cya'

            self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.__polySeq, self.__polySeqRst,
                                                      resolvedMultimer=(self.__reasons is not None))
            self.__chainAssign, message = assignPolymerSequence(self.__pA, self.__ccU, file_type, self.__polySeq, self.__polySeqRst, self.__seqAlign)

            if len(message) > 0:
                self.warningMessage += message

            if self.__chainAssign is not None:

                if len(self.__polySeq) == len(self.__polySeqRst):

                    chain_mapping = {}

                    for ca in self.__chainAssign:
                        ref_chain_id = ca['ref_chain_id']
                        test_chain_id = ca['test_chain_id']

                        if ref_chain_id != test_chain_id:
                            chain_mapping[test_chain_id] = ref_chain_id

                    if len(chain_mapping) == len(self.__polySeq):

                        for ps in self.__polySeqRst:
                            if ps['chain_id'] in chain_mapping:
                                ps['chain_id'] = chain_mapping[ps['chain_id']]

                        self.__seqAlign, _ = alignPolymerSequence(self.__pA, self.__polySeq, self.__polySeqRst,
                                                                  resolvedMultimer=(self.__reasons is not None))
                        self.__chainAssign, _ = assignPolymerSequence(self.__pA, self.__ccU, file_type, self.__polySeq, self.__polySeqRst, self.__seqAlign)

                trimSequenceAlignment(self.__seqAlign, self.__chainAssign)

                if 'Atom not found' in self.warningMessage and self.__reasons is None:

                    seqIdRemap = []

                    cyclicPolymer = {}

                    for ca in self.__chainAssign:
                        ref_chain_id = ca['ref_chain_id']
                        test_chain_id = ca['test_chain_id']

                        sa = next(sa for sa in self.__seqAlign
                                  if sa['ref_chain_id'] == ref_chain_id
                                  and sa['test_chain_id'] == test_chain_id)

                        poly_seq_model = next(ps for ps in self.__polySeq
                                              if ps['auth_chain_id'] == ref_chain_id)
                        poly_seq_rst = next(ps for ps in self.__polySeqRst
                                            if ps['chain_id'] == test_chain_id)

                        seq_id_mapping = {}
                        for ref_seq_id, mid_code, test_seq_id in zip(sa['ref_seq_id'], sa['mid_code'], sa['test_seq_id']):
                            if mid_code == '|':
                                try:
                                    seq_id_mapping[test_seq_id] = next(auth_seq_id for auth_seq_id, seq_id
                                                                       in zip(poly_seq_model['auth_seq_id'], poly_seq_model['seq_id'])
                                                                       if seq_id == ref_seq_id)
                                except StopIteration:
                                    pass

                        if ref_chain_id not in cyclicPolymer:
                            cyclicPolymer[ref_chain_id] =\
                                isCyclicPolymer(self.__cR, self.__polySeq, ref_chain_id, self.__representativeModelId, self.__modelNumName)

                        if cyclicPolymer[ref_chain_id]:

                            poly_seq_model = next(ps for ps in self.__polySeq
                                                  if ps['auth_chain_id'] == ref_chain_id)

                            offset = None
                            for seq_id, comp_id in zip(poly_seq_rst['seq_id'], poly_seq_rst['comp_id']):
                                if seq_id not in seq_id_mapping:
                                    _seq_id = next((_seq_id for _seq_id, _comp_id in zip(poly_seq_model['seq_id'], poly_seq_model['comp_id'])
                                                    if _seq_id not in seq_id_mapping.values() and _comp_id == comp_id), None)
                                    if _seq_id is not None:
                                        offset = seq_id - _seq_id
                                        break

                            if offset is not None:
                                for seq_id in poly_seq_rst['seq_id']:
                                    if seq_id not in seq_id_mapping:
                                        seq_id_mapping[seq_id] = seq_id - offset

                        if any(k for k, v in seq_id_mapping.items() if k != v)\
                           and not any(k for k, v in seq_id_mapping.items()
                                       if v in poly_seq_model['seq_id']
                                       and k == poly_seq_model['auth_seq_id'][poly_seq_model['seq_id'].index(v)]):
                            seqIdRemap.append({'chain_id': test_chain_id, 'seq_id_dict': seq_id_mapping})

                    if len(seqIdRemap) > 0:
                        if 'seq_id_remap' not in self.reasonsForReParsing:
                            self.reasonsForReParsing['seq_id_remap'] = seqIdRemap

                    if any(ps for ps in self.__polySeq if 'identical_chain_id' in ps):
                        polySeqRst, chainIdMapping = splitPolySeqRstForMultimers(self.__pA, self.__polySeq, self.__polySeqRst, self.__chainAssign)

                        if polySeqRst is not None:
                            self.__polySeqRst = polySeqRst
                            if 'chain_id_remap' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['chain_id_remap'] = chainIdMapping

                    if len(self.__polySeq) == 1 and len(self.__polySeqRst) == 1:
                        polySeqRst, chainIdMapping, modelChainIdExt =\
                            splitPolySeqRstForExactNoes(self.__pA, self.__polySeq, self.__polySeqRst, self.__chainAssign)

                        if polySeqRst is not None:
                            self.__polySeqRst = polySeqRst
                            if 'chain_id_clone' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['chain_id_clone'] = chainIdMapping
                            if 'model_chain_id_ext' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['model_chain_id_ext'] = modelChainIdExt

                    if self.__hasNonPoly:
                        polySeqRst, nonPolyMapping = splitPolySeqRstForNonPoly(self.__ccU, self.__nonPoly, self.__polySeqRst,
                                                                               self.__seqAlign, self.__chainAssign)

                        if polySeqRst is not None:
                            self.__polySeqRst = polySeqRst
                            if 'non_poly_remap' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['non_poly_remap'] = nonPolyMapping

                    if self.__hasBranch:
                        polySeqRst, branchMapping = splitPolySeqRstForBranch(self.__pA, self.__polySeq, self.__branch, self.__polySeqRst,
                                                                             self.__chainAssign)

                        if polySeqRst is not None:
                            self.__polySeqRst = polySeqRst
                            if 'branch_remap' not in self.reasonsForReParsing:
                                self.reasonsForReParsing['branch_remap'] = branchMapping

            if 'Atom not found' in self.warningMessage and self.__reasons is None:
                if len(self.unambigAtomNameMapping) > 0:
                    if 'unambig_atom_id_remap' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['unambig_atom_id_remap'] = self.unambigAtomNameMapping
                if len(self.ambigAtomNameMapping) > 0:
                    if 'ambig_atom_id_remap' not in self.reasonsForReParsing:
                        self.reasonsForReParsing['ambig_atom_id_remap'] = self.ambigAtomNameMapping
        # """
        # if 'label_seq_scheme' in self.reasonsForReParsing and self.reasonsForReParsing['label_seq_scheme']:
        #     if 'non_poly_remap' in self.reasonsForReParsing:
        #         self.reasonsForReParsing['label_seq_scheme'] = False
        #     if 'seq_id_remap' in self.reasonsForReParsing:
        #         del self.reasonsForReParsing['seq_id_remap']
        # """
        if 'local_seq_scheme' in self.reasonsForReParsing:
            if 'non_poly_remap' in self.reasonsForReParsing or 'branch_remap' in self.reasonsForReParsing:
                del self.reasonsForReParsing['local_seq_scheme']
            if 'seq_id_remap' in self.reasonsForReParsing:
                del self.reasonsForReParsing['seq_id_remap']

        if 'seq_id_remap' in self.reasonsForReParsing and 'non_poly_remap' in self.reasonsForReParsing:
            del self.reasonsForReParsing['seq_id_remap']

        if len(self.warningMessage) == 0:
            self.warningMessage = None
        else:
            self.warningMessage = self.warningMessage[0:-1]
            self.warningMessage = '\n'.join(set(self.warningMessage.split('\n')))

        if self.__remediate:
            if self.__dihed_lb_greater_than_ub and self.__dihed_ub_always_positive:
                if 'dihed_unusual_order' not in self.reasonsForReParsing:
                    self.reasonsForReParsing['dihed_unusual_order'] = True

    # Enter a parse tree produced by CyanaMRParser#comment.
    def enterComment(self, ctx: CyanaMRParser.CommentContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#comment.
    def exitComment(self, ctx: CyanaMRParser.CommentContext):
        if self.__cur_comment_inlined:
            return

        for col in range(20):
            if ctx.Any_name(col):
                text = str(ctx.Any_name(col)).lower()
                if 'cco' in text or 'coupling' in text:
                    self.__cur_dist_type = 'cco'
                    break
                if ('upl' in text or 'upper' in text) and not ('lol' in text or 'lower' in text):
                    self.__cur_dist_type = 'upl'
                    break
                if ('lol' in text or 'lower' in text) and not ('upl' in text or 'upper' in text):
                    self.__cur_dist_type = 'lol'
                    break
            else:
                break

    # Enter a parse tree produced by CyanaMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext != 'cco' else 'jcoup'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: CyanaMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        elif self.__cur_subtype == 'jcoup':
            self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):

        if self.__cur_subtype == 'dist' and (self.__cur_dist_type == 'cco' or len(self.numberSelection) == 6):
            self.__cur_subtype = 'jcoup'
            self.distRestraints -= 1
            self.jcoupRestraints += 1

        try:

            if None in self.genAtomNameSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = self.genAtomNameSelection[0].upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(1)).upper()
            atomId2 = self.genAtomNameSelection[1].upper()

            if len(compId1) == 1 and len(compId2) == 1 and compId1.isalpha() and compId2.isalpha():
                atom_like = self.__csStat.getAtomLikeNameSet(True, True, 1)
                if atomId1 in atom_like and atomId2 in atom_like:
                    self.exitDistance_wo_comp_restraint(ctx)
                    return

            target_value = None
            lower_limit = None
            upper_limit = None

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            if self.__cur_subtype == 'dist':

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                    if value > self.__max_dist_value:
                        self.__max_dist_value = value
                    if value < self.__min_dist_value:
                        self.__min_dist_value = value

                if has_square:
                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:
                    target_value = value
                    if delta > 0.0:
                        lower_limit = value - delta
                        upper_limit = value + delta

                elif self.__upl_or_lol is None:
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_only':
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.__upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                    self.__local_dist_types.append(self.__cur_dist_type)

                if not self.__hasPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                        isRdc = False

                    if chain_id_1 != chain_id_2:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) == 1:

                        if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')):
                            pass

                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        if not any(b for b in self.__ccU.lastBonds
                                   if ((b[self.__ccU.ccbAtomId1] == atom_id_1 and b[self.__ccU.ccbAtomId2] == atom_id_2)
                                       or (b[self.__ccU.ccbAtomId1] == atom_id_2 and b[self.__ccU.ccbAtomId2] == atom_id_1))):

                            if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                isRdc = False

                    if not isRdc:
                        self.__cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.__cur_subtype_altered = True
                            self.__cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            self.__cur_subtype = 'rdc'
                            self.rdcRestraints += 1
                            self.distRestraints -= 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.__createSfDict:
                                sf = self.__getSf()
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                    continue
                                if self.__debug:
                                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.__createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None,
                                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                                    sf['loop'].add_data(row)

                            self.__cur_subtype = 'dist'

                            return

                self.__allowZeroUpperLimit = False
                if self.__reasons is not None and 'model_chain_id_ext' in self.__reasons\
                   and len(self.atomSelectionSet[0]) > 0\
                   and len(self.atomSelectionSet[0]) == len(self.atomSelectionSet[1]):
                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if chain_id_1 != chain_id_2 and seq_id_1 == seq_id_2 and atom_id_1 == atom_id_2\
                       and ((chain_id_1 in self.__reasons['model_chain_id_ext'] and chain_id_2 in self.__reasons['model_chain_id_ext'][chain_id_1])
                            or (chain_id_2 in self.__reasons['model_chain_id_ext'] and chain_id_1 in self.__reasons['model_chain_id_ext'][chain_id_2])):
                        self.__allowZeroUpperLimit = True

                dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, self.__omitDistLimitOutlier)

                self.__allowZeroUpperLimit = False

                if dstFunc is None:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a Scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Non-magnetic susceptible spin appears in scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "\
                        f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                            f"Found inter-chain scalar coupling constant; "\
                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Found inter-residue scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                        pass

                    else:
                        self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                            "Found inter-residue scalar coupling constant; "\
                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                        return

                elif atom_id_1 == atom_id_2:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        "Found zero scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        couplingCode = '3J' + (atom1['auth_atom_id'] if 'auth_atom_id' in atom1 else atom1['atom_id'])\
                            + (atom2['auth_atom_id'] if 'auth_atom_id' in atom2 else atom2['atom_id'])
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', couplingCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.__cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()
            self.genAtomNameSelection.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_restraint.
    def exitDistance_wo_comp_restraint(self, ctx: CyanaMRParser.Distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            chainId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            chainId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                elif self.__cur_subtype == 'jcoup':
                    self.jcoupRestraints -= 1
                return

            if self.__cur_subtype == 'dist':

                value = self.numberSelection[0]
                weight = 1.0

                delta = None
                has_square = False

                if len(self.numberSelection) > 2:
                    value2 = self.numberSelection[1]
                    weight = self.numberSelection[2]

                    has_square = True

                elif len(self.numberSelection) > 1:
                    value2 = self.numberSelection[1]

                    if value2 <= 1.0 or value2 < value:
                        delta = abs(value2)
                    else:
                        has_square = True

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                    if value > self.__max_dist_value:
                        self.__max_dist_value = value
                    if value < self.__min_dist_value:
                        self.__min_dist_value = value

                if has_square:
                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                elif delta is not None:
                    target_value = value
                    if delta > 0.0:
                        lower_limit = value - delta
                        upper_limit = value + delta

                elif self.__upl_or_lol is None:
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_only':
                    if self.__cur_dist_type == 'upl':
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    elif self.__cur_dist_type == 'lol':
                        lower_limit = value
                    elif value > 1.8:
                        upper_limit = value
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        lower_limit = value

                elif self.__upl_or_lol == 'upl_w_lol':
                    upper_limit = value

                elif self.__upl_or_lol == 'lol_only':
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        upper_limit = 5.5  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # 'lol_w_upl'
                    lower_limit = value

                if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                    self.__local_dist_types.append(self.__cur_dist_type)

                if not self.__hasPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                    isRdc = True

                    chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                    seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                    comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                    atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                    chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                    seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                    comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                    atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                    if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                        isRdc = False

                    if chain_id_1 != chain_id_2:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) > 1:
                        isRdc = False

                    if abs(seq_id_1 - seq_id_2) == 1:

                        if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                                ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                                 or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')):
                            pass

                        else:
                            isRdc = False

                    elif atom_id_1 == atom_id_2:
                        isRdc = False

                    elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                        if not any(b for b in self.__ccU.lastBonds
                                   if ((b[self.__ccU.ccbAtomId1] == atom_id_1 and b[self.__ccU.ccbAtomId2] == atom_id_2)
                                       or (b[self.__ccU.ccbAtomId1] == atom_id_2 and b[self.__ccU.ccbAtomId2] == atom_id_1))):

                            if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                                isRdc = False

                    if not isRdc:
                        self.__cur_subtype_altered = False

                    else:

                        isRdc = False

                        if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                            isRdc = True

                        elif value < 1.0 or value > 6.0:
                            self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                            self.__cur_subtype_altered = True
                            self.__cur_rdc_orientation += 1
                            isRdc = True

                        if isRdc:
                            self.__cur_subtype = 'rdc'
                            self.rdcRestraints += 1
                            self.distRestraints -= 1

                            target_value = value
                            lower_limit = upper_limit = None

                            if len(self.numberSelection) > 2:
                                error = abs(self.numberSelection[1])
                                lower_limit = target_value - error
                                upper_limit = target_value + error

                            dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                            if dstFunc is None:
                                return

                            if self.__createSfDict:
                                sf = self.__getSf()
                                sf['id'] += 1

                            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                                  self.atomSelectionSet[1]):
                                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                    continue
                                if self.__debug:
                                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                                if self.__createSfDict and sf is not None:
                                    sf['index_id'] += 1
                                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                                 '.', None,
                                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                                    sf['loop'].add_data(row)

                            self.__cur_subtype = 'dist'

                            return

                dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, self.__omitDistLimitOutlier)

                if dstFunc is None:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)

            else:  # cco

                target = self.numberSelection[0]
                error = None

                weight = 1.0
                if len(self.numberSelection) > 2:
                    error = abs(self.numberSelection[1])
                    weight = self.numberSelection[2]

                elif len(self.numberSelection) > 1:
                    error = abs(self.numberSelection[1])

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                target_value = target
                lower_limit = target - error if error is not None else None
                upper_limit = target + error if error is not None else None

                dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId1, seqId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequenceWithChainIdWithoutCompId(chainId2, seqId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if not self.areUniqueCoordAtoms('a Scalar coupling'):
                    return

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Non-magnetic susceptible spin appears in scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "\
                        f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                if chain_id_1 != chain_id_2:
                    ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                    ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                    if ps1 is None and ps2 is None:
                        self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                            f"Found inter-chain scalar coupling constant; "\
                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                        return

                elif abs(seq_id_1 - seq_id_2) > 1:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Found inter-residue scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                elif abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')
                             or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                             or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                        pass

                    else:
                        self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                            "Found inter-residue scalar coupling constant; "\
                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                        return

                elif atom_id_1 == atom_id_2:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        "Found zero scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        couplingCode = '3J' + (atom1['auth_atom_id'] if 'auth_atom_id' in atom1 else atom1['atom_id'])\
                            + (atom2['auth_atom_id'] if 'auth_atom_id' in atom2 else atom2['atom_id'])
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', couplingCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            elif self.__cur_subtype == 'jcoup':
                self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateDistanceRange(self, weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier):
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value:.3f}"
            else:
                if target_value <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The target value='{target_value:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    target_value = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The target value='{target_value:.3f}' must be within range {DIST_RESTRAINT_ERROR}.\n"

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.3f}"
            else:
                if lower_limit <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    lower_limit = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.\n"

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit:.3f}"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit:.3f}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    upper_limit = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit:.3f}' must be within range {DIST_RESTRAINT_ERROR}.\n"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.3f}' must be less than the target value '{target_value:.3f}'.\n"

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit:.3f}' must be greater than the target value '{target_value:.3f}'.\n"

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.3f}' must be less than the upper limit value '{upper_limit:.3f}'.\n"

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value:.3f}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        if lower_limit is not None:
            if DIST_RANGE_MIN <= lower_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        if upper_limit is not None:
            if DIST_RANGE_MIN <= upper_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit:.3f}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        return dstFunc

    def validatePeakVolumeRange(self, weight, target_value, lower_limit, upper_limit):
        """ Validate NOESY peak volume value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            dstFunc['target_value'] = f"{target_value}"

        if lower_limit is not None:
            dstFunc['lower_limit'] = f"{lower_limit}"

        if upper_limit is not None:
            dstFunc['upper_limit'] = f"{upper_limit}"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit}' must be less than the target value '{target_value}'.\n"

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit}' must be greater than the target value '{target_value}'.\n"

        if not validRange:
            return None

        return dstFunc

    def getRealChainSeqId(self, ps, seqId, compId=None, isPolySeq=True):
        if compId is not None:
            compId = translateToStdResName(compId)
        # if self.__reasons is not None and 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
        if not self.__preferAuthSeq:
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId)
            if seqKey in self.__labelToAuthSeq:
                _chainId, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _chainId, _seqId
        if seqId in ps['auth_seq_id']:
            if compId is None:
                return ps['auth_chain_id'], seqId
            idx = ps['auth_seq_id'].index(seqId)
            if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
                return ps['auth_chain_id'], seqId
        # if seqId in ps['seq_id']:
        #     idx = ps['seq_id'].index(seqId)
        #     if compId is None:
        #         return ps['auth_chain_id'], ps['auth_seq_id'][idx]
        #     if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
        #         return ps['auth_chain_id'], ps['auth_seq_id'][idx]
        return ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId

    def assignCoordPolymerSequence(self, seqId, compId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = []
        _seqId = seqId

        fixedChainId = None
        fixedSeqId = None

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

        if self.__reasons is not None:
            if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
               and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                return self.atomIdListToChainAssign(self.__reasons['ambig_atom_id_remap'][compId][atomId])
            if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
               and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                atomId = self.__reasons['unambig_atom_id_remap'][compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.__reasons and compId in self.__reasons['non_poly_remap']\
               and seqId in self.__reasons['non_poly_remap'][compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], None, seqId, compId)
            if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
            elif 'seq_id_remap' in self.__reasons:
                fixedChainId, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], None, seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping\
               and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping\
               and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        updatePolySeqRst(self.__polySeqRst, self.__polySeq[0]['chain_id'] if fixedChainId is None else fixedChainId, _seqId, translateToStdResName(compId), compId)

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, compId)
            if self.__reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                origCompId = ps['auth_comp_id'][idx]
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId):
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, True))
                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.append((chainId, seqId, cifCompId, True))
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId):
                    #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                    #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                    # """
            elif 'gap_in_auth_seq' in ps:
                min_auth_seq_id = ps['auth_seq_id'][0]
                max_auth_seq_id = ps['auth_seq_id'][-1]
                if min_auth_seq_id <= seqId <= max_auth_seq_id:
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_auth_seq_id:
                        if _seqId_ in ps['auth_seq_id']:
                            break
                        _seqId_ += 1
                    if _seqId_ not in ps['auth_seq_id']:
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_auth_seq_id:
                            if _seqId_ in ps['auth_seq_id']:
                                break
                            _seqId_ -= 1
                    if _seqId_ in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((chainId, seqId_, cifCompId, True))
                                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, compId, False)
                if self.__reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                        _, _, atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                    if 'alt_auth_seq_id' in np and seqId in np['auth_seq_id'] and seqId not in np['alt_auth_seq_id']:
                        seqId = next(_altSeqId for _seqId, _altSeqId in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _seqId == seqId)
                    if compId in (cifCompId, origCompId):
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((chainId, seqId, cifCompId, False))
                    elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId):
                            #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                            #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                            # """

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None and fixedChainId != chainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))
                                    # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                    #     self.reasonsForReParsing['label_seq_scheme'] = True
                            elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    chainAssign.append((chainId, _seqId, cifCompId, True))
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId):
                    #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                    #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                    # """

        if len(chainAssign) == 0:
            if seqId == 1 and atomId in ('H', 'HN'):
                return self.assignCoordPolymerSequence(seqId, compId, 'H1')
            if seqId < 1 and len(self.__polySeq) == 1:
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{compId}:{atomId} is not present in the coordinates. "\
                    f"The residue number '{_seqId}' is not present in polymer sequence of chain {self.__polySeq[0]['chain_id']} of the coordinates. "\
                    "Please update the sequence in the Macromolecules page.\n"
            else:
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{compId}:{atomId} is not present in the coordinates.\n"

        return chainAssign

    def assignCoordPolymerSequenceWithChainId(self, refChainId, seqId, compId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = []
        _seqId = seqId

        fixedChainId = None
        fixedSeqId = None

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

        if self.__reasons is not None:
            if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
               and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                return self.atomIdListToChainAssign(self.__reasons['ambig_atom_id_remap'][compId][atomId])
            if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
               and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                atomId = self.__reasons['unambig_atom_id_remap'][compId][atomId][0]  # select representative one
            if 'non_poly_remap' in self.__reasons and compId in self.__reasons['non_poly_remap']\
               and seqId in self.__reasons['non_poly_remap'][compId]:
                fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], str(refChainId), seqId, compId)
                refChainId = fixedChainId
            if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
                refChainId = fixedChainId
            if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                refChainId = fixedChainId
            elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                refChainId = fixedChainId
            elif 'seq_id_remap' in self.__reasons:
                _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], str(refChainId), seqId)
            if fixedSeqId is not None:
                _seqId = fixedSeqId

        if len(self.ambigAtomNameMapping) > 0:
            if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                return self.atomIdListToChainAssign(self.ambigAtomNameMapping[compId][atomId])
        if len(self.unambigAtomNameMapping) > 0:
            if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                atomId = self.unambigAtomNameMapping[compId][atomId][0]  # select representative one

        updatePolySeqRst(self.__polySeqRst, str(refChainId), _seqId, translateToStdResName(compId), compId)

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, compId)
            if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                if chainId != self.__chainNumberDict[refChainId]:
                    continue
            if self.__reasons is not None:
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    seqId = fixedSeqId
                elif fixedSeqId is not None:
                    seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                origCompId = ps['auth_comp_id'][idx]
                if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                    _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                    atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                if compId in (cifCompId, origCompId):
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, True))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId
                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.append((chainId, seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId):
                    #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                    #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                    # """
            elif 'gap_in_auth_seq' in ps:
                min_auth_seq_id = ps['auth_seq_id'][0]
                max_auth_seq_id = ps['auth_seq_id'][-1]
                if min_auth_seq_id <= seqId <= max_auth_seq_id:
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_auth_seq_id:
                        if _seqId_ in ps['auth_seq_id']:
                            break
                        _seqId_ += 1
                    if _seqId_ not in ps['auth_seq_id']:
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_auth_seq_id:
                            if _seqId_ in ps['auth_seq_id']:
                                break
                            _seqId_ -= 1
                    if _seqId_ in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            origCompId = ps['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId_, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((chainId, seqId_, cifCompId, True))
                                elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, compId, False)
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if self.__reasons is not None:
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                        seqId = fixedSeqId
                    elif fixedSeqId is not None:
                        seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    origCompId = np['auth_comp_id'][idx]
                    if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                        _, coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, self.__hasCoord)
                        atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                    if 'alt_auth_seq_id' in np and seqId in np['auth_seq_id'] and seqId not in np['alt_auth_seq_id']:
                        seqId = next(_altSeqId for _seqId, _altSeqId in zip(np['auth_seq_id'], np['alt_auth_seq_id']) if _seqId == seqId)
                    if compId in (cifCompId, origCompId):
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((chainId, seqId, cifCompId, False))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                    elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, False))
                        if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                            self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        idx = ps['seq_id'].index(seqId)
                        cifCompId = ps['comp_id'][idx]
                        origCompId = ps['auth_comp_id'][idx]
                        if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                            _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                            atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                        if compId in (cifCompId, origCompId):
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True
                        elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                            if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                self.__chainNumberDict[refChainId] = chainId
                            # """ defer to sequence alignment error
                            # if cifCompId != translateToStdResName(compId):
                            #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                            #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                            # """

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                        if chainId != self.__chainNumberDict[refChainId]:
                            continue
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            idx = np['seq_id'].index(seqId)
                            cifCompId = np['comp_id'][idx]
                            origCompId = np['auth_comp_id'][idx]
                            if self.__mrAtomNameMapping is not None and origCompId not in monDict3:
                                _, coordAtomSite = self.getCoordAtomSiteOf(chainId, _seqId, self.__hasCoord)
                                atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, origCompId, atomId, coordAtomSite)
                            if compId in (cifCompId, origCompId):
                                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                    chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                                    # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                    #     self.reasonsForReParsing['label_seq_scheme'] = True
                            elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is None and refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                    _seqId = fixedSeqId
                elif fixedSeqId is not None:
                    _seqId = fixedSeqId
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    chainAssign.append((chainId, _seqId, cifCompId, True))
                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                        self.__chainNumberDict[refChainId] = chainId
                    # """ defer to sequence alignment error
                    # if cifCompId != translateToStdResName(compId):
                    #     self.warningMessage += f"[Unmatched residue name] {self.__getCurrentRestraint()}"\
                    #         f"The residue name {_seqId}:{compId} is unmatched with the name of the coordinates, {cifCompId}.\n"
                    # """

        if len(chainAssign) == 0:
            if seqId == 1 and atomId in ('H', 'HN'):
                return self.assignCoordPolymerSequenceWithChainId(refChainId, seqId, compId, 'H1')
            if compId == 'AMB' and (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{compId}:{atomId} is not present in the coordinates. "\
                    "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.\n"
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{_seqId}:{compId}:{atomId} is not present in the coordinates. "\
                        f"The residue number '{_seqId}' is not present in polymer sequence of chain {refChainId} of the coordinates. "\
                        "Please update the sequence in the Macromolecules page.\n"
                else:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{_seqId}:{compId}:{atomId} is not present in the coordinates.\n"

        return chainAssign

    def assignCoordPolymerSequenceWithoutCompId(self, seqId, atomId=None):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = []
        _seqId = seqId

        fixedChainId = None
        fixedSeqId = None

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, None)
            if self.__reasons is not None:
                if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
                    if fixedChainId != chainId:
                        continue
                if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                    if fixedChainId != chainId:
                        continue
                elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                    if fixedChainId != chainId:
                        continue
                elif 'seq_id_remap' in self.__reasons:
                    _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                if fixedSeqId is not None:
                    seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                if self.__reasons is not None:
                    if 'non_poly_remap' in self.__reasons and cifCompId in self.__reasons['non_poly_remap']\
                       and seqId in self.__reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if fixedChainId != chainId or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.append((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps:
                min_auth_seq_id = ps['auth_seq_id'][0]
                max_auth_seq_id = ps['auth_seq_id'][-1]
                if min_auth_seq_id <= seqId <= max_auth_seq_id:
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_auth_seq_id:
                        if _seqId_ in ps['auth_seq_id']:
                            break
                        _seqId_ += 1
                    if _seqId_ not in ps['auth_seq_id']:
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_auth_seq_id:
                            if _seqId_ in ps['auth_seq_id']:
                                break
                            _seqId_ -= 1
                    if _seqId_ in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                            if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, None, False)
                if self.__reasons is not None:
                    if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
                        if fixedChainId != chainId:
                            continue
                    if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                        if fixedChainId != chainId:
                            continue
                    elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                        if fixedChainId != chainId:
                            continue
                    elif 'seq_id_remap' in self.__reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                    if fixedSeqId is not None:
                        seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                        if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if fixedChainId is not None:
                        if fixedChainId != chainId:
                            continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                            if atomId is None or len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if fixedChainId is not None:
                    if fixedChainId != chainId:
                        continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, chainId, _seqId, cifCompId)
                    chainAssign.append((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0:
            if seqId == 1 and atomId is not None and atomId in ('H', 'HN'):
                return self.assignCoordPolymerSequenceWithoutCompId(seqId, 'H1')
            if atomId is not None and (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{atomId} is not present in the coordinates. "\
                    "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.\n"
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{_seqId}:{atomId} is not present in the coordinates. "\
                        f"The residue number '{_seqId}' is not present in polymer sequence of chain {self.__polySeq[0]['chain_id']} of the coordinates. "\
                        "Please update the sequence in the Macromolecules page.\n"
                else:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{_seqId}:{atomId} is not present in the coordinates.\n"

        return chainAssign

    def assignCoordPolymerSequenceWithChainIdWithoutCompId(self, fixedChainId, seqId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = []
        _seqId = seqId

        fixedSeqId = None

        for ps in self.__polySeq:
            chainId, seqId = self.getRealChainSeqId(ps, _seqId, None)
            if chainId != fixedChainId:
                continue
            if self.__reasons is not None:
                if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
                    if fixedChainId != chainId:
                        continue
                if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                    if fixedChainId != chainId:
                        continue
                elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                    fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                    if fixedChainId != chainId:
                        continue
                elif 'seq_id_remap' in self.__reasons:
                    _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                if fixedSeqId is not None:
                    seqId = _seqId = fixedSeqId
            if seqId in ps['auth_seq_id']:
                idx = ps['auth_seq_id'].index(seqId)
                cifCompId = ps['comp_id'][idx]
                if self.__reasons is not None:
                    if 'non_poly_remap' in self.__reasons and cifCompId in self.__reasons['non_poly_remap']\
                       and seqId in self.__reasons['non_poly_remap'][cifCompId]:
                        fixedChainId, fixedSeqId = retrieveRemappedNonPoly(self.__reasons['non_poly_remap'], chainId, seqId, cifCompId)
                        if fixedSeqId is not None:
                            seqId = _seqId = fixedSeqId
                        if fixedChainId != chainId or seqId not in ps['auth_seq_id']:
                            continue
                updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                    chainAssign.append((chainId, seqId, cifCompId, True))
            elif 'gap_in_auth_seq' in ps:
                min_auth_seq_id = ps['auth_seq_id'][0]
                max_auth_seq_id = ps['auth_seq_id'][-1]
                if min_auth_seq_id <= seqId <= max_auth_seq_id:
                    _seqId_ = seqId + 1
                    while _seqId_ <= max_auth_seq_id:
                        if _seqId_ in ps['auth_seq_id']:
                            break
                        _seqId_ += 1
                    if _seqId_ not in ps['auth_seq_id']:
                        _seqId_ = seqId - 1
                        while _seqId_ >= min_auth_seq_id:
                            if _seqId_ in ps['auth_seq_id']:
                                break
                            _seqId_ -= 1
                    if _seqId_ in ps['auth_seq_id']:
                        idx = ps['auth_seq_id'].index(_seqId_) - (_seqId_ - seqId)
                        try:
                            seqId_ = ps['auth_seq_id'][idx]
                            cifCompId = ps['comp_id'][idx]
                            updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((chainId, seqId_, cifCompId, True))
                        except IndexError:
                            pass

        if self.__hasNonPolySeq:
            for np in self.__nonPolySeq:
                chainId, seqId = self.getRealChainSeqId(np, _seqId, None, False)
                if chainId != fixedChainId:
                    continue
                if self.__reasons is not None:
                    if 'branch_remap' in self.__reasons and seqId in self.__reasons['branch_remap']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['branch_remap'], seqId)
                        if fixedChainId != chainId:
                            continue
                    if 'chain_id_remap' in self.__reasons and seqId in self.__reasons['chain_id_remap']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_remap'], seqId)
                        if fixedChainId != chainId:
                            continue
                    elif 'chain_id_clone' in self.__reasons and seqId in self.__reasons['chain_id_clone']:
                        fixedChainId, fixedSeqId = retrieveRemappedChainId(self.__reasons['chain_id_clone'], seqId)
                        if fixedChainId != chainId:
                            continue
                    elif 'seq_id_remap' in self.__reasons:
                        _, fixedSeqId = retrieveRemappedSeqId(self.__reasons['seq_id_remap'], chainId, seqId)
                    if fixedSeqId is not None:
                        seqId = _seqId = fixedSeqId
                if seqId in np['auth_seq_id']:
                    idx = np['auth_seq_id'].index(seqId)
                    cifCompId = np['comp_id'][idx]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                        chainAssign.append((chainId, seqId, cifCompId, False))

        if len(chainAssign) == 0:
            for ps in self.__polySeq:
                chainId = ps['chain_id']
                if chainId != fixedChainId:
                    continue
                seqKey = (chainId, _seqId)
                if seqKey in self.__authToLabelSeq:
                    _, seqId = self.__authToLabelSeq[seqKey]
                    if seqId in ps['seq_id']:
                        cifCompId = ps['comp_id'][ps['seq_id'].index(seqId)]
                        updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                        if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                            chainAssign.append((ps['auth_chain_id'], _seqId, cifCompId, True))
                            # if 'label_seq_scheme' not in self.reasonsForReParsing:
                            #     self.reasonsForReParsing['label_seq_scheme'] = True

            if self.__hasNonPolySeq:
                for np in self.__nonPolySeq:
                    chainId = np['auth_chain_id']
                    if chainId != fixedChainId:
                        continue
                    seqKey = (chainId, _seqId)
                    if seqKey in self.__authToLabelSeq:
                        _, seqId = self.__authToLabelSeq[seqKey]
                        if seqId in np['seq_id']:
                            cifCompId = np['comp_id'][np['seq_id'].index(seqId)]
                            updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                            if len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((np['auth_chain_id'], _seqId, cifCompId, False))
                                # if 'label_seq_scheme' not in self.reasonsForReParsing:
                                #     self.reasonsForReParsing['label_seq_scheme'] = True

        if len(chainAssign) == 0 and self.__altPolySeq is not None:
            for ps in self.__altPolySeq:
                chainId = ps['auth_chain_id']
                if chainId != fixedChainId:
                    continue
                if _seqId in ps['auth_seq_id']:
                    cifCompId = ps['comp_id'][ps['auth_seq_id'].index(_seqId)]
                    updatePolySeqRst(self.__polySeqRst, fixedChainId, _seqId, cifCompId)
                    chainAssign.append((chainId, _seqId, cifCompId, True))

        if len(chainAssign) == 0:
            if seqId == 1 and atomId in ('H', 'HN'):
                return self.assignCoordPolymerSequenceWithChainIdWithoutCompId(fixedChainId, seqId, 'H1')
            if (('-' in atomId and ':' in atomId) or '.' in atomId):
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates. "\
                    "Please attach ambiguous atom name mapping information generated by 'makeDIST_RST' to the CYANA restraint file.\n"
            else:
                if seqId < 1 and len(self.__polySeq) == 1:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates. "\
                        f"The residue number '{_seqId}' is not present in polymer sequence of chain {fixedChainId} of the coordinates. "\
                        "Please update the sequence in the Macromolecules page.\n"
                else:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{fixedChainId}:{_seqId}:{atomId} is not present in the coordinates.\n"

        return chainAssign

    def selectCoordAtoms(self, chainAssign, seqId, compId, atomId, allowAmbig=True, enableWarning=True):
        """ Select atoms of the coordinates.
        """

        atomSelection = []

        authAtomId = atomId

        _atomId = atomId

        if compId is not None:

            if self.__mrAtomNameMapping is not None and compId not in monDict3:
                _atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

            if self.__reasons is not None:
                if 'ambig_atom_id_remap' in self.__reasons and compId in self.__reasons['ambig_atom_id_remap']\
                   and atomId in self.__reasons['ambig_atom_id_remap'][compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.__reasons['ambig_atom_id_remap'][compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
                if 'unambig_atom_id_remap' in self.__reasons and compId in self.__reasons['unambig_atom_id_remap']\
                   and atomId in self.__reasons['unambig_atom_id_remap'][compId]:
                    atomIds = self.__reasons['unambig_atom_id_remap'][compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                        atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

            if len(self.ambigAtomNameMapping) > 0:
                if compId in self.ambigAtomNameMapping and atomId in self.ambigAtomNameMapping[compId]:
                    atomSelection = self.atomIdListToAtomSelection(self.ambigAtomNameMapping[compId][atomId])
                    for atom in atomSelection:
                        chainId = atom['chain_id']
                        cifSeqId = atom['seq_id']
                        cifCompId = atom['comp_id']
                        cifAtomId = atom['atom_id']
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return
            if len(self.unambigAtomNameMapping) > 0:
                if compId in self.unambigAtomNameMapping and atomId in self.unambigAtomNameMapping[compId]:
                    atomIds = self.unambigAtomNameMapping[compId][atomId]
                    for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:
                        seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                        for cifAtomId in atomIds:
                            self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)
                        atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId, 'atom_id': cifAtomId})
                    if len(atomSelection) > 0:
                        self.atomSelectionSet.append(atomSelection)
                    return

        for chainId, cifSeqId, cifCompId, isPolySeq in chainAssign:

            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
            if self.__mrAtomNameMapping is not None and cifCompId not in monDict3:
                _atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, cifSeqId, cifCompId, atomId, coordAtomSite)
                if atomId != _atomId and coordAtomSite is not None and _atomId in coordAtomSite['atom_id']:
                    atomId = _atomId
                elif self.__reasons is not None and 'branch_remap' in self.__reasons:
                    _seqId = retrieveOriginalSeqIdFromMRMap(self.__reasons['branch_remap'], chainId, cifSeqId)
                    if _seqId != cifSeqId:
                        _, _, atomId = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, _seqId, cifCompId, atomId, coordAtomSite)

            _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomId, leave_unmatched=True)
            if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomId[:-1], leave_unmatched=True)

            if details is not None:
                _atomId_ = translateToStdAtomName(atomId, cifCompId, ccU=self.__ccU)
                if _atomId_ != atomId:
                    __atomId = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]
                    if coordAtomSite is not None and any(_atomId_ for _atomId_ in __atomId if _atomId_ in coordAtomSite['atom_id']):
                        _atomId = __atomId
            # _atomId = self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]

            if coordAtomSite is not None\
               and not any(_atomId_ for _atomId_ in _atomId if _atomId_ in coordAtomSite['atom_id'])\
               and atomId in coordAtomSite['atom_id']:
                _atomId = [atomId]

            if coordAtomSite is None and not isPolySeq and self.__hasNonPolySeq:
                try:
                    for np in self.__nonPolySeq:
                        if np['auth_chain_id'] == chainId and cifSeqId in np['auth_seq_id']:
                            cifSeqId = np['seq_id'][np['auth_seq_id'].index(cifSeqId)]
                            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
                            if coordAtomSite is not None:
                                break
                except ValueError:
                    pass

            lenAtomId = len(_atomId)
            if lenAtomId == 0:
                if enableWarning:
                    self.warningMessage += f"[Invalid atom nomenclature] {self.__getCurrentRestraint()}"\
                        f"{seqId}:{compId}:{atomId} is invalid atom nomenclature.\n"
                continue
            if lenAtomId > 1 and not allowAmbig:
                if enableWarning:
                    self.warningMessage += f"[Invalid atom selection] {self.__getCurrentRestraint()}"\
                        f"Ambiguous atom selection '{seqId}:{compId}:{atomId}' is not allowed as a angle restraint.\n"
                continue

            for cifAtomId in _atomId:
                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                                      'atom_id': cifAtomId, 'auth_atom_id': authAtomId})

                self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite, enableWarning)

        if len(atomSelection) > 0:
            self.atomSelectionSet.append(atomSelection)

    def testCoordAtomIdConsistency(self, chainId, seqId, compId, atomId, seqKey, coordAtomSite, enableWarning=True):
        if not self.__hasCoord:
            return

        found = False

        if coordAtomSite is not None:
            if atomId in coordAtomSite['atom_id']:
                found = True
            elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
                found = True
                self.__authAtomId = 'auth_atom_id'

            elif self.__preferAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.__authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        self.__authSeqId = 'label_seq_id'
                        self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()

            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__authSeqId = 'auth_seq_id'
                        self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    else:
                        self.__preferAuthSeq = False
                else:
                    self.__preferAuthSeq = False

        elif self.__preferAuthSeq:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        else:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = False
            else:
                self.__preferAuthSeq = False

        if found:
            return

        if self.__preferAuthSeq:
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    self.__authSeqId = 'label_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        else:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__authSeqId = 'auth_seq_id'
                    self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = False
            else:
                self.__preferAuthSeq = False

        if found:
            return

        if self.__ccU.updateChemCompDict(compId):
            cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
            if cca is not None and seqKey not in self.__coordUnobsRes and self.__ccU.lastChemCompDict['_chem_comp.pdbx_release_status'] == 'REL':
                if seqId == 1 and atomId in ('H', 'HN'):
                    self.testCoordAtomIdConsistency(chainId, seqId, compId, 'H1', seqKey, coordAtomSite)
                    return
                if atomId[0] == 'H':
                    ccb = next((ccb for ccb in self.__ccU.lastBonds
                                if atomId in (ccb[self.__ccU.ccbAtomId1], ccb[self.__ccU.ccbAtomId2])), None)
                    if ccb is not None:
                        bondedTo = ccb[self.__ccU.ccbAtomId2] if ccb[self.__ccU.ccbAtomId1] == atomId else ccb[self.__ccU.ccbAtomId1]
                        if coordAtomSite is not None and bondedTo in coordAtomSite['atom_id'] and cca[self.__ccU.ccaLeavingAtomFlag] != 'Y':
                            self.warningMessage += f"[Hydrogen not instantiated] {self.__getCurrentRestraint()}"\
                                f"{chainId}:{seqId}:{compId}:{atomId} is not properly instantiated in the coordinates. "\
                                "Please re-upload the model file.\n"
                            return
                if enableWarning:
                    if chainId in MAJOR_ASYM_ID_SET:
                        self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                            f"{chainId}:{seqId}:{compId}:{atomId} is not present in the coordinates.\n"

    def getCoordAtomSiteOf(self, chainId, seqId, cifCheck=True, asis=True):
        seqKey = (chainId, seqId)
        coordAtomSite = None
        if cifCheck:
            preferAuthSeq = self.__preferAuthSeq if asis else not self.__preferAuthSeq
            if preferAuthSeq:
                if seqKey in self.__coordAtomSite:
                    coordAtomSite = self.__coordAtomSite[seqKey]
            else:
                if seqKey in self.__labelToAuthSeq:
                    seqKey = self.__labelToAuthSeq[seqKey]
                    if seqKey in self.__coordAtomSite:
                        coordAtomSite = self.__coordAtomSite[seqKey]
        return seqKey, coordAtomSite

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def enterTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraints.
    def exitTorsion_angle_restraints(self, ctx: CyanaMRParser.Torsion_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def enterTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_restraint.
    def exitTorsion_angle_restraint(self, ctx: CyanaMRParser.Torsion_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            compId = str(ctx.Simple_name(0)).upper()
            if self.__cur_subtype_altered:  # invoked from exitCco_restraint()
                seqId = int(str(ctx.Integer()))
                chainId = str(ctx.Simple_name(1)).upper()
                angleName = str(ctx.Simple_name(2)).upper()
            else:
                seqId = int(str(ctx.Integer(0)))
                angleName = str(ctx.Simple_name(1)).upper()

            if None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.__remediate and self.__reasons is not None and 'dihed_unusual_order' in self.__reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"
            """
            if lower_limit > upper_limit:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.\n"
                if self.__remediate:
                    self.__dihed_lb_greater_than_ub = True
                return
            """
            if self.__remediate and upper_limit < 0.0:
                self.__dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                        f"The angle identifier {str(ctx.Simple_name(1))!r} is unknown for the residue {compId!r}, "\
                        "of which CYANA residue library should be uploaded.\n"
                    return

            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign = self.assignCoordPolymerSequence(seqId, compId, 'CA')
                if len(chainAssign) > 0:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainAssign[0][0])
                    if 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                            if atomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId}:{compId} is not present in the coordinates.\n"
                                return

                self.__retrieveLocalSeqScheme()

                if self.__cur_subtype_altered:  # invoked from exitCco_restraint()
                    chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)
                else:
                    chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{seqId}:{compId} is not present in the coordinates.\n"
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                            f"The angle identifier {str(ctx.Simple_name(1))!r} is unknown for the residue {compId!r}, "\
                            "of which CYANA residue library should be uploaded.\n"
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.__ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    atomSelection = []

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection.clear()

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.warningMessage += f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"\
                                    f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "\
                                    "Please update the sequence in the Macromolecules page.\n"
                                _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
                            else:
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)

                            if cifAtomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.\n"
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf()
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', angleName,
                                         sf['list_id'], self.__entryId, dstFunc, atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId]))

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{seqId}:{compId} is not present in the coordinates.\n"
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                            f"The angle identifier {str(ctx.Simple_name(1))!r} did not match with residue {compId!r}.\n"
                        return

                    atomSelection = []

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection.clear()

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.warningMessage += f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"\
                                    f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "\
                                    "Please update the sequence in the Macromolecules page.\n"
                                _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.\n"
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf()
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', angleName,
                                         sf['list_id'], self.__entryId, dstFunc, None, None, None, None, atom5)
                            sf['loop'].add_data(row)

        except ValueError:
            self.dihedRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateAngleRange(self, weight, target_value, lower_limit, upper_limit):
        """ Validate angle value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if self.__correctCircularShift:
            _array = numpy.array([target_value, lower_limit, upper_limit],
                                 dtype=float)

            shift = None
            if numpy.nanmin(_array) >= THRESHHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmax(_array) // 360) * 360
            elif numpy.nanmax(_array) <= -THRESHHOLD_FOR_CIRCULAR_SHIFT:
                shift = -(numpy.nanmin(_array) // 360) * 360
            if shift is not None:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    "The target/limit values for an angle restraint have been circularly shifted "\
                    f"to fit within range {ANGLE_RESTRAINT_ERROR}.\n"
                if target_value is not None:
                    target_value += shift
                if lower_limit is not None:
                    lower_limit += shift
                if upper_limit is not None:
                    upper_limit += shift

        if target_value is not None:
            if ANGLE_ERROR_MIN < target_value < ANGLE_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value:.3f}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value:.3f}' must be within range {ANGLE_RESTRAINT_ERROR}.\n"

        if lower_limit is not None:
            if ANGLE_ERROR_MIN <= lower_limit < ANGLE_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.\n"

        if upper_limit is not None:
            if ANGLE_ERROR_MIN < upper_limit <= ANGLE_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit}' must be within range {ANGLE_RESTRAINT_ERROR}.\n"

        if not validRange:
            return None

        if target_value is not None:
            if ANGLE_RANGE_MIN <= target_value <= ANGLE_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value:.3f}' should be within range {ANGLE_RESTRAINT_RANGE}.\n"

        if lower_limit is not None:
            if ANGLE_RANGE_MIN <= lower_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.\n"

        if upper_limit is not None:
            if ANGLE_RANGE_MIN <= upper_limit <= ANGLE_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit}' should be within range {ANGLE_RESTRAINT_RANGE}.\n"

        return dstFunc

    # Enter a parse tree produced by CyanaMRParser#rdc_restraints.
    def enterRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'rdc'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

        self.rdcParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#rdc_restraints.
    def exitRdc_restraints(self, ctx: CyanaMRParser.Rdc_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#rdc_parameter.
    def enterRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#rdc_parameter.
    def exitRdc_parameter(self, ctx: CyanaMRParser.Rdc_parameterContext):
        orientation = self.__cur_rdc_orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1)))

        self.rdcParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.__debug:
            print(f"subtype={self.__cur_subtype} orientation={orientation} "
                  f"parameters={self.rdcParameterDict[orientation]}")

        self.numberSelection.clear()

        if self.__createSfDict:
            self.__addSf()

    # Enter a parse tree produced by CyanaMRParser#rdc_restraint.
    def enterRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):  # pylint: disable=unused-argument
        self.rdcRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#rdc_restraint.
    def exitRdc_restraint(self, ctx: CyanaMRParser.Rdc_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            if None in self.numberSelection:
                self.rdcRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer(2)))
            # if len(self.numberSelection) > 3:
            #     scale = self.numberSelection[3]

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            if orientation not in self.rdcParameterDict:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The orientation '{orientation}' must be defined before you start to describe RDC restraints.\n"
                return

            if seqId1 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The residue number '{seqId1}' must not be the same as the center of orientation.\n"
                return

            if seqId2 == self.rdcParameterDict[orientation]['orientation_center_seq_id']:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The residue number '{seqId2}' must not be the same as the center of orientation.\n"
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validateRdcRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('an RDC'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Non-magnetic susceptible spin appears in RDC vector; "\
                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "\
                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Found inter-chain RDC vector; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'gap_in_auth_seq' in ps and ps['gap_in_auth_seq']), None)
                if ps1 is None:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Found inter-residue RDC vector; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                         or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        "Found inter-residue RDC vector; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

            elif atom_id_1 == atom_id_2:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    "Found zero RDC vector; "\
                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                return

            elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                if not any(b for b in self.__ccU.lastBonds
                           if ((b[self.__ccU.ccbAtomId1] == atom_id_1 and b[self.__ccU.ccbAtomId2] == atom_id_2)
                               or (b[self.__ccU.ccbAtomId1] == atom_id_2 and b[self.__ccU.ccbAtomId2] == atom_id_1))):

                    if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                        self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                            "Found an RDC vector over multiple covalent bonds; "\
                            f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                        return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None,
                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                    sf['loop'].add_data(row)

        except ValueError:
            self.rdcRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validateRdcRange(self, weight, orientation, target_value, lower_limit, upper_limit):
        """ Validate RDC value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if orientation is not None:
            dstFunc['orientation'] = orientation

        if target_value is not None:
            if RDC_ERROR_MIN < target_value < RDC_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' must be within range {RDC_RESTRAINT_ERROR}.\n"

        if lower_limit is not None:
            if RDC_ERROR_MIN <= lower_limit < RDC_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.\n"

        if upper_limit is not None:
            if RDC_ERROR_MIN < upper_limit <= RDC_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit:.6f}' must be within range {RDC_RESTRAINT_ERROR}.\n"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.\n"

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.\n"

        if not validRange:
            return None

        if target_value is not None:
            if RDC_RANGE_MIN <= target_value <= RDC_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' should be within range {RDC_RESTRAINT_RANGE}.\n"

        if lower_limit is not None:
            if RDC_RANGE_MIN <= lower_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.\n"

        if upper_limit is not None:
            if RDC_RANGE_MIN <= upper_limit <= RDC_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit:.6f}' should be within range {RDC_RESTRAINT_RANGE}.\n"

        return dstFunc

    def areUniqueCoordAtoms(self, subtype_name):
        """ Check whether atom selection sets are uniquely assigned.
        """

        for _atomSelectionSet in self.atomSelectionSet:

            if len(_atomSelectionSet) < 2:
                continue

            for (atom1, atom2) in itertools.combinations(_atomSelectionSet, 2):
                if atom1['chain_id'] != atom2['chain_id']:
                    continue
                if atom1['seq_id'] != atom2['seq_id']:
                    continue
                self.warningMessage += f"[Invalid atom selection] {self.__getCurrentRestraint()}"\
                    f"Ambiguous atom selection '{atom1['chain_id']}:{atom1['seq_id']}:{atom1['comp_id']}:{atom1['atom_id']} or "\
                    f"{atom2['atom_id']}' is not allowed as {subtype_name} restraint.\n"
                return False

        return True

    # Enter a parse tree produced by CyanaMRParser#pcs_restraints.
    def enterPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'pcs'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

        self.pcsParameterDict = {}

    # Exit a parse tree produced by CyanaMRParser#pcs_restraints.
    def exitPcs_restraints(self, ctx: CyanaMRParser.Pcs_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#pcs_parameter.
    def enterPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#pcs_parameter.
    def exitPcs_parameter(self, ctx: CyanaMRParser.Pcs_parameterContext):
        orientation = int(str(ctx.Integer(0)))
        magnitude = self.numberSelection[0]
        rhombicity = self.numberSelection[1]
        orientationCenterSeqId = int(str(ctx.Integer(1)))

        self.pcsParameterDict[orientation] = {'magnitude': magnitude,
                                              'rhombicity': rhombicity,
                                              'orientation_center_seq_id': orientationCenterSeqId}

        if self.__debug:
            print(f"subtype={self.__cur_subtype} orientation={orientation} "
                  f"parameters={self.pcsParameterDict[orientation]}")

        self.numberSelection.clear()

        if self.__createSfDict:
            self.__addSf()

    # Enter a parse tree produced by CyanaMRParser#pcs_restraint.
    def enterPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument
        self.pcsRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#pcs_restraint.
    def exitPcs_restraint(self, ctx: CyanaMRParser.Pcs_restraintContext):  # pylint: disable=unused-argument

        try:

            seqId = int(str(ctx.Integer(0)))
            compId = str(ctx.Simple_name(0)).upper()
            atomId = str(ctx.Simple_name(1)).upper()

            if None in self.numberSelection:
                self.pcsRestraints -= 1
                return

            target = self.numberSelection[0]
            error = abs(self.numberSelection[1])
            weight = self.numberSelection[2]
            orientation = int(str(ctx.Integer(1)))

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            if orientation not in self.pcsParameterDict:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The orientation '{orientation}' must be defined before you start to describe PCS restraints.\n"
                return

            if seqId == self.pcsParameterDict[orientation]['orientation_center_seq_id']:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The residue number '{seqId}' must not be the same as the center of orientation.\n"
                return

            target_value = target
            lower_limit = target - error
            upper_limit = target + error

            dstFunc = self.validatePcsRange(weight, orientation, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign = self.assignCoordPolymerSequence(seqId, compId, atomId)

            if len(chainAssign) == 0:
                return

            self.selectCoordAtoms(chainAssign, seqId, compId, atomId)

            if len(self.atomSelectionSet) < 1:
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            for atom in self.atomSelectionSet[0]:
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.pcsRestraints} "
                          f"atom={atom} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None,
                                 sf['list_id'], self.__entryId, dstFunc, atom)
                    sf['loop'].add_data(row)

        except ValueError:
            self.pcsRestraints -= 1
        finally:
            self.numberSelection.clear()

    def validatePcsRange(self, weight, orientation, target_value, lower_limit, upper_limit):
        """ Validate PCS value range.
        """

        validRange = True
        dstFunc = {'weight': weight, 'orientation': orientation}

        if target_value is not None:
            if PCS_ERROR_MIN < target_value < PCS_ERROR_MAX:
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' must be within range {PCS_RESTRAINT_ERROR}.\n"

        if lower_limit is not None:
            if PCS_ERROR_MIN <= lower_limit < PCS_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit:.6f}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.\n"

        if upper_limit is not None:
            if PCS_ERROR_MIN < upper_limit <= PCS_ERROR_MAX:
                dstFunc['upper_limit'] = f"{upper_limit:.6f}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit:.6f}' must be within range {PCS_RESTRAINT_ERROR}.\n"

        if target_value is not None:

            if lower_limit is not None:
                if lower_limit > target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit:.6f}' must be less than the target value '{target_value}'.\n"

            if upper_limit is not None:
                if upper_limit < target_value:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit:.6f}' must be greater than the target value '{target_value}'.\n"

        if not validRange:
            return None

        if target_value is not None:
            if PCS_RANGE_MIN <= target_value <= PCS_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' should be within range {PCS_RESTRAINT_RANGE}.\n"

        if lower_limit is not None:
            if PCS_RANGE_MIN <= lower_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.\n"

        if upper_limit is not None:
            if PCS_RANGE_MIN <= upper_limit <= PCS_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit:.6f}' should be within range {PCS_RESTRAINT_RANGE}.\n"

        return dstFunc

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def enterFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixres' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraints.
    def exitFixres_distance_restraints(self, ctx: CyanaMRParser.Fixres_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def enterFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixres_distance_restraint.
    def exitFixres_distance_restraint(self, ctx: CyanaMRParser.Fixres_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col, value in enumerate(self.numberSelection):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixres'] = True

                else:  # 'noepk'

                    target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_dist_type == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def enterFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixresw' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraints.
    def exitFixresw_distance_restraints(self, ctx: CyanaMRParser.Fixresw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def enterFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw_distance_restraint.
    def exitFixresw_distance_restraint(self, ctx: CyanaMRParser.Fixresw_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 2):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]

                delta = None
                has_square = False

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    weight = 1.0
                    has_square = True

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if has_square:
                        if value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.__applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.__applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw'] = True

                else:  # 'noepk'

                    if has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def enterFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixresw2' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraints.
    def exitFixresw2_distance_restraints(self, ctx: CyanaMRParser.Fixresw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def enterFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixresw2_distance_restraint.
    def exitFixresw2_distance_restraint(self, ctx: CyanaMRParser.Fixresw2_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()

            int_col = 1
            str_col = 1

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 3):
                atomId1 = str(ctx.Simple_name(str_col)).upper()
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col + 1)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 2)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixresw2'] = True

                else:  # 'noepk'

                    lower_limit = value
                    upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 3

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def enterFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatm' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraints.
    def exitFixatm_distance_restraints(self, ctx: CyanaMRParser.Fixatm_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def enterFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatm_distance_restraint.
    def exitFixatm_distance_restraint(self, ctx: CyanaMRParser.Fixatm_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col, value in enumerate(self.numberSelection):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    dstFunc = self.validateDistanceRange(1.0, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and abs(value) > DIST_ERROR_MAX * 10.0:
                        self.reasonsForReParsing['noepk_fixatm'] = True

                else:  # 'noepk'

                    target_value = value

                    dstFunc = self.validatePeakVolumeRange(1.0, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def enterFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatmw' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraints.
    def exitFixatmw_distance_restraints(self, ctx: CyanaMRParser.Fixatmw_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def enterFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw_distance_restraint.
    def exitFixatmw_distance_restraint(self, ctx: CyanaMRParser.Fixatmw_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 2):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]

                delta = None
                has_square = False

                if value2 < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{value2}' must not be a negative value.\n"
                    return
                if value2 == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{value2}' should be a positive value.\n"

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    weight = 1.0
                    has_square = True

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if has_square:
                        if value2 > DIST_RANGE_MAX:  # lol_only
                            lower_limit = value

                        elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                            upper_limit = value2
                            lower_limit = value
                            if self.__applyPdbStatCap:
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                        else:  # upl_only
                            if value2 > 1.8:
                                upper_limit = value2
                                if self.__applyPdbStatCap:
                                    lower_limit = 1.8  # default value of PDBStat
                                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                            else:
                                upper_limit = value2

                    elif delta is not None:
                        target_value = value
                        if delta > 0.0:
                            lower_limit = value - delta
                            upper_limit = value + delta

                    elif self.__upl_or_lol is None:
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_only':
                        if self.__cur_dist_type == 'upl':
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        elif self.__cur_dist_type == 'lol':
                            lower_limit = value
                        elif value > 1.8:
                            upper_limit = value
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            lower_limit = value

                    elif self.__upl_or_lol == 'upl_w_lol':
                        upper_limit = value

                    elif self.__upl_or_lol == 'lol_only':
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            upper_limit = 5.5  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # 'lol_w_upl'
                        lower_limit = value

                    if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                        self.__local_dist_types.append(self.__cur_dist_type)

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw'] = True

                else:  # 'noepk'

                    if has_square:
                        lower_limit = value
                        upper_limit = value2
                    else:
                        target_value = value

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def enterFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist' if self.__file_ext is None or self.__file_ext not in ('upv', 'lov') else 'noepk'
        if self.__reasons is not None and 'noepk_fixatmw2' in self.__reasons:
            self.__cur_subtype = 'noepk'

        self.__cur_subtype_altered = False
        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraints.
    def exitFixatmw2_distance_restraints(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def enterFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):  # pylint: disable=unused-argument
        if self.__cur_subtype == 'dist':
            self.distRestraints += 1
        else:
            self.noepkRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#fixatmw2_distance_restraint.
    def exitFixatmw2_distance_restraint(self, ctx: CyanaMRParser.Fixatmw2_distance_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()

            int_col = 1
            str_col = 2

            omit_dist_limit_outlier = self.__reasons is not None and self.__omitDistLimitOutlier

            if None in self.numberSelection:
                if self.__cur_subtype == 'dist':
                    self.distRestraints -= 1
                else:
                    self.noepkRestraints -= 1
                return

            for num_col in range(0, len(self.numberSelection), 3):
                seqId2 = int(str(ctx.Integer(int_col)))
                compId2 = str(ctx.Simple_name(str_col)).upper()
                atomId2 = str(ctx.Simple_name(str_col + 1)).upper()

                value = self.numberSelection[num_col]
                value2 = self.numberSelection[num_col + 1]
                weight = self.numberSelection[num_col + 2]

                if weight < 0.0:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' must not be a negative value.\n"
                    return
                if weight == 0.0:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The relative weight value of '{weight}' should be a positive value.\n"

                target_value = None
                lower_limit = None
                upper_limit = None

                if self.__cur_subtype == 'dist':

                    if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                        if value > self.__max_dist_value:
                            self.__max_dist_value = value
                        if value < self.__min_dist_value:
                            self.__min_dist_value = value

                    if value2 > DIST_RANGE_MAX:  # lol_only
                        lower_limit = value

                    elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                        upper_limit = value2
                        lower_limit = value
                        if self.__applyPdbStatCap:
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                    else:  # upl_only
                        if value2 > 1.8:
                            upper_limit = value2
                            if self.__applyPdbStatCap:
                                lower_limit = 1.8  # default value of PDBStat
                                target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                        else:
                            upper_limit = value2

                    dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier)

                    if dstFunc is None and (abs(value) > DIST_ERROR_MAX * 10.0 or abs(value2) > DIST_ERROR_MAX * 10.0):
                        self.reasonsForReParsing['noepk_fixatmw2'] = True

                else:  # 'noepk'

                    lower_limit = value
                    upper_limit = value2

                    dstFunc = self.validatePeakVolumeRange(weight, target_value, lower_limit, upper_limit)

                if dstFunc is None:
                    return

                if not self.__hasPolySeq:
                    return

                self.__retrieveLocalSeqScheme()

                chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
                chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                        continue
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                              f"atom1={atom1} atom2={atom2} {dstFunc}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', memberLogicCode,
                                     sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                        sf['loop'].add_data(row)
                        if self.__cur_subtype == 'noepk':
                            break

                if num_col > 0 and self.__cur_subtype == 'dist':
                    self.distRestraints += 1

                int_col += 1
                str_col += 2

        except ValueError:
            if self.__cur_subtype == 'dist':
                self.distRestraints -= 1
            else:
                self.noepkRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def enterQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraints.
    def exitQconvr_distance_restraints(self, ctx: CyanaMRParser.Qconvr_distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def enterQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#qconvr_distance_restraint.
    def exitQconvr_distance_restraint(self, ctx: CyanaMRParser.Qconvr_distance_restraintContext):

        try:

            upl = bool(ctx.NoeUpp())

            seqId1 = int(str(ctx.Integer(0)))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            seqId2 = int(str(ctx.Integer(1)))
            compId2 = str(ctx.Simple_name(2)).upper()
            atomId2 = str(ctx.Simple_name(3)).upper()

            target_value = None
            lower_limit = None
            upper_limit = None

            if None in self.numberSelection:
                return

            value = self.numberSelection[0]
            weight = 1.0

            if not self.__hasPolySeq:
                return

            if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX:
                if upl and value > self.__max_dist_value:
                    self.__max_dist_value = value
                if not upl and value < self.__min_dist_value:
                    self.__min_dist_value = value

            if upl:
                upper_limit = value
            else:
                lower_limit = value

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, self.__omitDistLimitOutlier)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberLogicCode,
                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                    sf['loop'].add_data(row)

        except ValueError:
            self.distRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def enterDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraints.
    def exitDistance_w_chain_restraints(self, ctx: CyanaMRParser.Distance_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def enterDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain_restraint.
    def exitDistance_w_chain_restraint(self, ctx: CyanaMRParser.Distance_w_chain_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer(0)))
            seqId2 = int(str(ctx.Integer(1)))
            jVal = [''] * 6
            for j in range(6):
                jVal[j] = str(ctx.Simple_name(j)).upper()

            if len(self.__col_order_of_dist_w_chain) == 0:
                for j in range(3):
                    if len(jVal[j]) > 2 and translateToStdResName(jVal[j]) in monDict3:
                        self.__col_order_of_dist_w_chain['comp_id_1'] = j
                        compId = jVal[j]
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if _atomId_ != atomId:
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['atom_id_1'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_1'] = 3 - (j + k)
                                        break
                for j in range(3, 6):
                    if len(jVal[j]) > 2 and translateToStdResName(jVal[j]) in monDict3:
                        self.__col_order_of_dist_w_chain['comp_id_2'] = j
                        compId = jVal[j]
                        if self.__ccU.updateChemCompDict(compId):
                            for k in range(3, 6):
                                if k == j:
                                    continue
                                atomId = jVal[k]
                                _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId, leave_unmatched=True)
                                if details is not None and len(atomId) > 1 and not atomId[-1].isalpha():
                                    _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(compId, atomId[:-1], leave_unmatched=True)

                                if details is not None:
                                    _atomId_ = translateToStdAtomName(atomId, compId, ccU=self.__ccU)
                                    if _atomId_ != atomId:
                                        _atomId = self.__nefT.get_valid_star_atom_in_xplor(compId, _atomId_)[0]
                                if len(_atomId) > 0:
                                    cca = next((cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == _atomId[0]), None)
                                    if cca is not None:
                                        self.__col_order_of_dist_w_chain['atom_id_2'] = k
                                        self.__col_order_of_dist_w_chain['chain_id_2'] = 12 - (j + k)
                                        break

            if len(self.__col_order_of_dist_w_chain) != 6:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Failed to identify columns for comp_id_1, atom_id_1, chain_id_1, comp_id_2, atom_id_2, chain_id_2.\n"
                self.distRestraints -= 1
                return

            if None in self.numberSelection:
                self.distRestraints -= 1
                return

            target_value = None
            lower_limit = None
            upper_limit = None

            value = self.numberSelection[0]
            weight = 1.0

            delta = None
            has_square = False

            if len(self.numberSelection) > 2:
                value2 = self.numberSelection[1]
                weight = self.numberSelection[2]

                has_square = True

            elif len(self.numberSelection) > 1:
                value2 = self.numberSelection[1]

                if value2 <= 1.0 or value2 < value:
                    delta = abs(value2)
                else:
                    has_square = True

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            if DIST_RANGE_MIN <= value <= DIST_RANGE_MAX and not self.__cur_subtype_altered:
                if value > self.__max_dist_value:
                    self.__max_dist_value = value
                if value < self.__min_dist_value:
                    self.__min_dist_value = value

            if has_square:
                if value2 > DIST_RANGE_MAX:  # lol_only
                    lower_limit = value

                elif 1.8 <= value <= DIST_ERROR_MAX and DIST_RANGE_MIN <= value2 <= DIST_RANGE_MAX:
                    upper_limit = value2
                    lower_limit = value
                    if self.__applyPdbStatCap:
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

                else:  # upl_only
                    if value2 > 1.8:
                        upper_limit = value2
                        if self.__applyPdbStatCap:
                            lower_limit = 1.8  # default value of PDBStat
                            target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                    else:
                        upper_limit = value2

            elif delta is not None:
                target_value = value
                if delta > 0.0:
                    lower_limit = value - delta
                    upper_limit = value + delta

            elif self.__upl_or_lol is None:
                if self.__cur_dist_type == 'upl':
                    upper_limit = value
                elif self.__cur_dist_type == 'lol':
                    lower_limit = value
                elif value > 1.8:
                    upper_limit = value
                else:
                    lower_limit = value

            elif self.__upl_or_lol == 'upl_only':
                if self.__cur_dist_type == 'upl':
                    upper_limit = value
                    if self.__applyPdbStatCap:
                        lower_limit = 1.8  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                elif self.__cur_dist_type == 'lol':
                    lower_limit = value
                elif value > 1.8:
                    upper_limit = value
                    if self.__applyPdbStatCap:
                        lower_limit = 1.8  # default value of PDBStat
                        target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat
                else:
                    lower_limit = value

            elif self.__upl_or_lol == 'upl_w_lol':
                upper_limit = value

            elif self.__upl_or_lol == 'lol_only':
                lower_limit = value
                if self.__applyPdbStatCap:
                    upper_limit = 5.5  # default value of PDBStat
                    target_value = (upper_limit + lower_limit) / 2.0  # default procedure of PDBStat

            else:  # 'lol_w_upl'
                lower_limit = value

            if len(self.__cur_dist_type) > 0 and self.__cur_dist_type not in self.__local_dist_types:
                self.__local_dist_types.append(self.__cur_dist_type)

            if not self.__hasPolySeq:  # can't decide whether NOE or RDC wo the coordinates
                return

            chainId1 = jVal[self.__col_order_of_dist_w_chain['chain_id_1']]
            chainId2 = jVal[self.__col_order_of_dist_w_chain['chain_id_2']]
            compId1 = jVal[self.__col_order_of_dist_w_chain['comp_id_1']]
            compId2 = jVal[self.__col_order_of_dist_w_chain['comp_id_2']]
            atomId1 = jVal[self.__col_order_of_dist_w_chain['atom_id_1']]
            atomId2 = jVal[self.__col_order_of_dist_w_chain['atom_id_2']]

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if len(self.atomSelectionSet[0]) == 1 and len(self.atomSelectionSet[1]) == 1:

                isRdc = True

                chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
                seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
                comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
                atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

                chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
                seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
                comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
                atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

                if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                    isRdc = False

                if chain_id_1 != chain_id_2:
                    isRdc = False

                if abs(seq_id_1 - seq_id_2) > 1:
                    isRdc = False

                if abs(seq_id_1 - seq_id_2) == 1:

                    if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                            ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                             or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')):
                        pass

                    else:
                        isRdc = False

                elif atom_id_1 == atom_id_2:
                    isRdc = False

                elif self.__ccU.updateChemCompDict(comp_id_1):  # matches with comp_id in CCD

                    if not any(b for b in self.__ccU.lastBonds
                               if ((b[self.__ccU.ccbAtomId1] == atom_id_1 and b[self.__ccU.ccbAtomId2] == atom_id_2)
                                   or (b[self.__ccU.ccbAtomId1] == atom_id_2 and b[self.__ccU.ccbAtomId2] == atom_id_1))):

                        if self.__nefT.validate_comp_atom(comp_id_1, atom_id_1) and self.__nefT.validate_comp_atom(comp_id_2, atom_id_2):
                            isRdc = False

                if not isRdc:
                    self.__cur_subtype_altered = False

                else:

                    isRdc = False

                    if self.__cur_subtype_altered and atom_id_1 + atom_id_2 == self.auxAtomSelectionSet:
                        isRdc = True

                    elif value < 1.0 or value > 6.0:
                        self.auxAtomSelectionSet = atom_id_1 + atom_id_2
                        self.__cur_subtype_altered = True
                        self.__cur_rdc_orientation += 1
                        isRdc = True

                    if isRdc:
                        self.__cur_subtype = 'rdc'
                        self.rdcRestraints += 1
                        self.distRestraints -= 1

                        target_value = value
                        lower_limit = upper_limit = None

                        if len(self.numberSelection) > 2:
                            error = abs(self.numberSelection[1])
                            lower_limit = target_value - error
                            upper_limit = target_value + error

                        dstFunc = self.validateRdcRange(weight, self.__cur_rdc_orientation, target_value, lower_limit, upper_limit)

                        if dstFunc is None:
                            return

                        if self.__createSfDict:
                            sf = self.__getSf()
                            sf['id'] += 1

                        for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                              self.atomSelectionSet[1]):
                            if isLongRangeRestraint([atom1, atom2], self.__polySeq if self.__gapInAuthSeq else None):
                                continue
                            if self.__debug:
                                print(f"subtype={self.__cur_subtype} id={self.rdcRestraints} "
                                      f"atom1={atom1} atom2={atom2} {dstFunc}")
                            if self.__createSfDict and sf is not None:
                                sf['index_id'] += 1
                                row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                             '.', None,
                                             sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                                sf['loop'].add_data(row)

                        self.__cur_subtype = 'dist'

                        return

            dstFunc = self.validateDistanceRange(weight, target_value, lower_limit, upper_limit, self.__omitDistLimitOutlier)

            if dstFunc is None:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithChainId(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithChainId(chainId2, seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.distRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    memberLogicCode = '.' if len(self.atomSelectionSet[0]) * len(self.atomSelectionSet[1]) > 1 else 'OR'
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', memberLogicCode,
                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                    sf['loop'].add_data(row)

        except ValueError:
            self.distRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def enterDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraints.
    def exitDistance_w_chain2_restraints(self, ctx: CyanaMRParser.Distance_w_chain2_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def enterDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain2_restraint.
    def exitDistance_w_chain2_restraint(self, ctx: CyanaMRParser.Distance_w_chain2_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def enterDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraints.
    def exitDistance_w_chain3_restraints(self, ctx: CyanaMRParser.Distance_w_chain3_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def enterDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#distance_w_chain3_restraint.
    def exitDistance_w_chain3_restraint(self, ctx: CyanaMRParser.Distance_w_chain3_restraintContext):
        self.exitDistance_w_chain_restraint(ctx)

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def enterTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraints.
    def exitTorsion_angle_w_chain_restraints(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def enterTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#torsion_angle_w_chain_restraint.
    def exitTorsion_angle_w_chain_restraint(self, ctx: CyanaMRParser.Torsion_angle_w_chain_restraintContext):

        try:

            chainId = str(ctx.Simple_name(0))
            seqId = int(str(ctx.Integer()))
            compId = str(ctx.Simple_name(1)).upper()
            angleName = str(ctx.Simple_name(2)).upper()

            if None in self.numberSelection:
                self.dihedRestraints -= 1
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]

            if self.__remediate and self.__reasons is not None and 'dihed_unusual_order' in self.__reasons:
                target_value, deviation = lower_limit, upper_limit
                if deviation > 0.0:
                    lower_limit = target_value - deviation
                    upper_limit = target_value + deviation
                else:
                    lower_limit = upper_limit = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                weight = self.numberSelection[2]

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"
            """
            if lower_limit > upper_limit:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The angle's lower limit '{lower_limit}' must be less than or equal to the upper limit '{upper_limit}'.\n"
                if self.__remediate:
                    self.__dihed_lb_greater_than_ub = True
                return
            """
            if self.__remediate and upper_limit < 0.0:
                self.__dihed_ub_always_positive = False

            # target_value = (upper_limit + lower_limit) / 2.0

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            # support AMBER's dihedral angle naming convention for nucleic acids
            # http://ambermd.org/tutorials/advanced/tutorial4/
            if angleName in ('EPSILN', 'EPSLN'):
                angleName = 'EPSILON'

            # nucleic CHI angle
            if angleName == 'CHIN':
                angleName = 'CHI'

            if angleName not in KNOWN_ANGLE_NAMES:
                lenAngleName = len(angleName)
                try:
                    # For the case 'EPSIL' could be standard name 'EPSILON'
                    angleName = next(name for name in KNOWN_ANGLE_NAMES if len(name) >= lenAngleName and name[:lenAngleName] == angleName)
                except StopIteration:
                    self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                        f"The angle identifier {str(ctx.Simple_name(2))!r} is unknown for the residue {compId!r}, "\
                        "of which CYANA residue library should be uploaded.\n"
                    return

            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            if carbohydrate:
                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, 'CA')
                if len(chainAssign) > 0:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainAssign[0][0])
                    if 'type' in ps and 'polypeptide' in ps['type']:
                        peptide = True
                        nucleotide = carbohydrate = False

            if carbohydrate and angleName in KNOWN_ANGLE_CARBO_ATOM_NAMES:
                atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
            else:
                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

            if angleName != 'PPA':

                if isinstance(atomNames, list):
                    atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                else:  # nucleic CHI angle
                    atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                    if atomId is None and carbohydrate:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                        if isinstance(atomNames, list):
                            atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)
                        else:  # nucleic CHI angle
                            atomId = next(name for name, offset in zip(atomNames['Y'], seqOffset['Y']) if offset == 0)

                        if not isinstance(atomId, str):
                            atomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)
                            if atomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId}:{compId} is not present in the coordinates.\n"
                                return

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{seqId}:{compId} is not present in the coordinates.\n"
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    if peptide and angleName in ('PHI', 'PSI', 'OMEGA',
                                                 'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                                                 'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42'):
                        pass
                    elif nucleotide and angleName in ('ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON', 'ZETA',
                                                      'CHI', 'ETA', 'THETA', "ETA'", "THETA'",
                                                      'NU0', 'NU1', 'NU2', 'NU3', 'NU4',
                                                      'TAU0', 'TAU1', 'TAU2', 'TAU3', 'TAU4'):
                        pass
                    elif carbohydrate and angleName in ('PHI', 'PSI', 'OMEGA'):
                        pass
                    else:
                        self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                            f"The angle identifier {str(ctx.Simple_name(2))!r} is unknown for the residue {compId!r}, "\
                            "of which CYANA residue library should be uploaded.\n"
                        return

                    atomNames = None
                    seqOffset = None

                    if carbohydrate:
                        atomNames = KNOWN_ANGLE_CARBO_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_CARBO_SEQ_OFFSET[angleName]
                    elif nucleotide and angleName == 'CHI':
                        if self.__ccU.updateChemCompDict(cifCompId):
                            try:
                                next(cca for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == 'N9')
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['R']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['R']
                            except StopIteration:
                                atomNames = KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']
                                seqOffset = KNOWN_ANGLE_SEQ_OFFSET['CHI']['Y']
                    else:
                        atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                        seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    atomSelection = []

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection.clear()

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.warningMessage += f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"\
                                    f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "\
                                    "Please update the sequence in the Macromolecules page.\n"
                                _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            if isinstance(atomId, str):
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)
                            else:
                                cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId])), None)

                            if cifAtomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.\n"
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 4:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf()
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                        self.atomSelectionSet[1],
                                                                        self.atomSelectionSet[2],
                                                                        self.atomSelectionSet[3]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', angleName,
                                         sf['list_id'], self.__entryId, dstFunc, atom1, atom2, atom3, atom4)
                            sf['loop'].add_data(row)

            # phase angle of pseudorotation
            else:

                atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                atomId = next(name for name, offset in zip(atomNames, seqOffset) if offset == 0)

                if not isinstance(atomId, str):
                    self.__ccU.updateChemCompDict(compId)
                    atomId = next(cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if atomId.match(cca[self.__ccU.ccaAtomId]))

                self.__retrieveLocalSeqScheme()

                chainAssign = self.assignCoordPolymerSequenceWithChainId(chainId, seqId, compId, atomId)

                if len(chainAssign) == 0:
                    self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                        f"{seqId}:{compId} is not present in the coordinates.\n"
                    return

                for chainId, cifSeqId, cifCompId, _ in chainAssign:
                    ps = next(ps for ps in self.__polySeq if ps['auth_chain_id'] == chainId)

                    peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(cifCompId)

                    atomNames = KNOWN_ANGLE_ATOM_NAMES[angleName]
                    seqOffset = KNOWN_ANGLE_SEQ_OFFSET[angleName]

                    if nucleotide:
                        pass
                    else:
                        self.warningMessage += f"[Insufficient angle selection] {self.__getCurrentRestraint()}"\
                            f"The angle identifier {str(ctx.Simple_name(2))!r} did not match with residue {compId!r}.\n"
                        return

                    atomSelection = []

                    for atomId, offset in zip(atomNames, seqOffset):

                        atomSelection.clear()

                        _cifSeqId = cifSeqId + offset
                        _cifCompId = cifCompId if offset == 0 else (ps['comp_id'][ps['auth_seq_id'].index(_cifSeqId)] if _cifSeqId in ps['auth_seq_id'] else None)

                        if _cifCompId is None:
                            try:
                                _cifCompId = ps['comp_id'][ps['auth_seq_id'].index(cifSeqId) + offset]
                            except IndexError:
                                pass
                            if _cifCompId is None:
                                self.warningMessage += f"[Sequence mismatch warning] {self.__getCurrentRestraint()}"\
                                    f"The residue number '{seqId+offset}' is not present in polymer sequence of chain {chainId} of the coordinates. "\
                                    "Please update the sequence in the Macromolecules page.\n"
                                _cifCompId = '.'
                            cifAtomId = atomId

                        else:
                            self.__ccU.updateChemCompDict(_cifCompId)

                            cifAtomId = next((cca[self.__ccU.ccaAtomId] for cca in self.__ccU.lastAtomList if cca[self.__ccU.ccaAtomId] == atomId), None)

                            if cifAtomId is None:
                                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                                    f"{seqId+offset}:{compId}:{atomId} is not present in the coordinates.\n"
                                return

                        atomSelection.append({'chain_id': chainId, 'seq_id': _cifSeqId, 'comp_id': _cifCompId, 'atom_id': cifAtomId})

                        if len(atomSelection) > 0:
                            self.atomSelectionSet.append(atomSelection)

                    if len(self.atomSelectionSet) < 5:
                        return

                    if not self.areUniqueCoordAtoms('a Torsion angle'):
                        return

                    if self.__createSfDict:
                        sf = self.__getSf()
                        sf['id'] += 1

                    for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                               self.atomSelectionSet[1],
                                                                               self.atomSelectionSet[2],
                                                                               self.atomSelectionSet[3],
                                                                               self.atomSelectionSet[4]):
                        if isLongRangeRestraint([atom1, atom2, atom3, atom4, atom5], self.__polySeq if self.__gapInAuthSeq else None):
                            continue
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                                  f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5} {dstFunc}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', angleName,
                                         sf['list_id'], self.__entryId, dstFunc, None, None, None, None, atom5)
                            sf['loop'].add_data(row)

        except ValueError:
            self.dihedRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#cco_restraints.
    def enterCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'jcoup'

        self.__cur_subtype_altered = False

    # Exit a parse tree produced by CyanaMRParser#cco_restraints.
    def exitCco_restraints(self, ctx: CyanaMRParser.Cco_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#cco_restraint.
    def enterCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):  # pylint: disable=unused-argument
        self.jcoupRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#cco_restraint.
    def exitCco_restraint(self, ctx: CyanaMRParser.Cco_restraintContext):

        try:

            seqId1 = int(str(ctx.Integer()))
            compId1 = str(ctx.Simple_name(0)).upper()
            atomId1 = str(ctx.Simple_name(1)).upper()
            atomId2 = str(ctx.Simple_name(2)).upper()

            if None in self.numberSelection:
                self.jcoupRestraints -= 1
                return

            if atomId2 in KNOWN_ANGLE_NAMES:
                self.__cur_subtype_altered = True
                self.__cur_subtype = 'dihed'
                self.dihedRestraints += 1
                self.jcoupRestraints -= 1
                self.exitTorsion_angle_restraint(ctx)
                return

            target = self.numberSelection[0]
            error = None

            weight = 1.0
            if len(self.numberSelection) > 2:
                error = abs(self.numberSelection[1])
                weight = self.numberSelection[2]

            elif len(self.numberSelection) > 1:
                error = abs(self.numberSelection[1])

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            target_value = target
            lower_limit = target - error if error is not None else None
            upper_limit = target + error if error is not None else None

            dstFunc = self.validateRdcRange(weight, None, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(seqId1, compId1, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId1, compId1, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a Scalar coupling'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            comp_id_1 = self.atomSelectionSet[0][0]['comp_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            comp_id_2 = self.atomSelectionSet[1][0]['comp_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            if (atom_id_1[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS) or (atom_id_2[0] not in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS):
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Non-magnetic susceptible spin appears in scalar coupling constant; "\
                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, "\
                    f"{chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                return

            if chain_id_1 != chain_id_2:
                ps1 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_1 and 'identical_auth_chain_id' in ps), None)
                ps2 = next((ps for ps in self.__polySeq if ps['auth_chain_id'] == chain_id_2 and 'identical_auth_chain_id' in ps), None)
                if ps1 is None and ps2 is None:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Found inter-chain scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

            elif abs(seq_id_1 - seq_id_2) > 1:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Found inter-residue scalar coupling constant; "\
                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                return

            elif abs(seq_id_1 - seq_id_2) == 1:

                if self.__csStat.peptideLike(comp_id_1) and self.__csStat.peptideLike(comp_id_2) and\
                        ((seq_id_1 < seq_id_2 and atom_id_1 == 'C' and atom_id_2 in ('N', 'H', 'CA'))
                         or (seq_id_1 > seq_id_2 and atom_id_1 in ('N', 'H', 'CA') and atom_id_2 == 'C')
                         or (seq_id_1 < seq_id_2 and atom_id_1.startswith('HA') and atom_id_2 == 'H')
                         or (seq_id_1 > seq_id_2 and atom_id_1 == 'H' and atom_id_2.startswith('HA'))):
                    pass

                else:
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        "Found inter-residue scalar coupling constant; "\
                        f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                    return

            elif atom_id_1 == atom_id_2:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    "Found zero scalar coupling constant; "\
                    f"({chain_id_1}:{seq_id_1}:{comp_id_1}:{atom_id_1}, {chain_id_2}:{seq_id_2}:{comp_id_2}:{atom_id_2}).\n"
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if isLongRangeRestraint([atom1, atom2], self.__polySeq):
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} id={self.jcoupRestraints} "
                          f"atom1={atom1} atom2={atom2} {dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    couplingCode = '3J' + (atom1['auth_atom_id'] if 'auth_atom_id' in atom1 else atom1['atom_id'])\
                        + (atom2['auth_atom_id'] if 'auth_atom_id' in atom2 else atom2['atom_id'])
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', couplingCode,
                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2)
                    sf['loop'].add_data(row)

        except ValueError:
            self.jcoupRestraints -= 1
        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by CyanaMRParser#ssbond_macro.
    def enterSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'ssbond'

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#ssbond_macro.
    def exitSsbond_macro(self, ctx: CyanaMRParser.Ssbond_macroContext):

        try:

            self.ssbondRestraints += 1

            try:
                _seqId1, _seqId2 = str(ctx.Ssbond_resids()).split('-')
                seqId1, seqId2 = int(_seqId1), int(_seqId2)
            except ValueError:
                self.ssbondRestraints -= 1
                return

            if not self.__hasPolySeq:
                return

            compId = 'CYSS'
            atomId = 'SG'

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(seqId1, compId, atomId)
            chainAssign2 = self.assignCoordPolymerSequence(seqId2, compId, atomId)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId, atomId)
            self.selectCoordAtoms(chainAssign2, seqId2, compId, atomId)

            if len(self.atomSelectionSet) < 2:
                return

            for atom1 in self.atomSelectionSet[0]:
                if atom1['comp_id'] != 'CYS':
                    self.warningMessage += f"[Invalid atom selection] {self.__getCurrentRestraint()}"\
                        f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.\n"
                    self.ssbondRestraints -= 1
                    return

            for atom2 in self.atomSelectionSet[1]:
                if atom2['comp_id'] != 'CYS':
                    self.warningMessage += f"[Invalid atom selection] {self.__getCurrentRestraint()}"\
                        f"Failed to select a Cystein residue for disulfide bond between '{seqId1}' and '{seqId2}'.\n"
                    self.ssbondRestraints -= 1
                    return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    distance = numpy.linalg.norm(toNpArray(_head[0]) - toNpArray(_tail[0]))
                    if distance > 2.5:
                        self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                            f"The distance of the disulfide bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "\
                            f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({distance:.3f}Å).\n"

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitSsbond_macro() ++ Error  - {str(e)}\n")

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA macro: disulfide bond linkage) id={self.ssbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None,
                                 sf['list_id'], self.__entryId, None, atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#hbond_macro.
    def enterHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'hbond'

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#hbond_macro.
    def exitHbond_macro(self, ctx: CyanaMRParser.Hbond_macroContext):

        try:

            self.hbondRestraints += 1

            seqId1 = int(str(ctx.Integer_HB(0)))
            seqId2 = int(str(ctx.Integer_HB(1)))
            atomId1 = str(ctx.Simple_name_HB(0))
            atomId2 = str(ctx.Simple_name_HB(1))

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a hydrogen bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    distance = numpy.linalg.norm(toNpArray(_head[0]) - toNpArray(_tail[0]))
                    if distance > (3.4 if atom_id_1[0] != 'H' and atom_id_2[0] != 'H' else 2.4):
                        self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                            f"The distance of the hydrogen bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "\
                            f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({distance:.3f}Å).\n"

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitHbond_macro() ++ Error  - {str(e)}\n")

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA macro: hydrogen bond linkage) id={self.hbondRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.', None,
                                 sf['list_id'], self.__entryId, None, atom1, atom2)
                    sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#link_statement.
    def enterLink_statement(self, ctx: CyanaMRParser.Link_statementContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#link_statement.
    def exitLink_statement(self, ctx: CyanaMRParser.Link_statementContext):

        try:

            self.geoRestraints += 1

            seqId1 = int(str(ctx.Integer(0)))
            seqId2 = int(str(ctx.Integer(1)))
            atomId1 = str(ctx.Simple_name(0))
            atomId2 = str(ctx.Simple_name(1))

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, None, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            if not self.areUniqueCoordAtoms('a covalent bond linkage'):
                return

            chain_id_1 = self.atomSelectionSet[0][0]['chain_id']
            seq_id_1 = self.atomSelectionSet[0][0]['seq_id']
            atom_id_1 = self.atomSelectionSet[0][0]['atom_id']

            chain_id_2 = self.atomSelectionSet[1][0]['chain_id']
            seq_id_2 = self.atomSelectionSet[1][0]['seq_id']
            atom_id_2 = self.atomSelectionSet[1][0]['atom_id']

            try:

                _head =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_1},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_1},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_1},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                _tail =\
                    self.__cR.getDictListWithFilter('atom_site',
                                                    [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                     {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                     {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'}
                                                     ],
                                                    [{'name': self.__authAsymId, 'type': 'str', 'value': chain_id_2},
                                                     {'name': self.__authSeqId, 'type': 'int', 'value': seq_id_2},
                                                     {'name': self.__authAtomId, 'type': 'str', 'value': atom_id_2},
                                                     {'name': self.__modelNumName, 'type': 'int',
                                                      'value': self.__representativeModelId},
                                                     {'name': 'label_alt_id', 'type': 'enum',
                                                      'enum': ('A')}
                                                     ])

                if len(_head) == 1 and len(_tail) == 1:
                    distance = numpy.linalg.norm(toNpArray(_head[0]) - toNpArray(_tail[0]))
                    if distance > (3.5 if atom_id_1[0] != 'H' and atom_id_2[0] != 'H' else 2.5):
                        self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                            f"The distance of the covalent bond linkage ({chain_id_1}:{seq_id_1}:{atom_id_1} - "\
                            f"{chain_id_2}:{seq_id_2}:{atom_id_2}) is too far apart in the coordinates ({distance:.3f}Å).\n"

            except Exception as e:
                if self.__verbose:
                    self.__lfh.write(f"+CyanaMRParserListener.exitLink_statement() ++ Error  - {str(e)}\n")

            if self.__createSfDict:
                sf = self.__getSf('covalent bond linkage')
                sf['id'] += 1
                if len(sf['loop']['tag']) == 0:
                    sf['loop']['tags'] = ['index_id', 'id',
                                          'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                          'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                          'list_id', 'entry_id']

            has_inter_chain = hasIntraChainResraint(self.atomSelectionSet)

            for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                  self.atomSelectionSet[1]):
                if has_inter_chain and atom1['chain_id'] != atom2['chain_id']:
                    continue
                if self.__debug:
                    print(f"subtype={self.__cur_subtype} (CYANA statement: covalent bond linkage) id={self.geoRestraints} "
                          f"atom1={atom1} atom2={atom2}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    sf['loop']['data'].append([sf['index_id'], sf['id'],
                                               atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                               atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                               sf['list_id'], self.__entryId])

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#stereoassign_macro.
    def enterStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'fchiral'

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by CyanaMRParser#stereoassign_macro.
    def exitStereoassign_macro(self, ctx: CyanaMRParser.Stereoassign_macroContext):

        try:

            self.fchiralRestraints += 1

            _strip = str(ctx.Double_quote_string()).strip('"').strip()
            _split = re.sub(' +', ' ', _strip).split(' ')

            len_split = len(_split)

            if len_split < 3:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.\n"
                return

            atomId1 = _split[0].upper()
            atomId2 = None

            if not atomId1.isalnum():
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.\n"
                return

            if _split[1].isdecimal():
                seq_id_offset = 1
            else:
                seq_id_offset = 2
                atomId2 = _split[1].upper()

            for l in range(seq_id_offset, len_split):
                if not _split[l].isdecimal():
                    self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                        f"Could not interpret '{str(ctx.Double_quote_string())}' as floating chiral stereo assignment.\n"
                    return

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            seqId1 = int(_split[seq_id_offset])

            chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

            if atomId2 is not None:

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None,
                                     sf['list_id'], self.__entryId, None, atom1, atom2)
                        sf['loop'].add_data(row)

                for l in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[l])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)
                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)
                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None,
                                         sf['list_id'], self.__entryId, None, atom1, atom2)
                            sf['loop'].add_data(row)

            else:

                if len(chainAssign1) == 0:
                    return

                self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                if len(self.atomSelectionSet) < 1:
                    return

                comp_id = self.atomSelectionSet[0][0]['comp_id']
                atom_id = self.atomSelectionSet[0][0]['atom_id']

                atomId2 = self.__csStat.getGeminalAtom(comp_id, atom_id)

                if atomId2 is None:
                    return

                chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                if len(chainAssign2) == 0:
                    return

                self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                if len(self.atomSelectionSet) < 2:
                    return

                if self.__createSfDict:
                    sf = self.__getSf()
                    sf['id'] += 1

                for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                      self.atomSelectionSet[1]):
                    if self.__debug:
                        print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                              f"atom1={atom1} atom2={atom2}")
                    if self.__createSfDict and sf is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     '.', None,
                                     sf['list_id'], self.__entryId, None, atom1, atom2)
                        sf['loop'].add_data(row)

                for l in range(seq_id_offset + 1, len_split):
                    self.atomSelectionSet.clear()

                    seqId1 = int(_split[l])

                    chainAssign1 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId1)

                    if len(chainAssign1) == 0:
                        return

                    self.selectCoordAtoms(chainAssign1, seqId1, None, atomId1)

                    if len(self.atomSelectionSet) < 1:
                        return

                    comp_id = self.atomSelectionSet[0][0]['comp_id']
                    atom_id = self.atomSelectionSet[0][0]['atom_id']

                    atomId2 = self.__csStat.getGeminalAtom(comp_id, atom_id)

                    if atomId2 is None:
                        return

                    chainAssign2 = self.assignCoordPolymerSequenceWithoutCompId(seqId1, atomId2)

                    if len(chainAssign2) == 0:
                        return

                    self.selectCoordAtoms(chainAssign2, seqId1, None, atomId2)

                    if len(self.atomSelectionSet) < 2:
                        return

                    for atom1, atom2 in itertools.product(self.atomSelectionSet[0],
                                                          self.atomSelectionSet[1]):
                        if self.__debug:
                            print(f"subtype={self.__cur_subtype} (CYANA macro: atom stereo) id={self.fchiralRestraints} "
                                  f"atom1={atom1} atom2={atom2}")
                        if self.__createSfDict and sf is not None:
                            sf['index_id'] += 1
                            row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                         '.', None,
                                         sf['list_id'], self.__entryId, None, atom1, atom2)
                            sf['loop'].add_data(row)

        finally:
            self.atomSelectionSet.clear()

    # Enter a parse tree produced by CyanaMRParser#declare_variable.
    def enterDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#declare_variable.
    def exitDeclare_variable(self, ctx: CyanaMRParser.Declare_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#set_variable.
    def enterSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#set_variable.
    def exitSet_variable(self, ctx: CyanaMRParser.Set_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unset_variable.
    def enterUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#unset_variable.
    def exitUnset_variable(self, ctx: CyanaMRParser.Unset_variableContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#print_macro.
    def enterPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#print_macro.
    def exitPrint_macro(self, ctx: CyanaMRParser.Print_macroContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def enterUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):
        self.__cur_resname_for_mapping = str(ctx.Simple_name()).upper()

        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#unambig_atom_name_mapping.
    def exitUnambig_atom_name_mapping(self, ctx: CyanaMRParser.Unambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#mapping_list.
    def enterMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#mapping_list.
    def exitMapping_list(self, ctx: CyanaMRParser.Mapping_listContext):
        atomName = str(ctx.Simple_name_MP(0)).upper()
        iupacName = set()

        i = 1
        while ctx.Simple_name_MP(i):
            iupacName.add(str(ctx.Simple_name_MP(i)).upper())
            i += 1

        if self.__cur_resname_for_mapping not in self.unambigAtomNameMapping:
            self.unambigAtomNameMapping[self.__cur_resname_for_mapping] = {}
        self.unambigAtomNameMapping[self.__cur_resname_for_mapping][atomName] = list(iupacName)

    # Enter a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def enterAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):
        self.__cur_resname_for_mapping = str(ctx.Simple_name()).upper()

        self.__cur_comment_inlined = True

    # Exit a parse tree produced by CyanaMRParser#ambig_atom_name_mapping.
    def exitAmbig_atom_name_mapping(self, ctx: CyanaMRParser.Ambig_atom_name_mappingContext):  # pylint: disable=unused-argument
        self.updateAmbigAtomNameMapping()

        self.__cur_comment_inlined = False

    # Enter a parse tree produced by CyanaMRParser#ambig_list.
    def enterAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#ambig_list.
    def exitAmbig_list(self, ctx: CyanaMRParser.Ambig_listContext):
        if ctx.Ambig_code_MP():
            ambigCode = str(ctx.Ambig_code_MP())
            i = 0
        else:
            ambigCode = str(ctx.Simple_name_MP(0)).upper()
            i = 1

        mapName = []

        j = 0
        while ctx.Simple_name_MP(i):
            mapName.append({'atom_name': str(ctx.Simple_name_MP(i)).upper(),
                            'seq_id': int(str(ctx.Integer_MP(j)))})
            i += 1
            j += 1

        if self.__cur_resname_for_mapping not in self.ambigAtomNameMapping:
            self.ambigAtomNameMapping[self.__cur_resname_for_mapping] = {}
        self.ambigAtomNameMapping[self.__cur_resname_for_mapping][ambigCode] = mapName

    def updateAmbigAtomNameMapping(self):
        if not self.__hasPolySeq or len(self.ambigAtomNameMapping) == 0:
            return

        unambigResidues = None
        if len(self.unambigAtomNameMapping) > 0:
            unambigResidues = [translateToStdResName(residue) for residue in self.unambigAtomNameMapping.keys()]

        for ambigDict in self.ambigAtomNameMapping.values():
            for ambigList in ambigDict.values():
                for ambig in ambigList:

                    if 'atom_id_list' in ambig:
                        continue

                    atomName = ambig['atom_name']
                    seqId = ambig['seq_id']

                    chainAssign = self.assignCoordPolymerSequenceWithoutCompId(seqId)

                    if len(chainAssign) == 0:
                        continue

                    ambig['atom_id_list'] = []

                    for cifChainId, cifSeqId, cifCompId, _ in chainAssign:

                        has_unambig = False

                        if unambigResidues is not None and cifCompId in unambigResidues:

                            unambigMap = next(v for k, v in self.unambigAtomNameMapping.items()
                                              if translateToStdResName(k) == cifCompId)

                            if atomName in unambigMap:

                                for cifAtomId in unambigMap[atomName]:
                                    ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                                  'seq_id': cifSeqId,
                                                                  'comp_id': cifCompId,
                                                                  'atom_id': cifAtomId})

                                has_unambig = True

                        if has_unambig:
                            continue

                        self.atomSelectionSet.clear()

                        self.selectCoordAtoms(chainAssign, seqId, None, ambig['atom_name'].upper(), enableWarning=False)

                        if len(self.atomSelectionSet[0]) > 0:
                            ambig['atom_id_list'].extend(self.atomSelectionSet[0])
                            continue

                        _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomName, leave_unmatched=True)
                        if details is not None and len(atomName) > 1:
                            _atomId, _, details = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, atomName[:-1], leave_unmatched=True)

                        if details is not None:
                            _atomId_ = translateToStdAtomName(atomName, cifCompId, ccU=self.__ccU)
                            if _atomId_ != atomName:
                                _atomId = self.__nefT.get_valid_star_atom_in_xplor(cifCompId, _atomId_)[0]

                        for cifAtomId in _atomId:
                            ambig['atom_id_list'].append({'chain_id': cifChainId,
                                                          'seq_id': cifSeqId,
                                                          'comp_id': cifCompId,
                                                          'atom_id': cifAtomId})

                    ambig['atom_id_list'] = [dict(s) for s in set(frozenset(atom.items()) for atom in ambig['atom_id_list'])]

    def atomIdListToChainAssign(self, atomIdList):  # pylint: disable=no-self-use
        chainAssign = set()
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    chainAssign.add((atom_id['chain_id'], atom_id['seq_id'], atom_id['comp_id']))
        return list(chainAssign)

    def atomIdListToAtomSelection(self, atomIdList):  # pylint: disable=no-self-use
        atomSelection = []
        for item in atomIdList:
            if 'atom_id_list' in item:
                for atom_id in item['atom_id_list']:
                    if atom_id not in atomSelection:
                        atomSelection.append(atom_id)
        return atomSelection

    # Enter a parse tree produced by CyanaMRParser#number.
    def enterNumber(self, ctx: CyanaMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#number.
    def exitNumber(self, ctx: CyanaMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    # Enter a parse tree produced by CyanaMRParser#gen_atom_name.
    def enterGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by CyanaMRParser#gen_atom_name.
    def exitGen_atom_name(self, ctx: CyanaMRParser.Gen_atom_nameContext):
        if ctx.Simple_name():
            self.genAtomNameSelection.append(str(ctx.Simple_name()))

        elif ctx.Ambig_code():
            self.genAtomNameSelection.append(str(ctx.Ambig_code()))

        else:
            self.genAtomNameSelection.append(None)

    def __getCurrentRestraint(self):
        if self.__cur_subtype == 'dist':
            return f"[Check the {self.distRestraints}th row of distance restraints] "
        if self.__cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of torsion angle restraints] "
        if self.__cur_subtype == 'rdc':
            return f"[Check the {self.rdcRestraints}th row of residual dipolar coupling restraints] "
        if self.__cur_subtype == 'pcs':
            return f"[Check the {self.pcsRestraints}th row of pseudocontact shift restraints] "
        if self.__cur_subtype == 'noepk':
            return f"[Check the {self.noepkRestraints}th row of NOESY volume restraints] "
        if self.__cur_subtype == 'jcoup':
            return f"[Check the {self.jcoupRestraints}th row of scalar coupling constant restraints] "
        if self.__cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of coordinate geometry restraints] "
        if self.__cur_subtype == 'hbond':
            return f"[Check the {self.hbondRestraints}th row of hydrogen bond restraints] "
        if self.__cur_subtype == 'ssbond':
            return f"[Check the {self.ssbondRestraints}th row of disulfide bond restraints] "
        if self.__cur_subtype == 'fchiral':
            return f"[Check the {self.fchiralRestraints}th row of floating chiral stereo assignments] "
        return ''

    def __setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        if self.__cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.distRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.dihedRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'rdc':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.rdcRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'pcs':
            self.reasonsForReParsing['loca_seq_scheme'][(self.__cur_subtype, self.pcsRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'noepk':
            self.reasonsForReParsing['loca_seq_scheme'][(self.__cur_subtype, self.noepkRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'jcoup':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.jcoupRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.geoRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'hbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.hbondRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'ssbond':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.ssbondRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'fchiral':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.fchiralRestraints)] = self.__preferAuthSeq
        if not self.__preferAuthSeq:
            self.__preferLabelSeqCount += 1
            if self.__preferLabelSeqCount > MAX_PREF_LABEL_SCHEME_COUNT:
                self.reasonsForReParsing['label_seq_scheme'] = True

    def __retrieveLocalSeqScheme(self):
        if self.__reasons is None or 'local_seq_scheme' not in self.__reasons:
            return
        if 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
            self.__preferAuthSeq = False
            self.__authSeqId = 'label_seq_id'
            return
        if self.__cur_subtype == 'dist':
            key = (self.__cur_subtype, self.distRestraints)
        elif self.__cur_subtype == 'dihed':
            key = (self.__cur_subtype, self.dihedRestraints)
        elif self.__cur_subtype == 'rdc':
            key = (self.__cur_subtype, self.rdcRestraints)
        elif self.__cur_subtype == 'pcs':
            key = (self.__cur_subtype, self.pcsRestraints)
        elif self.__cur_subtype == 'noepk':
            key = (self.__cur_subtype, self.noepkRestraints)
        elif self.__cur_subtype == 'jcoup':
            key = (self.__cur_subtype, self.jcoupRestraints)
        elif self.__cur_subtype == 'geo':
            key = (self.__cur_subtype, self.geoRestraints)
        elif self.__cur_subtype == 'hbond':
            key = (self.__cur_subtype, self.hbondRestraints)
        elif self.__cur_subtype == 'ssbond':
            key = (self.__cur_subtype, self.ssbondRestraints)
        elif self.__cur_subtype == 'fchiral':
            key = (self.__cur_subtype, self.fchiralRestraints)
        else:
            return

        if key in self.__reasons['local_seq_scheme']:
            self.__preferAuthSeq = self.__reasons['local_seq_scheme'][key]

    def __addSf(self, constraintType=None):
        _subtype = getValidSubType(self.__cur_subtype)

        if _subtype is None:
            return

        self.__listIdCounter = incListIdCounter(self.__cur_subtype, self.__listIdCounter)

        key = (self.__cur_subtype, constraintType, None)

        if key not in self.sfDict:
            self.sfDict[key] = []

        list_id = self.__listIdCounter[self.__cur_subtype]

        sf_framecode = 'CYANA_' + getRestraintName(self.__cur_subtype).replace(' ', '_') + str(list_id)

        sf = getSaveframe(self.__cur_subtype, sf_framecode, list_id, self.__entryId, self.__originalFileName,
                          constraintType)

        not_valid = True

        lp = getLoop(self.__cur_subtype)
        if not isinstance(lp, dict):
            sf.add_loop(lp)
            not_valid = False

        item = {'saveframe': sf, 'loop': lp, 'list_id': list_id,
                'id': 0, 'index_id': 0}

        if not_valid:
            item['tags'] = []

        self.sfDict[key].append(item)

    def __getSf(self, constraintType=None):
        key = (self.__cur_subtype, constraintType, None)

        if key not in self.sfDict:
            self.__addSf(constraintType)

        return self.sfDict[key][-1]

    def getContentSubtype(self):
        """ Return content subtype of CYANA MR file.
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints,
                          'noepk_restraint': self.noepkRestraints,
                          'jcoup_restraint': self.jcoupRestraints,
                          'geo_restraint': self.geoRestraints,
                          'hbond_restraint': self.hbondRestraints,
                          'ssbond_restraint': self.ssbondRestraints,
                          'fchiral_restraint': self.fchiralRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getEffectiveContentSubtype(self):
        """ Return effective content subtype of CYANA MR file (excluding .upv, lov, and .cco).
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'rdc_restraint': self.rdcRestraints,
                          'pcs_restraint': self.pcsRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getPolymerSequence(self):
        """ Return polymer sequence of CYANA MR file.
        """
        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self):
        """ Return sequence alignment between coordinates and CYANA MR.
        """
        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self):
        """ Return chain assignment between coordinates and CYANA MR.
        """
        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self):
        """ Return reasons for re-parsing CYANA MR file.
        """
        return None if len(self.reasonsForReParsing) == 0 else self.reasonsForReParsing

    def getTypeOfDistanceRestraints(self):
        """ Return type of distance restraints of the CYANA MR file.
        """
        if self.__file_ext is not None:
            if self.__file_ext in ('upl', 'lol'):
                return self.__file_ext

        if len(self.__local_dist_types) > 0:
            if 'upl' in self.__local_dist_types and 'lol' not in self.__local_dist_types:
                return 'upl'
            if 'lol' in self.__local_dist_types and 'upl' not in self.__local_dist_types:
                return 'lol'
            return 'both'

        if self.__max_dist_value == DIST_ERROR_MIN:
            return ''

        if self.__max_dist_value > 3.5 and self.__min_dist_value > 2.7:
            return 'upl'
        if self.__max_dist_value < 2.7:
            return 'lol'

        return 'both'

    def getListIdCounter(self):
        """ Return updated list id counter.
        """
        return None if len(self.__listIdCounter) == 0 else self.__listIdCounter

    def getSfDict(self):
        """ Return a dictionary of pynmrstar saveframes.
        """
        return None if len(self.sfDict) == 0 else self.sfDict

# del CyanaMRParser
