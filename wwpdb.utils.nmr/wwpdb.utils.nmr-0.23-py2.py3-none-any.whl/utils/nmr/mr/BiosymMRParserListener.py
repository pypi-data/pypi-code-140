##
# File: BiosymMRParserListener.py
# Date: 17-May-2022
#
# Updates:
# Generated from BiosymMRParser.g4 by ANTLR 4.11.1
""" ParserLister class for BIOSYM MR files.
    @author: Masashi Yokochi
"""
import sys
import itertools
import numpy

from antlr4 import ParseTreeListener

try:
    from wwpdb.utils.align.alignlib import PairwiseAlign  # pylint: disable=no-name-in-module
    from wwpdb.utils.nmr.mr.BiosymMRParser import BiosymMRParser
    from wwpdb.utils.nmr.mr.ParserListenerUtil import (checkCoordinates,
                                                       extendCoordinatesForExactNoes,
                                                       getTypeOfDihedralRestraint,
                                                       translateToStdResName,
                                                       translateToStdAtomName,
                                                       isCyclicPolymer,
                                                       getRestraintName,
                                                       getValidSubType,
                                                       incListIdCounter,
                                                       getSaveframe,
                                                       getLoop,
                                                       getRow,
                                                       REPRESENTATIVE_MODEL_ID,
                                                       MAX_PREF_LABEL_SCHEME_COUNT,
                                                       THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                                       DIST_RESTRAINT_RANGE,
                                                       DIST_RESTRAINT_ERROR,
                                                       ANGLE_RESTRAINT_RANGE,
                                                       ANGLE_RESTRAINT_ERROR)
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
    from nmr.mr.BiosymMRParser import BiosymMRParser
    from nmr.mr.ParserListenerUtil import (checkCoordinates,
                                           extendCoordinatesForExactNoes,
                                           getTypeOfDihedralRestraint,
                                           translateToStdResName,
                                           translateToStdAtomName,
                                           isCyclicPolymer,
                                           getRestraintName,
                                           getValidSubType,
                                           incListIdCounter,
                                           getSaveframe,
                                           getLoop,
                                           getRow,
                                           REPRESENTATIVE_MODEL_ID,
                                           MAX_PREF_LABEL_SCHEME_COUNT,
                                           THRESHHOLD_FOR_CIRCULAR_SHIFT,
                                           DIST_RESTRAINT_RANGE,
                                           DIST_RESTRAINT_ERROR,
                                           ANGLE_RESTRAINT_RANGE,
                                           ANGLE_RESTRAINT_ERROR)
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


# This class defines a complete listener for a parse tree produced by BiosymMRParser.
class BiosymMRParserListener(ParseTreeListener):

    # __verbose = None
    # __lfh = None
    __debug = False

    __createSfDict = False
    __omitDistLimitOutlier = True
    __allowZeroUpperLimit = False
    __correctCircularShift = True

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

    # CIF reader
    __cR = None
    __hasCoord = False

    # data item name for model ID in 'atom_site' category
    __modelNumName = None

    # data item names for auth_asym_id, auth_seq_id, auth_atom_id in 'atom_site' category
    # __authAsymId = None
    # __authSeqId = None
    # __authAtomId = None
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

    # chain number dictionary
    __chainNumberDict = None

    # polymer sequence of MR file
    __polySeqRst = None

    __seqAlign = None
    __chainAssign = None

    # current restraint subtype
    __cur_subtype = ''

    # collection of atom selection
    atomSelectionSet = []

    # collection of number selection
    numberSelection = []

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
                 reasons=None):
        # self.__verbose = verbose
        # self.__lfh = loga

        self.__representativeModelId = representativeModelId
        self.__mrAtomNameMapping = None if mrAtomNameMapping is None or len(mrAtomNameMapping) == 0 else mrAtomNameMapping

        self.__cR = cR
        self.__hasCoord = cR is not None

        if self.__hasCoord:
            ret = checkCoordinates(verbose, log, representativeModelId, cR, cC)
            self.__modelNumName = ret['model_num_name']
            # self.__authAsymId = ret['auth_asym_id']
            # self.__authSeqId = ret['auth_seq_id']
            # self.__authAtomId = ret['auth_atom_id']
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

        self.distRestraints = 0      # BIOSYM: Distance restraints
        self.dihedRestraints = 0     # BIOSYM: Dihedral angle restraints
        self.geoRestraints = 0       # BIOSYM: Chirality/prochirality constraints

    def setDebugMode(self, debug):
        self.__debug = debug

    def createSfDict(self, createSfDict):
        self.__createSfDict = createSfDict

    def setOriginaFileName(self, originalFileName):
        self.__originalFileName = originalFileName

    def setListIdCounter(self, listIdCounter):
        self.__listIdCounter = listIdCounter

    def setEntryId(self, entryId):
        self.__entryId = entryId

    # Enter a parse tree produced by BiosymMRParser#biosym_mr.
    def enterBiosym_mr(self, ctx: BiosymMRParser.Biosym_mrContext):  # pylint: disable=unused-argument
        self.__chainNumberDict = {}
        self.__polySeqRst = []

    # Exit a parse tree produced by BiosymMRParser#biosym_mr.
    def exitBiosym_mr(self, ctx: BiosymMRParser.Biosym_mrContext):  # pylint: disable=unused-argument
        if self.__hasPolySeq and self.__polySeqRst is not None:
            sortPolySeqRst(self.__polySeqRst,
                           None if self.__reasons is None or 'non_poly_remap' not in self.__reasons else self.__reasons['non_poly_remap'])

            file_type = 'nm-res-bio'

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

    # Enter a parse tree produced by BiosymMRParser#distance_restraints.
    def enterDistance_restraints(self, ctx: BiosymMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

    # Exit a parse tree produced by BiosymMRParser#distance_restraints.
    def exitDistance_restraints(self, ctx: BiosymMRParser.Distance_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#distance_restraint.
    def enterDistance_restraint(self, ctx: BiosymMRParser.Distance_restraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#distance_restraint.
    def exitDistance_restraint(self, ctx: BiosymMRParser.Distance_restraintContext):

        try:

            chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(1)))

            if None in self.numberSelection:
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            # obs_value = self.numberSelection[2]
            weight = self.numberSelection[3]
            # weight_ub = self.numberSelection[4]
            # max_penalty = self.numberSelection[5]

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(chainId2, seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
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

            if dstFunc is None:
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

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by BiosymMRParser#distance_constraints.
    def enterDistance_constraints(self, ctx: BiosymMRParser.Distance_constraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dist'

    # Exit a parse tree produced by BiosymMRParser#distance_constraints.
    def exitDistance_constraints(self, ctx: BiosymMRParser.Distance_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#distance_constraint.
    def enterDistance_constraint(self, ctx: BiosymMRParser.Distance_constraintContext):  # pylint: disable=unused-argument
        self.distRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#distance_constraint.
    def exitDistance_constraint(self, ctx: BiosymMRParser.Distance_constraintContext):

        try:

            chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(1)))

            if None in self.numberSelection:
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # max_penalty = self.numberSelection[4]

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(chainId2, seqId2, compId2, atomId2)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)

            if len(self.atomSelectionSet) < 2:
                return

            self.__allowZeroUpperLimit = False
            if self.__reasons is not None and 'model_chain_id_ext' in self.__reasons\
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

            if dstFunc is None:
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

        finally:
            self.numberSelection.clear()

    def splitAtomSelectionExpr(self, atomSelection):  # pylint: disable=no-self-use
        """ Split BIOSYM atom selection expression.
        """

        try:

            atomSel = atomSelection.upper().split(':')

            chainId = int(atomSel[0])
            residue = atomSel[1].split('_')
            compId = residue[0]
            try:
                seqId = int(residue[1])
            except ValueError:
                seqId = int(''.join(c for c in residue[1] if c.isdigit()))
                chainId = ''.join(c for c in residue[1] if not c.isdigit())
                if len(chainId) == 0:
                    chainId = None
            atomId = atomSel[2]

            return chainId, seqId, compId, atomId

        except ValueError:
            return None, None, None, None

    def validateDistanceRange(self, weight, target_value, lower_limit, upper_limit, omit_dist_limit_outlier):
        """ Validate distance value range.
        """

        validRange = True
        dstFunc = {'weight': weight}

        if target_value is not None:
            if DIST_ERROR_MIN < target_value < DIST_ERROR_MAX or (target_value == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['target_value'] = f"{target_value}"
            else:
                if target_value <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The target value='{target_value}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    target_value = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The target value='{target_value}' must be within range {DIST_RESTRAINT_ERROR}.\n"

        if lower_limit is not None:
            if DIST_ERROR_MIN <= lower_limit < DIST_ERROR_MAX:
                dstFunc['lower_limit'] = f"{lower_limit}"
            else:
                if lower_limit <= DIST_ERROR_MIN and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    lower_limit = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit}' must be within range {DIST_RESTRAINT_ERROR}.\n"

        if upper_limit is not None:
            if DIST_ERROR_MIN < upper_limit <= DIST_ERROR_MAX or (upper_limit == 0.0 and self.__allowZeroUpperLimit):
                dstFunc['upper_limit'] = f"{upper_limit}"
            else:
                if (upper_limit <= DIST_ERROR_MIN or upper_limit > DIST_ERROR_MAX) and omit_dist_limit_outlier:
                    self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit}' is omitted because it is not within range {DIST_RESTRAINT_ERROR}.\n"
                    upper_limit = None
                else:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The upper limit value='{upper_limit}' must be within range {DIST_RESTRAINT_ERROR}.\n"

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

        else:

            if lower_limit is not None and upper_limit is not None:
                if lower_limit > upper_limit:
                    validRange = False
                    self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                        f"The lower limit value='{lower_limit}' must be less than the upper limit value '{upper_limit}'.\n"

        if not validRange:
            return None

        if target_value is not None:
            if DIST_RANGE_MIN <= target_value <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        if lower_limit is not None:
            if DIST_RANGE_MIN <= lower_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The lower limit value='{lower_limit}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        if upper_limit is not None:
            if DIST_RANGE_MIN <= upper_limit <= DIST_RANGE_MAX:
                pass
            else:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The upper limit value='{upper_limit}' should be within range {DIST_RESTRAINT_RANGE}.\n"

        return dstFunc

    def getRealChainSeqId(self, ps, seqId, compId, isPolySeq=True):
        compId = translateToStdResName(compId)
        # if self.__reasons is not None and 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
        if not self.__preferAuthSeq:
            seqKey = (ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId)
            if seqKey in self.__labelToAuthSeq:
                _chainId, _seqId = self.__labelToAuthSeq[seqKey]
                if _seqId in ps['auth_seq_id']:
                    return _chainId, _seqId
        if seqId in ps['auth_seq_id']:
            idx = ps['auth_seq_id'].index(seqId)
            if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
                return ps['auth_chain_id'], seqId
        # if seqId in ps['seq_id']:
        #     idx = ps['seq_id'].index(seqId)
        #     if compId in (ps['comp_id'][idx], ps['auth_comp_id'][idx]):
        #         return ps['auth_chain_id'], ps['auth_seq_id'][idx]
        return ps['chain_id' if isPolySeq else 'auth_chain_id'], seqId

    def assignCoordPolymerSequence(self, refChainId, seqId, compId, atomId):
        """ Assign polymer sequences of the coordinates.
        """

        chainAssign = []
        _seqId = seqId

        fixedChainId = None
        fixedSeqId = None

        if refChainId is not None:
            if any(ps for ps in self.__polySeq if ps['auth_chain_id'] == refChainId):
                if refChainId not in self.__chainNumberDict:
                    self.__chainNumberDict[refChainId] = refChainId

        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            seqId, compId, _ = retrieveAtomIdentFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

        if self.__reasons is not None:
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
                                    if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                        self.__chainNumberDict[refChainId] = chainId
                            elif len(self.__nefT.get_valid_star_atom(cifCompId, atomId)[0]) > 0:
                                chainAssign.append((chainId, seqId_, cifCompId, True))
                                if refChainId is not None and refChainId != chainId and refChainId not in self.__chainNumberDict:
                                    self.__chainNumberDict[refChainId] = chainId
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
                if refChainId is not None and refChainId != chainId and refChainId in self.__chainNumberDict:
                    if chainId != self.__chainNumberDict[refChainId]:
                        continue
                if fixedChainId is not None and fixedChainId != chainId:
                    continue
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
                return self.assignCoordPolymerSequence(refChainId, seqId, compId, 'H1')
            if seqId < 1 and len(self.__polySeq) == 1:
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{compId}:{atomId} is not present in the coordinates. "\
                    f"The residue number '{_seqId}' is not present in polymer sequence of chain {refChainId} of the coordinates. "\
                    "Please update the sequence in the Macromolecules page.\n"
            else:
                self.warningMessage += f"[Atom not found] {self.__getCurrentRestraint()}"\
                    f"{_seqId}:{compId}:{atomId} is not present in the coordinates.\n"

        return chainAssign

    def selectCoordAtoms(self, chainAssign, seqId, compId, atomId, allowAmbig=True):
        """ Select atoms of the coordinates.
        """

        atomSelection = []

        authAtomId = atomId

        _atomId = atomId
        if self.__mrAtomNameMapping is not None and compId not in monDict3:
            _atomId = retrieveAtomIdFromMRMap(self.__mrAtomNameMapping, seqId, compId, atomId)

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

            seqKey, coordAtomSite = self.getCoordAtomSiteOf(chainId, cifSeqId, self.__hasCoord)
            if atomId != _atomId and coordAtomSite is not None and _atomId in coordAtomSite['atom_id']:
                atomId = _atomId

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
                self.warningMessage += f"[Invalid atom nomenclature] {self.__getCurrentRestraint()}"\
                    f"{seqId}:{compId}:{atomId} is invalid atom nomenclature.\n"
                continue
            if lenAtomId > 1 and not allowAmbig:
                self.warningMessage += f"[Invalid atom selection] {self.__getCurrentRestraint()}"\
                    f"Ambiguous atom selection '{seqId}:{compId}:{atomId}' is not allowed as a angle restraint.\n"
                continue

            for cifAtomId in _atomId:
                atomSelection.append({'chain_id': chainId, 'seq_id': cifSeqId, 'comp_id': cifCompId,
                                      'atom_id': cifAtomId, 'auth_atom_id': authAtomId})

                self.testCoordAtomIdConsistency(chainId, cifSeqId, cifCompId, cifAtomId, seqKey, coordAtomSite)

        if len(atomSelection) > 0:
            self.atomSelectionSet.append(atomSelection)

    def testCoordAtomIdConsistency(self, chainId, seqId, compId, atomId, seqKey, coordAtomSite):
        if not self.__hasCoord:
            return

        found = False

        if coordAtomSite is not None:
            if atomId in coordAtomSite['atom_id']:
                found = True
            elif 'alt_atom_id' in coordAtomSite and atomId in coordAtomSite['alt_atom_id']:
                found = True
                # self.__authAtomId = 'auth_atom_id'

            elif self.__preferAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        # self.__authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        # self.__authSeqId = 'label_seq_id'
                        # self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()

            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        # self.__authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        # self.__authSeqId = 'auth_seq_id'
                        # self.__authAtomId = 'auth_atom_id'
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
                    # self.__authSeqId = 'label_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    self.__preferAuthSeq = False
                    # self.__authSeqId = 'label_seq_id'
                    # self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()

        else:
            self.__preferAuthSeq = True
            _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
            if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                if atomId in _coordAtomSite['atom_id']:
                    found = True
                    # self.__authSeqId = 'auth_seq_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                    found = True
                    # self.__authSeqId = 'auth_seq_id'
                    # self.__authAtomId = 'auth_atom_id'
                    seqKey = _seqKey
                    self.__setLocalSeqScheme()
                else:
                    self.__preferAuthSeq = False
            else:
                self.__preferAuthSeq = False

        if found:
            return

        if chainId in self.__chainNumberDict.values():

            if self.__preferAuthSeq:
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId, asis=False)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        # self.__authSeqId = 'label_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        self.__preferAuthSeq = False
                        # self.__authSeqId = 'label_seq_id'
                        # self.__authAtomId = 'auth_atom_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
            else:
                self.__preferAuthSeq = True
                _seqKey, _coordAtomSite = self.getCoordAtomSiteOf(chainId, seqId)
                if _coordAtomSite is not None and _coordAtomSite['comp_id'] == compId:
                    if atomId in _coordAtomSite['atom_id']:
                        found = True
                        # self.__authSeqId = 'auth_seq_id'
                        seqKey = _seqKey
                        self.__setLocalSeqScheme()
                    elif 'alt_atom_id' in _coordAtomSite and atomId in _coordAtomSite['alt_atom_id']:
                        found = True
                        # self.__authSeqId = 'auth_seq_id'
                        # self.__authAtomId = 'auth_atom_id'
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

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_restraints.
    def enterDihedral_angle_restraints(self, ctx: BiosymMRParser.Dihedral_angle_restraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_restraints.
    def exitDihedral_angle_restraints(self, ctx: BiosymMRParser.Dihedral_angle_restraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_restraint.
    def enterDihedral_angle_restraint(self, ctx: BiosymMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_restraint.
    def exitDihedral_angle_restraint(self, ctx: BiosymMRParser.Dihedral_angle_restraintContext):  # pylint: disable=unused-argument

        try:

            chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
            chainId3, seqId3, compId3, atomId3 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
            chainId4, seqId4, compId4, atomId4 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(3)))

            if None in self.numberSelection:
                return

            # cco = self.numberSelection[0]
            # cco_err = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # weught_max = self.numberSelection[4]

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            target_value = None
            lower_limit = self.numberSelection[5]
            upper_limit = self.numberSelection[6]

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            dstFunc2 = dstFunc3 = dstFunc4 = None

            if len(self.numberSelection) > 8:
                lower_limit2 = self.numberSelection[7]
                upper_limit2 = self.numberSelection[8]

                dstFunc2 = self.validateAngleRange(weight, target_value, lower_limit2, upper_limit2)

            if len(self.numberSelection) > 10:
                lower_limit3 = self.numberSelection[9]
                upper_limit3 = self.numberSelection[10]

                dstFunc3 = self.validateAngleRange(weight, target_value, lower_limit3, upper_limit3)

            if len(self.numberSelection) > 12:
                lower_limit4 = self.numberSelection[11]
                upper_limit4 = self.numberSelection[12]

                dstFunc4 = self.validateAngleRange(weight, target_value, lower_limit4, upper_limit4)

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(chainId2, seqId2, compId2, atomId2)
            chainAssign3 = self.assignCoordPolymerSequence(chainId3, seqId3, compId3, atomId3)
            chainAssign4 = self.assignCoordPolymerSequence(chainId4, seqId4, compId4, atomId4)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0\
               or len(chainAssign3) == 0 or len(chainAssign4) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtoms(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            if not self.areUniqueCoordAtoms('a Dihedral angle'):
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                       [atom1, atom2, atom3, atom4])
                if angleName is None:
                    continue
                if self.__debug:
                    _dstFunc = f"{dstFunc}"
                    if dstFunc2 is not None:
                        _dstFunc += f" {dstFunc2}"
                    if dstFunc3 is not None:
                        _dstFunc += f" {dstFunc3}"
                    if dstFunc4 is not None:
                        _dstFunc += f" {dstFunc4}"
                    print(f"subtype={self.__cur_subtype} id={self.dihedRestraints} angleName={angleName} "
                          f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} {_dstFunc}")
                if self.__createSfDict and sf is not None:
                    sf['index_id'] += 1
                    row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                 '.' if dstFunc2 is None else 1, angleName,
                                 sf['list_id'], self.__entryId, dstFunc, atom1, atom2, atom3, atom4)
                    sf['loop'].add_data(row)
                    if dstFunc2 is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     2, angleName,
                                     sf['list_id'], self.__entryId, dstFunc2, atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)
                    if dstFunc3 is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     3, angleName,
                                     sf['list_id'], self.__entryId, dstFunc3, atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)
                    if dstFunc4 is not None:
                        sf['index_id'] += 1
                        row = getRow(self.__cur_subtype, sf['id'], sf['index_id'],
                                     4, angleName,
                                     sf['list_id'], self.__entryId, dstFunc4, atom1, atom2, atom3, atom4)
                        sf['loop'].add_data(row)

        finally:
            self.numberSelection.clear()

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_constraints.
    def enterDihedral_angle_constraints(self, ctx: BiosymMRParser.Dihedral_angle_constraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'dihed'

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_constraints.
    def exitDihedral_angle_constraints(self, ctx: BiosymMRParser.Dihedral_angle_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#dihedral_angle_constraint.
    def enterDihedral_angle_constraint(self, ctx: BiosymMRParser.Dihedral_angle_constraintContext):  # pylint: disable=unused-argument
        self.dihedRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#dihedral_angle_constraint.
    def exitDihedral_angle_constraint(self, ctx: BiosymMRParser.Dihedral_angle_constraintContext):  # pylint: disable=unused-argument

        try:

            chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
            chainId2, seqId2, compId2, atomId2 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
            chainId3, seqId3, compId3, atomId3 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
            chainId4, seqId4, compId4, atomId4 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(3)))

            if None in self.numberSelection:
                return

            target_value = None
            lower_limit = self.numberSelection[0]
            upper_limit = self.numberSelection[1]
            weight = self.numberSelection[2]
            # weight_ub = self.numberSelection[3]
            # weught_max = self.numberSelection[4]

            if weight < 0.0:
                self.warningMessage += f"[Invalid data] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' must not be a negative value.\n"
                return
            if weight == 0.0:
                self.warningMessage += f"[Range value warning] {self.__getCurrentRestraint()}"\
                    f"The relative weight value of '{weight}' should be a positive value.\n"

            dstFunc = self.validateAngleRange(weight, target_value, lower_limit, upper_limit)

            if dstFunc is None:
                return

            if not self.__hasPolySeq:
                return

            self.__retrieveLocalSeqScheme()

            chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)
            chainAssign2 = self.assignCoordPolymerSequence(chainId2, seqId2, compId2, atomId2)
            chainAssign3 = self.assignCoordPolymerSequence(chainId3, seqId3, compId3, atomId3)
            chainAssign4 = self.assignCoordPolymerSequence(chainId4, seqId4, compId4, atomId4)

            if len(chainAssign1) == 0 or len(chainAssign2) == 0\
               or len(chainAssign3) == 0 or len(chainAssign4) == 0:
                return

            self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1, False)
            self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2, False)
            self.selectCoordAtoms(chainAssign3, seqId3, compId3, atomId3, False)
            self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)

            if len(self.atomSelectionSet) < 4:
                return

            if not self.areUniqueCoordAtoms('a Dihedral angle'):
                return

            if self.__createSfDict:
                sf = self.__getSf()
                sf['id'] += 1

            compId = self.atomSelectionSet[0][0]['comp_id']
            peptide, nucleotide, carbohydrate = self.__csStat.getTypeOfCompId(compId)

            for atom1, atom2, atom3, atom4 in itertools.product(self.atomSelectionSet[0],
                                                                self.atomSelectionSet[1],
                                                                self.atomSelectionSet[2],
                                                                self.atomSelectionSet[3]):
                angleName = getTypeOfDihedralRestraint(peptide, nucleotide, carbohydrate,
                                                       [atom1, atom2, atom3, atom4])
                if angleName is None:
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
                dstFunc['target_value'] = f"{target_value}"
            else:
                validRange = False
                self.warningMessage += f"[Range value error] {self.__getCurrentRestraint()}"\
                    f"The target value='{target_value}' must be within range {ANGLE_RESTRAINT_ERROR}.\n"

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
                    f"The target value='{target_value}' should be within range {ANGLE_RESTRAINT_RANGE}.\n"

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

    # Enter a parse tree produced by BiosymMRParser#chirality_constraints.
    def enterChirality_constraints(self, ctx: BiosymMRParser.Chirality_constraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by BiosymMRParser#chirality_constraints.
    def exitChirality_constraints(self, ctx: BiosymMRParser.Chirality_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#chirality_constraint.
    def enterChirality_constraint(self, ctx: BiosymMRParser.Chirality_constraintContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#chirality_constraint.
    def exitChirality_constraint(self, ctx: BiosymMRParser.Chirality_constraintContext):
        chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection()))

        chirality = str(ctx.Chiral_code())

        if not self.__hasPolySeq:
            return

        self.__retrieveLocalSeqScheme()

        chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)

        if len(chainAssign1) == 0:
            return

        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)

        if len(self.atomSelectionSet) < 2:
            return

        if not self.areUniqueCoordAtoms('a Chirality'):
            return

        if self.__createSfDict:
            sf = self.__getSf('BIOSYM chirality constraint')
            sf['id'] += 1
            if len(sf['loop']['tag']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id', 'auth_seq_id', 'auth_comp_id', 'auth_atom_id',
                                      'chirality',
                                      'list_id', 'entry_id']

        for atom1 in self.atomSelectionSet[0]:
            if self.__debug:
                print(f"subtype={self.__cur_subtype} id={self.geoRestraints} "
                      f"atom={atom1} chirality={chirality}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           chirality,
                                           sf['list_id'], self.__entryId])

    # Enter a parse tree produced by BiosymMRParser#prochirality_constraints.
    def enterProchirality_constraints(self, ctx: BiosymMRParser.Prochirality_constraintsContext):  # pylint: disable=unused-argument
        self.__cur_subtype = 'geo'

    # Exit a parse tree produced by BiosymMRParser#prochirality_constraints.
    def exitProchirality_constraints(self, ctx: BiosymMRParser.Prochirality_constraintsContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#prochirality_constraint.
    def enterProchirality_constraint(self, ctx: BiosymMRParser.Prochirality_constraintContext):  # pylint: disable=unused-argument
        self.geoRestraints += 1

        self.atomSelectionSet.clear()

    # Exit a parse tree produced by BiosymMRParser#prochirality_constraint.
    def exitProchirality_constraint(self, ctx: BiosymMRParser.Prochirality_constraintContext):
        chainId1, seqId1, compId1, atomId1 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(0)))
        chainId2, seqId2, compId2, atomId2 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(1)))
        chainId3, seqId3, compId3, atomId3 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(2)))
        chainId4, seqId4, compId4, atomId4 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(3)))
        chainId5, seqId5, compId5, atomId5 = self.splitAtomSelectionExpr(str(ctx.Atom_selection(4)))

        if not self.__hasPolySeq:
            return

        self.__retrieveLocalSeqScheme()

        chainAssign1 = self.assignCoordPolymerSequence(chainId1, seqId1, compId1, atomId1)
        chainAssign2 = self.assignCoordPolymerSequence(chainId2, seqId2, compId2, atomId2)
        chainAssign3 = self.assignCoordPolymerSequence(chainId3, seqId3, compId3, atomId3)
        chainAssign4 = self.assignCoordPolymerSequence(chainId4, seqId4, compId4, atomId4)
        chainAssign5 = self.assignCoordPolymerSequence(chainId5, seqId5, compId5, atomId5)

        if len(chainAssign1) == 0 or len(chainAssign2) == 0\
           or len(chainAssign3) == 0 or len(chainAssign4) == 0\
           or len(chainAssign5) == 0:
            return

        self.selectCoordAtoms(chainAssign1, seqId1, compId1, atomId1)
        self.selectCoordAtoms(chainAssign2, seqId2, compId2, atomId2)
        self.selectCoordAtoms(chainAssign3, seqId3, compId3, atomId3, False)
        self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)
        self.selectCoordAtoms(chainAssign4, seqId4, compId4, atomId4, False)

        if len(self.atomSelectionSet) < 5:
            return

        if self.__createSfDict:
            sf = self.__getSf('BIOSYM prochirality constraint')
            sf['id'] += 1
            if len(sf['loop']['tag']) == 0:
                sf['loop']['tags'] = ['index_id', 'id',
                                      'auth_asym_id_1', 'auth_seq_id_1', 'auth_comp_id_1', 'auth_atom_id_1',
                                      'auth_asym_id_2', 'auth_seq_id_2', 'auth_comp_id_2', 'auth_atom_id_2',
                                      'auth_asym_id_3', 'auth_seq_id_3', 'auth_comp_id_3', 'auth_atom_id_3',
                                      'auth_asym_id_4', 'auth_seq_id_4', 'auth_comp_id_4', 'auth_atom_id_4',
                                      'auth_asym_id_5', 'auth_seq_id_5', 'auth_comp_id_5', 'auth_atom_id_5',
                                      'list_id', 'entry_id']

        for atom1, atom2, atom3, atom4, atom5 in itertools.product(self.atomSelectionSet[0],
                                                                   self.atomSelectionSet[1],
                                                                   self.atomSelectionSet[2],
                                                                   self.atomSelectionSet[3],
                                                                   self.atomSelectionSet[4]):
            if self.__debug:
                print(f"subtype={self.__cur_subtype} id={self.geoRestraints} "
                      f"atom1={atom1} atom2={atom2} atom3={atom3} atom4={atom4} atom5={atom5}")
            if self.__createSfDict and sf is not None:
                sf['index_id'] += 1
                sf['loop']['data'].append([sf['index_id'], sf['id'],
                                           atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id'],
                                           atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id'],
                                           atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id'],
                                           atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id'],
                                           atom5['chain_id'], atom5['seq_id'], atom5['comp_id'], atom5['atom_id'],
                                           sf['list_id'], self.__entryId])

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

    # Enter a parse tree produced by BiosymMRParser#mixing_time.
    def enterMixing_time(self, ctx: BiosymMRParser.Mixing_timeContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#mixing_time.
    def exitMixing_time(self, ctx: BiosymMRParser.Mixing_timeContext):  # pylint: disable=unused-argument
        pass

    # Enter a parse tree produced by BiosymMRParser#number.
    def enterNumber(self, ctx: BiosymMRParser.NumberContext):  # pylint: disable=unused-argument
        pass

    # Exit a parse tree produced by BiosymMRParser#number.
    def exitNumber(self, ctx: BiosymMRParser.NumberContext):
        if ctx.Float():
            self.numberSelection.append(float(str(ctx.Float())))

        elif ctx.Integer():
            self.numberSelection.append(float(str(ctx.Integer())))

        else:
            self.numberSelection.append(None)

    def __getCurrentRestraint(self):
        if self.__cur_subtype == 'dist':
            return f"[Check the {self.distRestraints}th row of distance restraints] "
        if self.__cur_subtype == 'dihed':
            return f"[Check the {self.dihedRestraints}th row of dihedral angle restraints] "
        if self.__cur_subtype == 'geo':
            return f"[Check the {self.geoRestraints}th row of chirality/prochirality restraints] "
        return ''

    def __setLocalSeqScheme(self):
        if 'local_seq_scheme' not in self.reasonsForReParsing:
            self.reasonsForReParsing['local_seq_scheme'] = {}
        if self.__cur_subtype == 'dist':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.distRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'dihed':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.dihedRestraints)] = self.__preferAuthSeq
        elif self.__cur_subtype == 'geo':
            self.reasonsForReParsing['local_seq_scheme'][(self.__cur_subtype, self.geoRestraints)] = self.__preferAuthSeq
        if not self.__preferAuthSeq:
            self.__preferLabelSeqCount += 1
            if self.__preferLabelSeqCount > MAX_PREF_LABEL_SCHEME_COUNT:
                self.reasonsForReParsing['label_seq_scheme'] = True

    def __retrieveLocalSeqScheme(self):
        if self.__reasons is None or 'local_seq_scheme' not in self.__reasons:
            return
        if 'label_seq_scheme' in self.__reasons and self.__reasons['label_seq_scheme']:
            self.__preferAuthSeq = False
            # self.__authSeqId = 'label_seq_id'
            return
        if self.__cur_subtype == 'dist':
            key = (self.__cur_subtype, self.distRestraints)
        elif self.__cur_subtype == 'dihed':
            key = (self.__cur_subtype, self.dihedRestraints)
        elif self.__cur_subtype == 'geo':
            key = (self.__cur_subtype, self.geoRestraints)
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

        sf_framecode = 'BIOSYM_' + getRestraintName(self.__cur_subtype).replace(' ', '_') + str(list_id)

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
        """ Return content subtype of BIOSYM MR file.
        """

        contentSubtype = {'dist_restraint': self.distRestraints,
                          'dihed_restraint': self.dihedRestraints,
                          'geo_restraint': self.geoRestraints
                          }

        return {k: 1 for k, v in contentSubtype.items() if v > 0}

    def getPolymerSequence(self):
        """ Return polymer sequence of BIOSYM MR file.
        """
        return None if self.__polySeqRst is None or len(self.__polySeqRst) == 0 else self.__polySeqRst

    def getSequenceAlignment(self):
        """ Return sequence alignment between coordinates and BIOSYM MR.
        """
        return None if self.__seqAlign is None or len(self.__seqAlign) == 0 else self.__seqAlign

    def getChainAssignment(self):
        """ Return chain assignment between coordinates and BIOSYM MR.
        """
        return None if self.__chainAssign is None or len(self.__chainAssign) == 0 else self.__chainAssign

    def getReasonsForReparsing(self):
        """ Return reasons for re-parsing BIOSYM MR file.
        """
        return None if len(self.reasonsForReParsing) == 0 else self.reasonsForReParsing

    def getListIdCounter(self):
        """ Return updated list id counter.
        """
        return None if len(self.__listIdCounter) == 0 else self.__listIdCounter

    def getSfDict(self):
        """ Return a dictionary of pynmrstar saveframes.
        """
        return None if len(self.sfDict) == 0 else self.sfDict

# del BiosymMRParser
