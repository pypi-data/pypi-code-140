##
# File: ParserListenerUtil.py
# Date: 18-Feb-2022
#
# Updates:
""" Utilities for MR/PT parser listener.
    @author: Masashi Yokochi
"""
import sys
import re
import copy
import collections
import itertools

import numpy

import pynmrstar

try:
    from wwpdb.utils.nmr.AlignUtil import (monDict3,
                                           MAJOR_ASYM_ID_SET,
                                           LEN_MAJOR_ASYM_ID_SET)
except ImportError:
    from nmr.AlignUtil import (monDict3,
                               MAJOR_ASYM_ID_SET,
                               LEN_MAJOR_ASYM_ID_SET)


MAX_ERROR_REPORT = 1
MAX_ERR_LINENUM_REPORT = 20

# isotope numbers of NMR observable nucleus
ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS = {'H': [1, 2, 3],
                                   'C': [13],
                                   'N': [15, 14],
                                   'O': [17],
                                   'P': [31],
                                   'S': [33],
                                   'F': [19],
                                   'CD': [113, 111],
                                   'CA': [43]
                                   }


# nucleus with half spin
HALF_SPIN_NUCLEUS = ('H', 'C', 'N', 'P', 'F', 'CD')


# allowed BMRB ambiguity codes
ALLOWED_AMBIGUITY_CODES = (1, 2, 3, 4, 5, 6, 9)


ALLOWED_ISOTOPE_NUMBERS = []
for isotopeNums in ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.values():
    ALLOWED_ISOTOPE_NUMBERS.extend(isotopeNums)

REPRESENTATIVE_MODEL_ID = 1


MAX_PREF_LABEL_SCHEME_COUNT = 100


THRESHHOLD_FOR_CIRCULAR_SHIFT = 340


DIST_RESTRAINT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 101.0}
DIST_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 150.0}


ANGLE_RESTRAINT_RANGE = {'min_inclusive': -330.0, 'max_inclusive': 330.0}
ANGLE_RESTRAINT_ERROR = {'min_exclusive': -360.0, 'max_exclusive': 360.0}


RDC_RESTRAINT_RANGE = {'min_inclusive': -100.0, 'max_inclusive': 100.0}
RDC_RESTRAINT_ERROR = {'min_exclusive': -200.0, 'max_exclusive': 200.0}


CS_RESTRAINT_RANGE = {'min_inclusive': -300.0, 'max_inclusive': 300.0}
CS_RESTRAINT_ERROR = {'min_exclusive': -999.0, 'max_exclusive': 999.0}


CSA_RESTRAINT_RANGE = {'min_inclusive': -300.0, 'max_inclusive': 300.0}
CSA_RESTRAINT_ERROR = {'min_exclusive': -999.0, 'max_exclusive': 999.0}


PCS_RESTRAINT_RANGE = {'min_inclusive': -20.0, 'max_inclusive': 20.0}
PCS_RESTRAINT_ERROR = {'min_exclusive': -40.0, 'max_exclusive': 40.0}


CCR_RESTRAINT_RANGE = {'min_inclusive': -10.0, 'max_inclusive': 10.0}
CCR_RESTRAINT_ERROR = {'min_exclusive': -20.0, 'max_exclusive': 20.0}


PRE_RESTRAINT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 20.0}
PRE_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 40.0}


T1T2_RESTRAINT_RANGE = {'min_inclusive': 1.0, 'max_inclusive': 20.0}
T1T2_RESTRAINT_ERROR = {'min_exclusive': 0.0, 'max_exclusive': 100.0}


CS_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 3.0}

DIST_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 5.0}

ANGLE_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 90.0}

RDC_UNCERTAINTY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 5.0}

WEIGHT_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 100.0}

SCALE_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 100.0}

PROBABILITY_RANGE = {'min_inclusive': 0.0, 'max_inclusive': 1.0}

# @see: https://x3dna.org/highlights/torsion-angles-of-nucleic-acid-structures for nucleic acids
KNOWN_ANGLE_ATOM_NAMES = {'PHI': ['C', 'N', 'CA', 'C'],  # i-1, i, i, i
                          'PSI': ['N', 'CA', 'C', 'N'],  # i, i, i, i+1
                          'OMEGA': ['CA', 'C', 'N', 'CA'],  # i, i, i+1, i+1; modified CYANA definition [O C N (H or CD for Proline residue)]
                          'CHI1': ['N', 'CA', 'CB', re.compile(r'^[COS]G1?$')],
                          'CHI2': ['CA', 'CB', re.compile(r'^CG1?$'), re.compile(r'^[CNOS]D1?$')],
                          'CHI3': ['CB', 'CG', re.compile(r'^[CS]D$'), re.compile(r'^[CNO]E1?$')],
                          'CHI4': ['CG', 'CD', re.compile(r'^[CN]E$'), re.compile(r'^[CN]Z$')],
                          'CHI5': ['CD', 'NE', 'CZ', 'NH1'],
                          'CHI21': ['CA', 'CB', re.compile(r'^[CO]G1$'), re.compile(r'^CD1|HG11?$')],  # ILE: (CG1, CD1), THR: (OG1, HG1), VAL: (CD1, HG11)
                          'CHI22': ['CA', 'CB', 'CG2', 'HG21'],  # ILE or THR or VAL
                          'CHI31': ['CB', re.compile(r'^CG1?$'), 'CD1', 'HD11'],  # ILE: CG1, LEU: CG
                          'CHI32': ['CB', 'CG', re.compile(r'^[CO]D2$'), re.compile(r'^HD21?$')],  # ASP: (OD2, HD2), LEU: (CD2, HD21)
                          'CHI42': ['CG', 'CD', 'OE2', 'HE2'],  # GLU
                          'ALPHA': ["O3'", 'P', "O5'", "C5'"],  # i-1, i, i, i
                          'BETA': ['P', "O5'", "C5'", "C4'"],
                          'GAMMA': ["O5'", "C5'", "C4'", "C3'"],
                          'DELTA': ["C5'", "C4'", "C3'", "O3'"],
                          'EPSILON': ["C4'", "C3'", "O3'", 'P'],  # i, i, i, i+1
                          'ZETA': ["C3'", "O3'", 'P', "O5'"],  # i, i, i+1, i+1
                          # aka. CHIN (nucleic CHI angle)
                          'CHI': {'Y': ["O4'", "C1'", 'N1', 'C2'],  # for pyrimidines (i.e. C, T, U) N1/3
                                  'R': ["O4'", "C1'", 'N9', 'C4']  # for purines (i.e. G, A) N1/3/7/9
                                  },
                          'ETA': ["C4'", 'P', "C4'", 'P'],  # i-1, i, i, i+1
                          'THETA': ['P', "C4'", 'P', "C4'"],  # i, i, i+1, i+1
                          "ETA'": ["C1'", 'P', "C1'", 'P'],  # i-1, i, i, i+1
                          "THETA'": ['P', "C1'", 'P', "C1'"],  # i, i, i+1, i+1
                          'NU0': ["C4'", "O4'", "C1'", "C2'"],
                          'NU1': ["O4'", "C1'", "C2'", "C3'"],
                          'NU2': ["C1'", "C2'", "C3'", "C4'"],
                          'NU3': ["C2'", "C3'", "C4'", "O4'"],
                          'NU4': ["C3'", "C4'", "O4'", "C1'"],
                          'TAU0': ["C4'", "O4'", "C1'", "C2'"],  # identical to NU0
                          'TAU1': ["O4'", "C1'", "C2'", "C3'"],  # identical to NU1
                          'TAU2': ["C1'", "C2'", "C3'", "C4'"],  # identical to NU2
                          'TAU3': ["C2'", "C3'", "C4'", "O4'"],  # identical to NU3
                          'TAU4': ["C3'", "C4'", "O4'", "C1'"],  # identical to NU4
                          'PPA': ["C1'", "C2'", "C3'", "C4'", "O4'"]  # phase angle of pseudorotation made up from five NU[0-4] dihedral angles
                          }

# @see: http://dx.doi.org/10.1107/S0907444909001905
KNOWN_ANGLE_CARBO_ATOM_NAMES = {'PHI': [re.compile(r'^H1|O5$'), 'C1', 'O1', re.compile(r'^C[46]$')],
                                'PSI': ['C1', 'O1', re.compile(r'^C[46]$'), re.compile(r'^H4|C[35]$')],
                                'OMEGA': ['O1', 'C6', 'C5', re.compile('^H5|C4|O5$')]}

KNOWN_ANGLE_NAMES = KNOWN_ANGLE_ATOM_NAMES.keys()

KNOWN_ANGLE_SEQ_OFFSET = {'PHI': [-1, 0, 0, 0],  # i-1, i, i, i
                          'PSI': [0, 0, 0, 1],  # i, i, i, i+1
                          'OMEGA': [0, 0, 1, 1],  # i, i, i+1, i+1; modified CYANA definition [O C N (H or CD for Proline residue)]
                          'CHI1': [0] * 4,
                          'CHI2': [0] * 4,
                          'CHI3': [0] * 4,
                          'CHI4': [0] * 4,
                          'CHI5': [0] * 4,
                          'CHI21': [0] * 4,  # ILE: (CG1, CD1), THR: (OG1, HG1), VAL: (CD1, HG11)
                          'CHI22': [0] * 4,  # ILE or THR or VAL
                          'CHI31': [0] * 4,  # ILE: CG1, LEU: CG
                          'CHI32': [0] * 4,  # ASP: (OD2, HD2), LEU: (CD2, HD21)
                          'CHI42': [0] * 4,  # GLU
                          'ALPHA': [-1, 0, 0, 0],  # i-1, i, i, i
                          'BETA': [0] * 4,
                          'GAMMA': [0] * 4,
                          'DELTA': [0] * 4,
                          'EPSILON': [0, 0, 0, 1],  # i, i, i, i+1
                          'ZETA': [0, 0, 1, 1],  # i, i, i+1, i+1
                          # aka. CHIN (nucleic CHI angle)
                          'CHI': {'Y': [0] * 4,  # for pyrimidines (i.e. C, T, U) N1/3
                                  'R': [0] * 4  # for purines (i.e. G, A) N1/3/7/9
                                  },
                          'ETA': [-1, 0, 0, 1],  # i-1, i, i, i+1
                          'THETA': [0, 0, 1, 1],  # i, i, i+1, i+1
                          "ETA'": [-1, 0, 0, 1],  # i-1, i, i, i+1
                          "THETA'": [0, 0, 1, 1],  # i, i, i+1, i+1
                          'NU0': [0] * 4,
                          'NU1': [0] * 4,
                          'NU2': [0] * 4,
                          'NU3': [0] * 4,
                          'NU4': [0] * 4,
                          'TAU0': [0] * 4,  # identical to NU0
                          'TAU1': [0] * 4,  # identical to NU1
                          'TAU2': [0] * 4,  # identical to NU2
                          'TAU3': [0] * 4,  # identical to NU3
                          'TAU4': [0] * 4,  # identical to NU4
                          'PPA': [0] * 5  # phase angle of pseudorotation made up from five NU[0-4] dihedral angles
                          }

KNOWN_ANGLE_CARBO_SEQ_OFFSET = {'PHI': [0, 0, 0, -1],  # i, i, i, i-n; for n > 0
                                'PSI': [0, 0, -1, -1],  # i, i, i-n, i-n; for n > 0
                                'OMEGA': [0, -1, -1, -1]  # i, i-n, i-n, i-n; for n > 0
                                }

XPLOR_RDC_PRINCIPAL_AXIS_NAMES = ('OO', 'X', 'Y', 'Z')

XPLOR_ORIGIN_AXIS_COLS = [0, 1, 2, 3]

XPLOR_NITROXIDE_NAMES = ('NO', 'NX')

LEGACY_PDB_RECORDS = ['HEADER', 'OBSLTE', 'TITLE ', 'SPLIT ', 'CAVEAT', 'COMPND', 'SOURCE', 'KEYWDS', 'EXPDAT',
                      'NUMMDL', 'MDLTYP', 'AUTHOR', 'REVDAT', 'SPRSDE', 'JRNL', 'REMARK',
                      'DBREF', 'DBREF1', 'DBREF2', 'SEQADV', 'SEQRES', 'MODRES',
                      'HET ', 'HETNAM', 'HETSYN', 'FORMUL',
                      'HELIX ', 'SHEET ',
                      'SSBOND', 'LINK ', 'CISPEP',
                      'SITE ',
                      'CRYST1', 'ORIGX1', 'ORIGX2', 'ORIGX3', 'SCALE1', 'SCALE2', 'SCALE3',
                      'MTRIX1', 'MTRIX2', 'MTRIX3',
                      'MODEL ', 'ATOM ', 'ANISOU', 'TER ', 'HETATM', 'ENDMDL',
                      'CONECT',
                      'MASTER'
                      ]

CYANA_MR_FILE_EXTS = (None, 'upl', 'lol', 'aco', 'rdc', 'pcs', 'upv', 'lov', 'cco')

NMR_STAR_SF_TAG_PREFIXES = {'dist_restraint': '_Gen_dist_constraint_list',
                            'dihed_restraint': '_Torsion_angle_constraint_list',
                            'rdc_restraint': '_RDC_constraint_list',
                            'noepk_restraint': '_Homonucl_NOE_list',
                            'jcoup_restraint': '_Coupling_constant_list',
                            'csa_restraint': '_Chem_shift_anisotropy',
                            'ddc_restraint': '_Dipolar_coupling_list',
                            'hvycs_restraint': '_CA_CB_constraint_list',
                            'procs_restraint': '_H_chem_shift_constraint_list',
                            'csp_restraint': '_Chem_shift_perturbation_list',
                            'auto_relax_restraint': '_Auto_relaxation_list',
                            'ccr_d_csa_restraint': '_Cross_correlation_D_CSA_list',
                            'ccr_dd_restraint': '_Cross_correlation_DD_list',
                            'fchiral_restraint': '_Floating_chirality_assign',
                            'other_restraint': '_Other_data_type_list'
                            }

NMR_STAR_SF_CATEGORIES = {'dist_restraint': 'general_distance_constraints',
                          'dihed_restraint': 'torsion_angle_constraints',
                          'rdc_restraint': 'RDC_constraints',
                          'noepk_restraint': 'homonucl_NOEs',
                          'jcoup_restraint': 'coupling_constants',
                          'csa_restraint': 'chem_shift_anisotropy',
                          'ddc_restraint': 'dipolar_couplings',
                          'hvycs_restraint': 'CA_CB_chem_shift_constraints',
                          'procs_restraint': 'H_chem_shift_constraints',
                          'csp_restraint': 'chem_shift_perturbation',
                          'auto_relax_restraint': 'auto_relaxation',
                          'ccr_d_csa_restraint': 'dipole_CSA_cross_correlations',
                          'ccr_dd_restraint': 'dipole_dipole_cross_correlations',
                          'fchiral_restraint': 'floating_chiral_stereo_assign',
                          'other_restraint': 'other_data_types'
                          }

NMR_STAR_SF_TAG_ITEMS = {'dist_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                            {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                            {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                             'enum': ('NOE', 'NOE build-up', 'NOE not seen', 'ROE', 'ROE build-up',
                                                      'hydrogen bond', 'disulfide bond', 'paramagnetic relaxation',
                                                      'symmetry', 'general distance', 'mutation', 'chemical shift perturbation',
                                                      'undefined', 'unknown')},
                                            {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                             'enum': ('log-harmonic', 'parabolic', 'square-well-parabolic',
                                                      'square-well-parabolic-linear', 'upper-bound-parabolic',
                                                      'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                      'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                            {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                            {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                         'dihed_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                              'enum': ('J-couplings', 'backbone chemical shifts', 'undefined', 'unknown')},
                                             {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                              'enum': ('parabolic', 'square-well-parabolic', 'square-well-parabolic-linear',
                                                       'upper-bound-parabolic', 'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                       'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'rdc_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Constraint_type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('RDC', 'undefined', 'unknown')},
                                           {'name': 'Potential_type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('parabolic', 'square-well-parabolic', 'square-well-parabolic-linear',
                                                     'upper-bound-parabolic', 'lower-bound-parabolic', 'upper-bound-parabolic-linear',
                                                     'lower-bound-parabolic-linear', 'undefined', 'unknown')},
                                           {'name': 'Tensor_magnitude', 'type': 'float', 'mandatory': False},
                                           {'name': 'Tensor_rhombicity', 'type': 'positive-float', 'mandatory': False},
                                           {'name': 'Tensor_auth_asym_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Tensor_auth_seq_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Tensor_auth_comp_ID', 'type': 'str', 'mandatory': False},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'noepk_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Homonuclear_NOE_val_type', 'type': 'enum', 'mandatory': True,
                                              'enum': ('peak volume', 'peak height', 'contour count', 'na')},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'jcoup_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                              'enforce-non-zero': True},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'csa_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': False,
                                           'enforce-non-zero': True},
                                           {'name': 'Val_units', 'type': 'enum', 'mandatory': False,
                                            'enum': ('ppm', 'ppb')},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'ddc_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': True,
                                           'enforce-non-zero': True},
                                           {'name': 'Scaling_factor', 'type': 'positive-float', 'mandatory': False},
                                           {'name': 'Fitting_procedure', 'type': 'str', 'mandatory': False},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'hvycs_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Units', 'type': 'str', 'mandatory': False},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'procs_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Units', 'type': 'str', 'mandatory': False},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                         'csp_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                           {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                           {'name': 'Type', 'type': 'enum', 'mandatory': False,
                                            'enum': ('macromolecular binding', 'ligand binding', 'ligand fragment binding', 'paramagnetic ligand binding')},
                                           {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                           {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                           {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                           ],
                         'auto_relax_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                  {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                  {'name': 'Temp_calibration_method', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('methanol', 'monoethylene glycol', 'no calibration applied')},
                                                  {'name': 'Temp_control_method', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('single scan interleaving', 'temperature compensation block',
                                                            'single scan interleaving and temperature compensation block',
                                                            'no temperature control applied')},
                                                  {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': True,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Exact_field_strength', 'type': 'positive-float', 'mandatory': False,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Common_relaxation_type_name', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('R1', 'R2', 'R1rho', 'ZQ relaxation', 'longitudinal spin order',
                                                            'single quantum antiphase', 'DQ relaxation')},
                                                  {'name': 'Relaxation_coherence_type', 'type': 'enum', 'mandatory': True,
                                                   'enum': ('Iz', 'Sz', '(I+)+(I-)', '(S+)+(S-)', 'I+', 'I-', 'S+', 'S-',
                                                            '(I+S-)+(I-S+)', 'I-S+', 'I+S-', 'IzSz', '((I+)+(I-))Sz', 'Iz((S+)+(S-))',
                                                            'I+Sz', 'I-Sz', 'IzS+', 'IzS-', '(I+S+)+(I-S-)', 'I+S+', 'I-S-')},
                                                  {'name': 'Relaxation_val_units', 'type': 'enum', 'mandatory': True,
                                                   'enum': ('s-1', 'ms-1', 'us-1', 'ns-1', 'ps-1')},
                                                  {'name': 'Rex_val_units', 'type': 'enum', 'mandatory': False,
                                                   'enum': ('s-1', 'ms-1', 'us-1')},
                                                  {'name': 'Rex_field_strength', 'type': 'positive-float', 'mandatory': False,
                                                   'enforce-non-zero': True},
                                                  {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                  {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                         'ccr_d_csa_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                                 {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': True,
                                                  'enforce-non-zero': True},
                                                 {'name': 'Val_units', 'type': 'enum', 'mandatory': True,
                                                  'enum': ('s-1', 'ms-1', 'us-1')},
                                                 {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                                 {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                                 {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                 ],
                         'ccr_dd_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                              {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                              {'name': 'Spectrometer_frequency_1H', 'type': 'positive-float', 'mandatory': True,
                                               'enforce-non-zero': True},
                                              {'name': 'Val_units', 'type': 'enum', 'mandatory': True,
                                               'enum': ('s-1', 'ms-1', 'us-1')},
                                              {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                              {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                         'fchiral_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                               {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                               {'name': 'Stereo_count', 'type': 'int', 'mandatory': True},
                                               {'name': 'Stereo_assigned_count', 'type': 'int', 'mandatory': True}
                                               ],
                         'other_restraint': [{'name': 'Sf_category', 'type': 'str', 'mandatory': True},
                                             {'name': 'Sf_framecode', 'type': 'str', 'mandatory': True},
                                             {'name': 'Definition', 'type': 'str', 'mandatory': True},
                                             {'name': 'Data_file_name', 'type': 'str', 'mandatory': False},
                                             {'name': 'ID', 'type': 'positive-int', 'mandatory': True},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ]
                         }

NMR_STAR_LP_CATEGORIES = {'dist_restraint': '_Gen_dist_constraint',
                          'dihed_restraint': '_Torsion_angle_constraint',
                          'rdc_restraint': '_RDC_constraint',
                          'noepk_restraint': '_Homonucl_NOE',
                          'jcoup_restraint': '_Coupling_constant',
                          'csa_restraint': '_CS_anisotropy',
                          'ddc_restraint': '_Dipolar_coupling',
                          'hvycs_restraint': '_CA_CB_constraint',
                          'procs_restraint': '_H_chem_shift_constraint',
                          'csp_restraint': '_Chem_shift_perturbation',
                          'auto_relax_restraint': '_Auto_relaxation',
                          'ccr_d_csa_restraint': '_Cross_correlation_D_CSA',
                          'ccr_dd_restraint': '_Cross_correlation_DD',
                          'fchical_restraint': 'Floating_chirality',
                          'other_restraint': '_Other_data'
                          }

NMR_STAR_LP_KEY_ITEMS = {'dist_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                            {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                            {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                            {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                            {'name': 'Atom_ID_1', 'type': 'str'},
                                            {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                            {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                            {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                            {'name': 'Atom_ID_2', 'type': 'str'}
                                            ],
                         'dihed_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_3', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_3'},
                                             {'name': 'Comp_index_ID_3', 'type': 'int', 'default-from': 'Seq_ID_3'},
                                             {'name': 'Comp_ID_3', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_3', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_4', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_4'},
                                             {'name': 'Comp_index_ID_4', 'type': 'int', 'default-from': 'Seq_ID_4'},
                                             {'name': 'Comp_ID_4', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_4', 'type': 'str'}
                                             ],
                         'rdc_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                           {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                           {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_1', 'type': 'str'},
                                           {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                           {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                           {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_2', 'type': 'str'}
                                           ],
                         'noepk_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'}
                                             ],
                         'jcoup_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'}
                                             ],
                         'rdc_raw_data': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                          {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                          {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                          {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                          {'name': 'Atom_ID_1', 'type': 'str'},
                                          {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                          {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                          {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                          {'name': 'Atom_ID_2', 'type': 'str'}
                                          ],
                         'csa_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                           {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID', 'type': 'str'}
                                           ],
                         'ddc_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                           {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_1', 'type': 'str'},
                                           {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                           {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID_2', 'type': 'str'}
                                           ],
                         'hvycs_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                             {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                             {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_1', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                             {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                             {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_2', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_3', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_3'},
                                             {'name': 'Comp_index_ID_3', 'type': 'int', 'default-from': 'Seq_ID_3'},
                                             {'name': 'Comp_ID_3', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_3', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_4', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_4'},
                                             {'name': 'Comp_index_ID_4', 'type': 'int', 'default-from': 'Seq_ID_4'},
                                             {'name': 'Comp_ID_4', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_4', 'type': 'str'},
                                             {'name': 'Entity_assembly_ID_5', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_5'},
                                             {'name': 'Comp_index_ID_5', 'type': 'int', 'default-from': 'Seq_ID_5'},
                                             {'name': 'Comp_ID_5', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID_5', 'type': 'str'}
                                             ],
                         'procs_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID'},
                                             {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                             {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID', 'type': 'str'}
                                             ],
                         'csp_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                           {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                           {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                           {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                           {'name': 'Atom_ID', 'type': 'str'}
                                           ],
                         'auto_relax_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                  {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                                  {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                                  {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                                  {'name': 'Atom_ID', 'type': 'str'}
                                                  ],
                         'ccr_d_csa_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                                 {'name': 'Dipole_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'Dipole_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_seq_ID_1'},
                                                 {'name': 'Dipole_comp_ID_1', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Dipole_atom_ID_1', 'type': 'str'},
                                                 {'name': 'Dipole_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'Dipole_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_seq_ID_2'},
                                                 {'name': 'Dipole_comp_ID_2', 'type': 'str', 'uppercase': True},
                                                 {'name': 'Dipole_atom_ID_2', 'type': 'str'},
                                                 {'name': 'CSA_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'CSA_comp_index_ID_1', 'type': 'int', 'default-from': 'CSA_seq_ID_1'},
                                                 {'name': 'CSA_comp_ID_1', 'type': 'str', 'uppercase': True},
                                                 {'name': 'CSA_atom_ID_1', 'type': 'str'},
                                                 {'name': 'CSA_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                                 {'name': 'CSA_comp_index_ID_2', 'type': 'int', 'default-from': 'CSA_seq_ID_2'},
                                                 {'name': 'CSA_comp_ID_2', 'type': 'str', 'uppercase': True},
                                                 {'name': 'CSA_atom_ID_2', 'type': 'str'}
                                                 ],
                         'ccr_dd_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                              {'name': 'Dipole_1_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_1_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_1_seq_ID_1'},
                                              {'name': 'Dipole_1_comp_ID_1', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_1_atom_ID_1', 'type': 'str'},
                                              {'name': 'Dipole_1_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_1_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_1_seq_ID_2'},
                                              {'name': 'Dipole_1_comp_ID_2', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_1_atom_ID_2', 'type': 'str'},
                                              {'name': 'Dipole_2_entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_2_comp_index_ID_1', 'type': 'int', 'default-from': 'Dipole_2_seq_ID_1'},
                                              {'name': 'Dipole_2_comp_ID_1', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_2_atom_ID_1', 'type': 'str'},
                                              {'name': 'Dipole_2_entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1'},
                                              {'name': 'Dipole_2_comp_index_ID_2', 'type': 'int', 'default-from': 'Dipole_2_seq_ID_2'},
                                              {'name': 'Dipole_2_comp_ID_2', 'type': 'str', 'uppercase': True},
                                              {'name': 'Dipole_2_atom_ID_2', 'type': 'str'}
                                              ],
                         'fchiral_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                               {'name': 'Entity_assembly_ID_1', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_1'},
                                               {'name': 'Comp_index_ID_1', 'type': 'int', 'default-from': 'Seq_ID_1'},
                                               {'name': 'Comp_ID_1', 'type': 'str', 'uppercase': True},
                                               {'name': 'Atom_ID_1', 'type': 'str'},
                                               {'name': 'Entity_assembly_ID_2', 'type': 'positive-int-as-str', 'default': '1', 'default-from': 'Auth_asym_ID_2'},
                                               {'name': 'Comp_index_ID_2', 'type': 'int', 'default-from': 'Seq_ID_2'},
                                               {'name': 'Comp_ID_2', 'type': 'str', 'uppercase': True},
                                               {'name': 'Atom_ID_2', 'type': 'str'}
                                               ],
                         'other_restraint': [{'name': 'ID', 'type': 'positive-int', 'auto-increment': True},
                                             {'name': 'Entity_assembly_ID', 'type': 'positive-int-as-str', 'default': '1'},
                                             {'name': 'Comp_index_ID', 'type': 'int', 'default-from': 'Seq_ID'},
                                             {'name': 'Comp_ID', 'type': 'str', 'uppercase': True},
                                             {'name': 'Atom_ID', 'type': 'str'}
                                             ]
                         }

NMR_STAR_LP_DATA_ITEMS = {'dist_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                             {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                              'enforce-non-zero': True},
                                             {'name': 'Member_logic_code', 'type': 'enum', 'mandatory': False,
                                              'enum': ('OR', 'AND'),
                                              'enforce-enum': True},
                                             {'name': 'Target_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Lower_linear_limit',
                                                                        'Upper_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val'],
                                                        'larger-than': ['Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Target_val_uncertainty', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                              'range': DIST_UNCERTAINTY_RANGE},
                                             {'name': 'Lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val',
                                                                        'Upper_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Upper_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'smaller-than': None,
                                                        'larger-than': ['Distance_lower_bound_val', 'Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Distance_lower_bound_val', 'type': 'range-float', 'mandatory': False,
                                              'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val', 'Lower_linear_limit', 'Upper_linear_limit', 'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Distance_upper_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit'],
                                                        'larger-than': ['Distance_upper_bound_val', 'Upper_linear_limit']}},
                                             {'name': 'Distance_upper_bound_val', 'type': 'range-float', 'mandatory': False,
                                              'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val', 'Lower_linear_limit', 'Upper_linear_limit', 'Distance_lower_bound_val'],
                                                        'coexist-with': None,  # ['Distance_lower_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val'],
                                                        'larger-than': ['Upper_linear_limit']}},
                                             {'name': 'Upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True, 'void-zero': True,
                                              'range': DIST_RESTRAINT_RANGE,
                                              'group': {'member-with': ['Target_val',
                                                                        'Lower_linear_limit',
                                                                        'Distance_lower_bound_val',
                                                                        'Distance_upper_bound_val'],
                                                        'coexist-with': None,  # ['Lower_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'smaller-than': ['Lower_linear_limit', 'Distance_lower_bound_val', 'Distance_upper_bound_val'],
                                                        'larger-than': None}},
                                             {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                              'range': WEIGHT_RANGE},
                                             # 'enforce-non-zero': True},
                                             {'name': 'Distance_val', 'type': 'range-float', 'mandatory': False,
                                                      'range': DIST_RESTRAINT_RANGE},
                                             {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                             {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                             {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                             {'name': 'Gen_dist_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                              'default': '1', 'default-from': 'parent'},
                                             {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                             ],
                          'dihed_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                              {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                               'enforce-non-zero': True},
                                              {'name': 'Torsion_angle_name', 'type': 'str', 'mandatory': False},
                                              {'name': 'Angle_target_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit',
                                                                         'Angle_lower_bound_val',
                                                                         'Angle_upper_bound_val'],
                                                         'coexist-with': None,
                                                         'smaller-than': ['Angle_lower_linear_limit', 'Angle_lower_bound_val'],
                                                         'larger-than': ['Angle_upper_bound_val', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_target_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': ANGLE_UNCERTAINTY_RANGE},
                                              {'name': 'Angle_lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_upper_linear_limit',
                                                                         'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_upper_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'smaller-than': None,
                                                         'larger-than': ['Angle_lower_bound_val', 'Angle_upper_bound', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_lower_bound_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_upper_bound_val'],
                                                         'smaller-than': ['Angle_lower_linear_limit'],
                                                         'larger-than': ['Angle_upper_bound_val', 'Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_upper_bound_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_upper_linear_limit', 'Angle_lower_bound_val'],
                                                         'coexist-with': None,  # ['Angle_lower_bound_val'],
                                                         'smaller-than': ['Angle_lower_bound_val', 'Angle_upper_linear_limit'],
                                                         'larger-than': ['Angle_upper_linear_limit'],
                                                         'circular-shift': 360.0}},
                                              {'name': 'Angle_upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': ANGLE_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Angle_target_val', 'Angle_lower_linear_limit',
                                                                         'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'coexist-with': None,  # ['Angle_lower_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'smaller-than': ['Angle_lower_linear_limit', 'Angle_lower_bound_val', 'Angle_upper_bound_val'],
                                                         'larger-than': None,
                                                         'circular-shift': 360.0}},
                                              {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                               'range': WEIGHT_RANGE},
                                              # 'enforce-non-zero': True},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_3', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_4', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_name_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Torsion_angle_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'rdc_restraint': [{'name': 'Index_ID', 'type': 'index-int', 'mandatory': False},
                                            {'name': 'Combination_ID', 'type': 'positive-int', 'mandatory': False,
                                             'enforce-non-zero': True},
                                            {'name': 'Target_value', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound'],
                                                       'larger-than': ['RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'Target_value_uncertainty', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': RDC_UNCERTAINTY_RANGE},
                                            {'name': 'RDC_lower_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'smaller-than': None,
                                                       'larger-than': ['RDC_lower_bound', 'RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'RDC_lower_bound', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit'],
                                                       'larger-than': ['RDC_upper_bound', 'RDC_upper_linear_limit']}},
                                            {'name': 'RDC_upper_bound', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_lower_linear_limit', 'RDC_upper_linear_limit', 'RDC_lower_bound'],
                                                       'coexist-with': None,  # ['RDC_lower_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound'],
                                                       'larger-than': ['RDC_upper_linear_limit']}},
                                            {'name': 'RDC_upper_linear_limit', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                             'range': RDC_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Target_value', 'RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'coexist-with': None,  # ['RDC_upper_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'smaller-than': ['RDC_lower_linear_limit', 'RDC_lower_bound', 'RDC_upper_bound'],
                                                       'larger-than': None}},
                                            {'name': 'Weight', 'type': 'range-float', 'mandatory': False,
                                             'range': WEIGHT_RANGE},
                                            # 'enforce-non-zero': True},
                                            {'name': 'RDC_val', 'type': 'range-float', 'mandatory': False,
                                             'range': RDC_RESTRAINT_RANGE},
                                            {'name': 'RDC_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': RDC_UNCERTAINTY_RANGE},
                                            {'name': 'RDC_val_scale_factor', 'type': 'range-float', 'mandatory': False,
                                             'range': SCALE_RANGE,
                                             'enforce-non-zero': True},
                                            {'name': 'RDC_distant_dependent', 'type': 'bool', 'mandatory': False},
                                            {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_name_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_name_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'RDC_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True, 'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'noepk_restraint': [{'name': 'Val', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val_min', 'Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': None}},
                                              {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Val_min', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val', 'Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': ['Val_max']}},
                                              {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'group': {'member-with': ['Val', 'Val_min'],
                                                         'coexist-with': None,
                                                         'smaller-than': ['Val_min'],
                                                         'larger-than': None}},
                                              {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Homonucl_NOE_list_ID', 'type': 'pointer-index', 'mandatory': True, 'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'jcoup_restraint': [{'name': 'Code', 'type': 'str', 'mandatory': True},
                                              {'name': 'Atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                               # 'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                               # 'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Ambiguity_code_1', 'type': 'enum-int', 'mandatory': False,
                                               'enum': ALLOWED_AMBIGUITY_CODES,
                                               'enforce-enum': True},
                                              {'name': 'Atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                               'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                               'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Ambiguity_code_2', 'type': 'enum-int', 'mandatory': False,
                                               'enum': ALLOWED_AMBIGUITY_CODES,
                                               'enforce-enum': True},
                                              {'name': 'Val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Val_min', 'Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': None}},
                                              {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Val_min', 'type': 'range-float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Val_max'],
                                                         'coexist-with': None,
                                                         'smaller-than': None,
                                                         'larger-than': ['Val_max']}},
                                              {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                               'range': RDC_RESTRAINT_RANGE,
                                               'group': {'member-with': ['Val_min'],
                                                         'coexist-with': None,
                                                         'smaller-than': ['Val_min'],
                                                         'larger-than': None}},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Coupling_constant_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'csa_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                             'range': CSA_RESTRAINT_RANGE},
                                            {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': {'min_inclusive': 0.0}},
                                            {'name': 'Principal_value_sigma_11_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_22_val', 'Principal_value_sigma_33_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_value_sigma_22_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_11_val', 'Principal_value_sigma_33_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_value_sigma_33_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': CSA_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_value_sigma_11_val', 'Principal_value_sigma_22_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_alpha_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_beta_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_beta_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_gamma_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_beta_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Bond_length', 'type': 'range-float', 'mandatory': False,
                                             'range': DIST_RESTRAINT_RANGE},
                                            {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Chem_shift_anisotropy_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'ddc_restraint': [{'name': 'Dipolar_coupling_code', 'type': 'str', 'mandatory': True},
                                            {'name': 'Atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_1',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Ambiguity_code_1', 'type': 'enum-int', 'mandatory': False,
                                             'enum': ALLOWED_AMBIGUITY_CODES,
                                             'enforce-enum': True},
                                            {'name': 'Atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID_2',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Ambiguity_code_2', 'type': 'enum-int', 'mandatory': False,
                                             'enum': ALLOWED_AMBIGUITY_CODES,
                                             'enforce-enum': True},
                                            {'name': 'Val', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_min', 'Val_max'],
                                                       'coexist-with': None,
                                                       'smaller-than': None,
                                                       'larger-than': None}},
                                            {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': {'min_inclusive': 0.0}},
                                            {'name': 'Val_min', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_max'],
                                                       'coexist-with': None,
                                                       'smaller-than': None,
                                                       'larger-than': ['Val_max']}},
                                            {'name': 'Val_max', 'type': 'float', 'mandatory': False, 'group-mandatory': True,
                                             'group': {'member-with': ['Val_min'],
                                                       'coexist-with': None,
                                                       'smaller-than': ['Val_min'],
                                                       'larger-than': None}},
                                            {'name': 'Principal_Euler_angle_alpha_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_beta_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_beta_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_gamma_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Principal_Euler_angle_gamma_val', 'type': 'range-float', 'mandatory': False, 'group-mandatory': False,
                                             'range': ANGLE_RESTRAINT_RANGE,
                                             'group': {'member-with': ['Principal_Euler_angle_alpha_val', 'Principal_Euler_angle_beta_val'],
                                                       'coexist-with': None}},
                                            {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                            {'name': 'Dipolar_coupling_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'hvycs_restraint': [{'name': 'CA_chem_shift_val', 'type': 'range-float', 'mandatory': True,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'CA_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'CB_chem_shift_val', 'type': 'range-float', 'mandatory': True,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'CB_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_3', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_3', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_4', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_4', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_asym_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID_5', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID_5', 'type': 'str', 'mandatory': False},
                                              {'name': 'CA_CB_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'procs_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Chem_shift_val', 'type': 'range-float', 'mandatory': True,
                                               'range': CS_RESTRAINT_RANGE},
                                              {'name': 'Chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': CS_UNCERTAINTY_RANGE},
                                              {'name': 'Auth_asym_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'H_chem_shift_constraint_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          'csp_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                             'enforce-enum': True},
                                            {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                             'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                             'enforce-enum': True},
                                            {'name': 'Chem_shift_val', 'type': 'range-float', 'mandatory': False,
                                             'range': CS_RESTRAINT_RANGE},
                                            {'name': 'Chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': CS_UNCERTAINTY_RANGE},
                                            {'name': 'Difference_chem_shift_val', 'type': 'range-float', 'mandatory': False,
                                             'range': CS_RESTRAINT_RANGE},
                                            {'name': 'Difference_chem_shift_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                             'range': CS_UNCERTAINTY_RANGE},
                                            {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                            {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                            {'name': 'Chem_shift_perturbation_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                             'default': '1', 'default-from': 'parent'},
                                            {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                            ],
                          'auto_relax_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                                    'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                    'enforce-enum': True},
                                                   {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                                    'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                    'enforce-enum': True},
                                                   {'name': 'Auto_relaxation_val', 'type': 'range-float', 'mandatory': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Auto_relaxation_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Rex_val', 'type': 'range-float', 'mandatory': False,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Rex_val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                    'range': PRE_RESTRAINT_RANGE},
                                                   {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                                   {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                                   {'name': 'Auto_relaxation_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                    'default': '1', 'default-from': 'parent'},
                                                   {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                   ],
                          'ccr_d_csa_restraint': [{'name': 'Dipole_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_atom_ID_1',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_atom_ID_1',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_atom_ID_2',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'Dipole_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_atom_ID_2',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'CSA_atom_ID_1',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'CSA_atom_ID_1',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'CSA_atom_ID_2',
                                                   'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                   'enforce-enum': True},
                                                  {'name': 'CSA_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'CSA_atom_ID_2',
                                                   'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                   'enforce-enum': True},
                                                  {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                                   'range': CCR_RESTRAINT_RANGE},
                                                  {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                   'range': CCR_RESTRAINT_RANGE},
                                                  {'name': 'Dipole_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Dipole_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                  {'name': 'Dipole_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Dipole_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                  {'name': 'CSA_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                  {'name': 'CSA_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'CSA_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                                  {'name': 'Cross_correlation_D_CSA_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                   'default': '1', 'default-from': 'parent'},
                                                  {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                                  ],
                          'ccr_dd_restraint': [{'name': 'Dipole_1_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_1',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_1',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_2',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_1_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_1_atom_ID_2',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_type_1', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_1',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_isotope_number_1', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_1',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_type_2', 'type': 'enum', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_2',
                                                'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                                'enforce-enum': True},
                                               {'name': 'Dipole_2_atom_isotope_number_2', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Dipole_2_atom_ID_2',
                                                'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                                'enforce-enum': True},
                                               {'name': 'Val', 'type': 'range-float', 'mandatory': True,
                                                'range': CCR_RESTRAINT_RANGE},
                                               {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                                'range': CCR_RESTRAINT_RANGE},
                                               {'name': 'Dipole_1_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_1_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_entity_assembly_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_entity_assembly_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Dipole_2_auth_atom_ID_2', 'type': 'str', 'mandatory': False},
                                               {'name': 'Cross_correlation_DD_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                                'default': '1', 'default-from': 'parent'},
                                               {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                               ],
                          'fchiral_restraint': [{'name': 'Stereospecific_assignment_code', 'type': 'str', 'mandatory': True},
                                                {'name': 'Auth_asym_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_seq_ID_1', 'type': 'int', 'mandatory': False},
                                                {'name': 'Auth_comp_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_atom_ID_1', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_asym_ID_2', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_seq_ID_2', 'type': 'int', 'mandatory': False},
                                                {'name': 'Auth_comp_ID_2', 'type': 'str', 'mandatory': False},
                                                {'name': 'Auth_atom_ID_2', 'type': 'str', 'mandatory': False}
                                                ],
                          'other_restraint': [{'name': 'Atom_type', 'type': 'enum', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS.keys()),
                                               'enforce-enum': True},
                                              {'name': 'Atom_isotope_number', 'type': 'enum-int', 'mandatory': True, 'default-from': 'Atom_ID',
                                               'enum': set(ALLOWED_ISOTOPE_NUMBERS),
                                               'enforce-enum': True},
                                              {'name': 'Val', 'type': 'float', 'mandatory': True},
                                              {'name': 'Val_err', 'type': 'range-float', 'mandatory': False, 'void-zero': True,
                                               'range': {'min_inclusive': 0.0}},
                                              {'name': 'Auth_entity_assembly_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_seq_ID', 'type': 'int', 'mandatory': False},
                                              {'name': 'Auth_comp_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Auth_atom_ID', 'type': 'str', 'mandatory': False},
                                              {'name': 'Other_data_type_list_ID', 'type': 'pointer-index', 'mandatory': True,
                                               'default': '1', 'default-from': 'parent'},
                                              {'name': 'Entry_ID', 'type': 'str', 'mandatory': True}
                                              ],
                          }


def toNpArray(atom):
    """ Return Numpy array of a given Cartesian coordinate in {'x': float, 'y': float, 'z': float} format.
    """

    return numpy.asarray([atom['x'], atom['y'], atom['z']], dtype=float)


def toRegEx(string):
    """ Return regular expression for a given string including XPLOR-NIH wildcard format.
    """

    if '*' in string:  # any string
        return string.replace('*', '.*')
    if '%' in string:  # a single character
        return string.replace('%', '.')
    if '#' in string:  # any number
        return string.replace('#', '[+-]?[0-9\\.]*')
    if '+' in string:  # any digit
        return string.replace('+', '[0-9]*')
    return string


def toNefEx(string):
    """ Return NEF regular expression for a given string including XPLOR-NIH wildcard format.
    """

    if '*' in string:  # any string
        return re.sub(r'\*\*', '*', string)
    if '%' in string:  # a single character
        return re.sub(r'\*\*', '*', string.replace('%', '*'))
    if '#' in string:  # any number
        return re.sub(r'\*\*', '*', string.replace('#', '*'))
    if '+' in string:  # any digit
        return re.sub(r'\%\%', '%', string.replace('+', '%'))
    return string


def stripQuot(string):
    """ Return strippped string by removing single/double quotation marks.
    """

    _string = string.strip()

    while True:
        if (_string[0] == '\'' and _string[-1] == '\'')\
           or (_string[0] == '"' and _string[-1] == '"'):
            _string = _string[1:len(_string) - 1].strip()
        else:
            break

    return _string


def translateToStdAtomName(atomId, refCompId=None, refAtomIdList=None, ccU=None):
    """ Translate software specific atom nomenclature for standard residues to the CCD one.
    """

    atomId = atomId.upper()

    if refAtomIdList is not None:
        if atomId in refAtomIdList:
            return atomId

    elif refCompId is not None and ccU is not None:
        refCompId = translateToStdResName(refCompId)
        if ccU.updateChemCompDict(refCompId):
            refAtomIdList = [cca[ccU.ccaAtomId] for cca in ccU.lastAtomList]
            if atomId in refAtomIdList:
                return atomId
            # DNA/RNA OH 5/3 prime terminus
            if atomId.startswith("H1'"):
                if atomId == "H1''" and "H1'A" in refAtomIdList:  # 4DG
                    return "H1'A"
            elif atomId.startswith("H2'"):
                if atomId == "H2'" and "H2'1" in refAtomIdList:  # DCZ, THM
                    return "H2'1"
                if atomId == "H2''" and "H2'2" in refAtomIdList:  # DCZ, THM
                    return "H2'2"
            elif atomId.startswith("H4'"):
                if atomId == "H4''" and "H4'A" in refAtomIdList:  # 4DG
                    return "H4'A"
            elif atomId.startswith("H5'"):
                if atomId == "H5'" and "H5'1" in refAtomIdList:  # DCZ, THM
                    return "H5'1"
                if atomId == "H5''" and "H5'2" in refAtomIdList:  # DCZ, THM
                    return "H5'2"
                if atomId == "H5''" and "H5'A" in refAtomIdList:  # 4DG, 23G
                    return "H5'A"
            elif atomId.startswith('M'):  # methyl group
                if 'H' + atomId[1:] + '1' in refAtomIdList:
                    return 'H' + atomId[1:]
                candidates = ccU.getRepresentativeMethylProtons(refCompId)
                if len(candidates) == 1:
                    atomId = candidates[0]
                    return atomId[:-1] if atomId.endswith('1') else atomId
            elif (atomId[0] + 'N' + atomId[1:] in refAtomIdList) or (atomId[0] + 'N' + atomId[1:] + '1' in refAtomIdList):  # 5CM
                return atomId[0] + 'N' + atomId[1:]
            elif atomId[0].endswith('2') and (atomId[0:-1] + 'A') in refAtomIdList:
                return atomId[0:-1] + 'A'
            elif atomId[0].endswith('3') and (atomId[0:-1] + 'B') in refAtomIdList:
                return atomId[0:-1] + 'B'
            elif atomId.startswith('1H'):
                if atomId[1:] + '1' in refAtomIdList:
                    return atomId[1:] + '1'
            elif atomId.startswith('2H'):
                if atomId[1:] + '2' in refAtomIdList:
                    return atomId[1:] + '2'
            elif atomId == "HX'":  # derived from 2mko AMBER RDC restraints
                if "H4'" in refAtomIdList:
                    return "H4'"

            # ambiguous atom generated by 'makeDIST_RST'
            if atomId[0] == 'Q':
                if atomId.startswith('QP'):
                    if 'H' + atomId[2:] + '2' in refAtomIdList:
                        return 'H' + atomId[2:] + '%'
                else:
                    if 'H' + atomId[1:] + '2' in refAtomIdList:
                        return 'H' + atomId[1:] + '%'

            elif atomId[-1] in ('-', '+'):
                if atomId[:-1] + '2' in refAtomIdList:
                    return atomId[:-1] + '%'

            elif atomId[0] == 'M':
                if atomId[-1] in ('X', 'Y'):
                    if 'H' + atomId[1:-1] + '1' in refAtomIdList or 'H' + atomId[1:-1] + '11' in refAtomIdList:
                        return 'H' + atomId[1:-1] + '%'
                elif 'H' + atomId[1:] + '1' in refAtomIdList or 'H' + atomId[1:] + '11' in refAtomIdList:
                    return 'H' + atomId[1:] + '%'

            elif atomId + '2' in refAtomIdList:
                return atomId + '%'

    # GROMACS atom nomenclature
    if refCompId is not None:
        if refCompId == 'ILE':
            if atomId in ('HD1', 'HD2', 'HD3'):
                return 'HD1' + atomId[-1]
            if atomId == 'CD':
                return 'CD1'
        if len(refCompId) == 3 and refCompId in monDict3:
            if atomId == 'O1':
                return 'O'
            if atomId == 'O2':
                return 'OXT'
            if atomId.startswith('HT') and len(atomId) > 2:
                return 'H' + atomId[2:]

    if atomId.endswith("O'1"):
        atomId = atomId[:len(atomId) - 3] + "O1'"
    elif atomId.endswith("O'2"):
        atomId = atomId[:len(atomId) - 3] + "O2'"
    elif atomId.endswith("O'3"):
        atomId = atomId[:len(atomId) - 3] + "O3'"
    elif atomId.endswith("O'4"):
        atomId = atomId[:len(atomId) - 3] + "O4'"
    elif atomId.endswith("O'5"):
        atomId = atomId[:len(atomId) - 3] + "O5'"
    elif atomId.endswith("O'6"):
        atomId = atomId[:len(atomId) - 3] + "O6'"
    elif atomId.endswith("'1") and not atomId.endswith("''1"):
        atomId = atomId.rstrip('1')
    elif atomId.endswith("'2") and not atomId.endswith("''2"):
        atomId = atomId.rstrip('2') + "'"
    elif atomId == 'O1P':
        atomId = 'OP1'
    elif atomId == 'O2P':
        atomId = 'OP2'
    elif atomId == 'O3P':
        atomId = 'OP3'
    elif atomId == 'H3T':
        atomId = "HO3'"
    elif atomId == 'H5T':
        atomId = 'HOP2'
    elif atomId.endswith("''"):
        if atomId[0] in ('C', 'O') and atomId[1].isdigit():
            atomId = atomId[:len(atomId) - 1]
    elif atomId.endswith('"'):
        atomId = atomId[:len(atomId) - 1] + "''"

    if refAtomIdList is not None and atomId not in refAtomIdList:
        if not atomId.endswith("'") and (atomId + "'") in refAtomIdList:
            return atomId + "'"
        if atomId.endswith("''''"):
            if atomId.startswith('H2') and "H2'2" in refAtomIdList:
                return "H2'2"
            if atomId[:-2] in refAtomIdList:
                return atomId[:-2]
        if atomId.endswith("'''"):
            if atomId[:-1] in refAtomIdList:
                return atomId[:-1]
        if atomId == "H2''1" and "H2'" in refAtomIdList:
            return "H2'"
        if atomId in ("H2''2", "H2''"):
            if "HO2'" in refAtomIdList:
                return "HO2'"
            if "H2''" in refAtomIdList:
                return "H2''"
            if atomId == "H2''" and "H2'1" in refAtomIdList:
                return "H2'1"
        if atomId.endswith("''") and atomId[:-1] in refAtomIdList:
            return atomId[:-1]
        if atomId[0] == 'H' and len(atomId) == 3 and atomId[1].isdigit() and atomId[2] in ('1', '2'):
            n = atomId[1]
            if atomId.endswith('1') and ('HN' + n) in refAtomIdList:
                return 'HN' + n
            if atomId.endswith('2') and ('HN' + n + 'A') in refAtomIdList:
                return 'HN' + n + 'A'

    return atomId


def translateToStdResName(compId):
    """ Translate software specific residue name for standard residues to the CCD one.
    """

    if len(compId) > 3:
        compId3 = compId[:3]

        if compId3 in monDict3:
            return compId3

    if compId.endswith('5') or compId.endswith('3'):
        _compId = compId[:-1]

        if _compId in monDict3:
            return _compId

    if compId.startswith('R') and len(compId) > 1 and compId[1] in ('A', 'C', 'G', 'U'):
        _compId = compId[1:]

        if _compId in monDict3:
            return _compId
        """ do not use
        if _compId.endswith('5') or _compId.endswith('3'):
            _compId = _compId[:-1]

            if _compId in monDict3:
                return _compId
        """
    if compId in ('HIE', 'HIP', 'HID'):
        return 'HIS'

    if len(compId) == 3:
        if compId == 'ADE' or compId.startswith('DA'):
            return 'DA'
        if compId == 'CYT' or compId.startswith('DC'):
            return 'DC'
        if compId == 'GUA' or compId.startswith('DG'):
            return 'DG'
        if compId == 'THY' or compId.startswith('DT'):
            return 'DT'

    if compId == 'RADE':
        return 'A'
    if compId == 'RCYT':
        return 'C'
    if compId == 'RGUA':
        return 'G'
    if compId == 'URA':
        return 'U'

    return compId


def checkCoordinates(verbose=True, log=sys.stdout,
                     representativeModelId=REPRESENTATIVE_MODEL_ID,
                     cR=None, prevCoordCheck=None,
                     testTag=True):
    """ Examine the coordinates for MR/PT parser listener.
    """

    changed = False

    polySeq = None if prevCoordCheck is None or 'polymer_sequence' not in prevCoordCheck else prevCoordCheck['polymer_sequence']
    altPolySeq = None if prevCoordCheck is None or 'alt_polymer_sequence' not in prevCoordCheck else prevCoordCheck['alt_polymer_sequence']
    nonPoly = None if prevCoordCheck is None or 'non_polymer' not in prevCoordCheck else prevCoordCheck['non_polymer']
    branch = None if prevCoordCheck is None or 'branch' not in prevCoordCheck else prevCoordCheck['branch']

    if polySeq is None:
        changed = True

        polySeqAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_poly_seq_scheme', 'auth_mon_id') else 'mon_id'
        nonPolyAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_nonpoly_scheme', 'auth_mon_id') else 'mon_id'
        branchAuthMonIdName = 'auth_mon_id' if cR.hasItem('pdbx_branch_scheme', 'auth_mon_id') else 'mon_id'

        # loop categories
        _lpCategories = {'poly_seq': 'pdbx_poly_seq_scheme',
                         'non_poly': 'pdbx_nonpoly_scheme',
                         'branch': 'pdbx_branch_scheme',
                         'coordinate': 'atom_site'
                         }

        # key items of loop
        _keyItems = {'poly_seq': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                  {'name': 'seq_id', 'type': 'int', 'alt_name': 'seq_id'},
                                  {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                  {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                  {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                  {'name': polySeqAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                  ],
                     'non_poly': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                  {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'seq_id'},
                                  {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                  {'name': 'pdb_strand_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                  {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                  {'name': nonPolyAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                  ],
                     'branch': [{'name': 'asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                {'name': 'pdb_seq_num', 'type': 'int', 'alt_name': 'seq_id'},
                                {'name': 'mon_id', 'type': 'str', 'alt_name': 'comp_id'},
                                {'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                {'name': 'auth_seq_num', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                {'name': branchAuthMonIdName, 'type': 'str', 'alt_name': 'auth_comp_id', 'default': '.'}
                                ],
                     'coordinate': [{'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'auth_chain_id'},
                                    {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                    {'name': 'auth_seq_id', 'type': 'int', 'alt_name': 'auth_seq_id'},
                                    {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'seq_id'},
                                    {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'auth_comp_id'},
                                    {'name': 'label_comp_id', 'type': 'str', 'alt_name': 'comp_id'}
                                    ]
                     }

        contentSubtype = 'poly_seq'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        try:

            try:
                polySeq = cR.getPolymerSequence(lpCategory, keyItems,
                                                withStructConf=False,
                                                withRmsd=False)
            except KeyError:  # pdbx_PDB_ins_code throws KeyError
                polySeq = []

            if len(polySeq) == 0:
                contentSubtype = 'coordinate'

                lpCategory = _lpCategories[contentSubtype]
                keyItems = _keyItems[contentSubtype]

                try:
                    polySeq = cR.getPolymerSequence(lpCategory, keyItems,
                                                    withStructConf=False,
                                                    withRmsd=False)
                except KeyError:
                    polySeq = []

            if len(polySeq) > 1:
                ps = copy.copy(polySeq[0])
                ps['auth_seq_id'] = ps['seq_id']
                altPolySeq = [ps]
                lastSeqId = ps['auth_seq_id'][-1]

                for chainId in range(1, len(polySeq)):
                    ps = copy.copy(polySeq[chainId])
                    if ps['seq_id'][0] <= lastSeqId:
                        offset = lastSeqId + 1 - ps['seq_id'][0]
                    else:
                        offset = 0
                    ps['auth_seq_id'] = [s + offset for s in ps['seq_id']]
                    altPolySeq.append(ps)
                    lastSeqId = ps['auth_seq_id'][-1]

        except Exception as e:
            if verbose:
                log.write(f"+ParserListenerUtil.checkCoordinates() ++ Error  - {str(e)}\n")

        contentSubtype = 'non_poly'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        nonPoly = None

        if cR.hasCategory(lpCategory):

            try:
                nonPoly = cR.getPolymerSequence(lpCategory, keyItems,
                                                withStructConf=False,
                                                withRmsd=False)

                for np in nonPoly:
                    conflict = False

                    altAuthSeqIds = []

                    for authSeqId, labelSeqId in zip(np['auth_seq_id'], np['seq_id']):

                        ps = next((ps for ps in polySeq if ps['auth_chain_id'] == np['auth_chain_id']), None)

                        if ps is None:
                            continue

                        if authSeqId in ps['auth_seq_id'] and labelSeqId not in ps['auth_seq_id']:
                            altAuthSeqIds.append(labelSeqId)

                            if 'ambig_auth_seq_id' not in ps:
                                ps['ambug_auth_seq_id'] = []
                            ps['ambug_auth_seq_id'].append(authSeqId)

                            conflict = True

                        else:
                            altAuthSeqIds.append(authSeqId)

                    if conflict:
                        np['alt_auth_seq_id'] = altAuthSeqIds

            except KeyError:
                nonPoly = None

        contentSubtype = 'branch'

        lpCategory = _lpCategories[contentSubtype]
        keyItems = _keyItems[contentSubtype]

        branch = None

        if cR.hasCategory(lpCategory):

            try:
                branch = cR.getPolymerSequence(lpCategory, keyItems,
                                               withStructConf=False,
                                               withRmsd=False)

                for bp in branch:
                    conflict = False

                    altAuthSeqIds = []

                    for authSeqId, labelSeqId in zip(bp['auth_seq_id'], bp['seq_id']):

                        ps = next((ps for ps in polySeq if ps['auth_chain_id'] == bp['auth_chain_id']), None)

                        if ps is None:
                            continue

                        if authSeqId in ps['auth_seq_id'] and labelSeqId not in ps['auth_seq_id']:
                            altAuthSeqIds.append(labelSeqId)

                            if 'ambig_auth_seq_id' not in ps:
                                ps['ambug_auth_seq_id'] = []
                            ps['ambug_auth_seq_id'].append(authSeqId)

                            conflict = True

                        else:
                            altAuthSeqIds.append(authSeqId)

                    if conflict:
                        bp['alt_auth_seq_id'] = altAuthSeqIds

            except KeyError:
                branch = None

    if not testTag:
        if not changed:
            return prevCoordCheck

        return {'polymer_sequence': polySeq,
                'alt_polymer_sequence': altPolySeq,
                'non_polymer': nonPoly,
                'branch': branch}

    modelNumName = None if prevCoordCheck is None or 'model_num_name' not in prevCoordCheck else prevCoordCheck['model_num_name']
    authAsymId = None if prevCoordCheck is None or 'auth_asym_id' not in prevCoordCheck else prevCoordCheck['auth_asym_id']
    authSeqId = None if prevCoordCheck is None or 'auth_seq_id' not in prevCoordCheck else prevCoordCheck['auth_seq_id']
    authAtomId = None if prevCoordCheck is None or 'auth_atom_id' not in prevCoordCheck else prevCoordCheck['auth_atom_id']

    coordAtomSite = None if prevCoordCheck is None or 'coord_atom_site' not in prevCoordCheck else prevCoordCheck['coord_atom_site']
    coordUnobsRes = None if prevCoordCheck is None or 'coord_unobs_res' not in prevCoordCheck else prevCoordCheck['coord_unobs_res']
    labelToAuthSeq = None if prevCoordCheck is None or 'label_to_auth_seq' not in prevCoordCheck else prevCoordCheck['label_to_auth_seq']
    authToLabelSeq = None if prevCoordCheck is None or 'auth_to_label_seq' not in prevCoordCheck else prevCoordCheck['auth_to_label_seq']
    labelToAuthChain = None if prevCoordCheck is None or 'label_to_auth_chain' not in prevCoordCheck else prevCoordCheck['label_to_auth_chain']
    authToLabelChain = None if prevCoordCheck is None or 'auth_to_label_chain' not in prevCoordCheck else prevCoordCheck['auth_to_label_chain']

    try:

        if modelNumName is None:
            modelNumName = 'pdbx_PDB_model_num' if cR.hasItem('atom_site', 'pdbx_PDB_model_num') else 'ndb_model'
        if authAsymId is None:
            authAsymId = 'pdbx_auth_asym_id' if cR.hasItem('atom_site', 'pdbx_auth_asym_id') else 'auth_asym_id'
        if authSeqId is None:
            authSeqId = 'pdbx_auth_seq_id' if cR.hasItem('atom_site', 'pdbx_auth_seq_id') else 'auth_seq_id'
        if authAtomId is None:
            authAtomId = 'pdbx_auth_atom_name' if cR.hasItem('atom_site', 'pdbx_auth_atom_name') else 'auth_atom_id'
        altAuthAtomId = None if authAtomId == 'auth_atom_id' else 'auth_atom_id'

        if coordAtomSite is None or labelToAuthSeq is None or authToLabelSeq is None:
            changed = True

            if len(polySeq) > LEN_MAJOR_ASYM_ID_SET:

                if altAuthAtomId is not None:
                    coord = cR.getDictListWithFilter('atom_site',
                                                     [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                                                      {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                                                      {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                                                      {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                                                      {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                                                      {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'},
                                                      {'name': altAuthAtomId, 'type': 'str', 'alt_name': 'alt_atom_id'},
                                                      {'name': 'type_symbol', 'type': 'str'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int',
                                                       'value': representativeModelId},
                                                      {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')},
                                                      {'name': authAsymId, 'type': 'enum', 'enum': MAJOR_ASYM_ID_SET}
                                                      ])
                else:
                    coord = cR.getDictListWithFilter('atom_site',
                                                     [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                                                      {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                                                      {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                                                      {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                                                      {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                                                      {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'},
                                                      {'name': 'type_symbol', 'type': 'str'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int',
                                                       'value': representativeModelId},
                                                      {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')},
                                                      {'name': authAsymId, 'type': 'enum', 'enum': MAJOR_ASYM_ID_SET}
                                                      ])

            else:

                if altAuthAtomId is not None:
                    coord = cR.getDictListWithFilter('atom_site',
                                                     [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                                                      {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                                                      {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                                                      {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                                                      {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                                                      {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'},
                                                      {'name': altAuthAtomId, 'type': 'str', 'alt_name': 'alt_atom_id'},
                                                      {'name': 'type_symbol', 'type': 'str'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int',
                                                       'value': representativeModelId},
                                                      {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                      ])
                else:
                    coord = cR.getDictListWithFilter('atom_site',
                                                     [{'name': authAsymId, 'type': 'str', 'alt_name': 'chain_id'},
                                                      {'name': 'label_asym_id', 'type': 'str', 'alt_name': 'alt_chain_id'},
                                                      {'name': authSeqId, 'type': 'int', 'alt_name': 'seq_id'},
                                                      {'name': 'label_seq_id', 'type': 'str', 'alt_name': 'alt_seq_id'},
                                                      {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'},
                                                      {'name': authAtomId, 'type': 'str', 'alt_name': 'atom_id'},
                                                      {'name': 'type_symbol', 'type': 'str'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int',
                                                       'value': representativeModelId},
                                                      {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                      ])

            authToLabelChain = {ps['auth_chain_id']: ps['chain_id'] for ps in polySeq}
            labelToAuthChain = {ps['chain_id']: ps['auth_chain_id'] for ps in polySeq}

            coordAtomSite = {}
            labelToAuthSeq = {}
            chainIds = set(c['chain_id'] for c in coord)
            for chainId in chainIds:
                seqIds = set(c['seq_id'] for c in coord if c['chain_id'] == chainId)
                for seqId in seqIds:
                    seqKey = (chainId, seqId)
                    compId = next(c['comp_id'] for c in coord
                                  if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId)
                    atomIds = [c['atom_id'] for c in coord
                               if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                    typeSymbols = [c['type_symbol'] for c in coord
                                   if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                    coordAtomSite[seqKey] = {'comp_id': compId, 'atom_id': atomIds, 'type_symbol': typeSymbols}
                    if altAuthAtomId is not None:
                        altAtomIds = [c['alt_atom_id'] for c in coord
                                      if c['chain_id'] == chainId and c['seq_id'] is not None and c['seq_id'] == seqId]
                        coordAtomSite[seqKey]['alt_atom_id'] = altAtomIds
                    altSeqId = next((c['alt_seq_id'] for c in coord if c['chain_id'] == chainId and c['seq_id'] == seqId), None)
                    if altSeqId is not None and altSeqId.isdigit():
                        labelToAuthSeq[(authToLabelChain[chainId], int(altSeqId))] = seqKey
                    else:
                        labelToAuthSeq[seqKey] = seqKey
            authToLabelSeq = {v: k for k, v in labelToAuthSeq.items()}

        if coordUnobsRes is None:
            coordUnobsRes = {}

            if cR.hasCategory('pdbx_unobs_or_zero_occ_residues'):

                unobs = cR.getDictListWithFilter('pdbx_unobs_or_zero_occ_residues',
                                                 [{'name': 'auth_asym_id', 'type': 'str', 'alt_name': 'chain_id'},
                                                  {'name': 'auth_seq_id', 'type': 'str', 'alt_name': 'seq_id'},
                                                  {'name': 'auth_comp_id', 'type': 'str', 'alt_name': 'comp_id'}
                                                  ],
                                                 [{'name': 'PDB_model_num', 'type': 'int', 'value': representativeModelId}
                                                  ])

                if len(unobs) > 0:
                    chainIds = set(u['chain_id'] for u in unobs)
                    for chainId in chainIds:
                        seqIds = set(int(u['seq_id']) for u in unobs if u['chain_id'] == chainId and u['seq_id'] is not None)
                        for seqId in seqIds:
                            seqKey = (chainId, seqId)
                            compId = next(u['comp_id'] for u in unobs
                                          if u['chain_id'] == chainId and u['seq_id'] is not None and int(u['seq_id']) == seqId)
                            coordUnobsRes[seqKey] = {'comp_id': compId}

                    if any(seqKey for seqKey in coordUnobsRes.keys() if seqKey not in authToLabelSeq):

                        if cR.hasItem('pdbx_unobs_or_zero_occ_residues', 'label_asym_id') and cR.hasItem('pdbx_unobs_or_zero_occ_residues', 'label_seq_id'):

                            unobs = cR.getDictListWithFilter('pdbx_unobs_or_zero_occ_residues',
                                                             [{'name': 'auth_asym_id', 'type': 'str'},
                                                              {'name': 'auth_seq_id', 'type': 'str'},
                                                              {'name': 'label_asym_id', 'type': 'str'},
                                                              {'name': 'label_seq_id', 'type': 'str'}
                                                              ],
                                                             [{'name': 'PDB_model_num', 'type': 'int', 'value': representativeModelId}
                                                              ])

                            if len(unobs) > 0:
                                for u in unobs:
                                    if u['auth_asym_id'] is not None and u['auth_seq_id'] is not None and u['label_asym_id'] is not None and u['label_seq_id'] is not None:
                                        authSeqKey = (u['auth_asym_id'], int(u['auth_seq_id']))
                                        labelSeqKey = (u['label_asym_id'], int(u['label_seq_id']))

                                        if authSeqKey not in authToLabelSeq:
                                            authToLabelSeq[authSeqKey] = labelSeqKey
                                        if labelSeqKey not in labelToAuthSeq:
                                            labelToAuthSeq[labelSeqKey] = authSeqKey

    except Exception as e:
        if verbose:
            log.write(f"+ParserListenerUtil.checkCoordinates() ++ Error  - {str(e)}\n")

    if not changed:
        return prevCoordCheck

    return {'model_num_name': modelNumName,
            'auth_asym_id': authAsymId,
            'auth_seq_id': authSeqId,
            'auth_atom_id': authAtomId,
            'alt_auth_atom_id': altAuthAtomId,
            'polymer_sequence': polySeq,
            'alt_polymer_sequence': altPolySeq,
            'non_polymer': nonPoly,
            'branch': branch,
            'coord_atom_site': coordAtomSite,
            'coord_unobs_res': coordUnobsRes,
            'label_to_auth_seq': labelToAuthSeq,
            'auth_to_label_seq': authToLabelSeq,
            'label_to_auth_chain': labelToAuthChain,
            'auth_to_label_chain': authToLabelChain}


def extendCoordinatesForExactNoes(modelChainIdExt,
                                  polySeq, altPolySeq, coordAtomSite, coordUnobsRes, labelToAuthSeq, authToLabelSeq):
    """ Extend coordinate chains for eNOEs-guided multiple conformers.
    """

    _polySeq = None

    if polySeq is not None:
        _polySeq = copy.copy(polySeq)

        for ps in polySeq:
            if ps['auth_chain_id'] in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    if not any(ps for ps in polySeq if ps['auth_chain_id'] == dstChainId):
                        _ps = copy.copy(ps)
                        _ps['chain_id'] = _ps['auth_chain_id'] = dstChainId
                        _polySeq.append(_ps)

    _altPolySeq = None

    if altPolySeq is not None:
        _altPolySeq = copy.copy(altPolySeq)

        for ps in altPolySeq:
            if ps['auth_chain_id'] in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    if not any(ps for ps in altPolySeq if ps['auth_chain_id'] == dstChainId):
                        _ps = copy.copy(ps)
                        _ps['chain_id'] = _ps['auth_chain_id'] = dstChainId
                        _altPolySeq.append(_ps)

    _coordAtomSite = None

    if coordAtomSite is not None:
        _coordAtomSite = copy.copy(coordAtomSite)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in _coordAtomSite:
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _coordAtomSite:
                                _coordAtomSite[_seqKey] = coordAtomSite[seqKey]

    _coordUnobsRes = None

    if coordUnobsRes is not None:
        _coordUnobsRes = copy.copy(coordUnobsRes)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in coordUnobsRes:
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _coordUnobsRes:
                                _coordUnobsRes[_seqKey] = coordUnobsRes[seqKey]

    _authToLabelSeq = None
    _labelToAuthSeq = None

    if authToLabelSeq is not None:
        _authToLabelSeq = copy.copy(authToLabelSeq)

        for ps in polySeq:
            srcChainId = ps['auth_chain_id']
            if srcChainId in modelChainIdExt:
                for dstChainId in modelChainIdExt[ps['auth_chain_id']]:
                    for seqId in ps['auth_seq_id']:
                        seqKey = (srcChainId, seqId)
                        if seqKey in authToLabelSeq:
                            _seqKey = (dstChainId, seqId)
                            if _seqKey not in _authToLabelSeq:
                                _authToLabelSeq[_seqKey] = (dstChainId, labelToAuthSeq[seqKey][1])

        _labelToAuthSeq = {v: k for k, v in _authToLabelSeq.items()}

    return _polySeq, _altPolySeq, _coordAtomSite, _coordUnobsRes, _labelToAuthSeq, _authToLabelSeq


def isLongRangeRestraint(atoms, polySeq=None):
    """ Return whether restraint is neither an intra residue nor sequential residues.
    """

    chainIds = [a['chain_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) > 1:
        return True

    seqIds = [a['seq_id'] for a in atoms]

    commonSeqId = collections.Counter(seqIds).most_common()

    if len(commonSeqId) == 1:
        return False

    for s1, s2 in itertools.combinations(commonSeqId, 2):
        if abs(s1[0] - s2[0]) > 1:
            if polySeq is None:
                return True

            # verify with label_seq_id scheme

            try:

                ps = next(ps for ps in polySeq if ps['auth_chain_id'] == chainIds[0])

                _seqIds = [ps['seq_id'][ps['auth_seq_id'].index(a['seq_id'])] for a in atoms]
                _commonSeqId = collections.Counter(_seqIds).most_common()
                for _s1, _s2 in itertools.combinations(_commonSeqId, 2):
                    if abs(_s1[0] - _s2[0]) > 1:
                        return True

            except Exception:
                return True

    return False


def isAsymmetricRangeRestraint(atoms, chainIdSet, symmetric):
    """ Return whether restraint is asymmetric.
    """

    lenAtoms = len(atoms)

    if len(set((frozenset(atom.items()) for atom in atoms))) != lenAtoms:  # reject identical atom
        return True

    lenChainIdSet = len(chainIdSet)

    chainIds = [a['chain_id'] for a in atoms]
    indices = [chainIdSet.index(c) for c in chainIds]

    for pos, index in enumerate(indices):
        if pos == lenAtoms - 1:
            break
        if index + 1 < lenChainIdSet:
            nextIndex = index + 1
        elif symmetric == 'circular':
            nextIndex = 0
        else:
            return True
        if indices[pos + 1] != nextIndex:
            return True

    seqIds = [a['seq_id'] for a in atoms]

    commonSeqId = collections.Counter(seqIds).most_common()

    if len(commonSeqId) == 1:
        return False

    for s1, s2 in itertools.combinations(commonSeqId, 2):
        if abs(s1[0] - s2[0]) > 1:
            return True

    return False


def hasIntraChainResraint(atomSelectionSet):
    """ Return whether intra-chain distance restraints in the atom selection.
    """

    for atom1, atom2 in itertools.product(atomSelectionSet[0],
                                          atomSelectionSet[1]):
        if atom1['chain_id'] == atom2['chain_id']:
            return True

    return False


def getTypeOfDihedralRestraint(polypeptide, polynucleotide, carbohydrates, atoms):
    """ Return type of dihedral angle restraint.
    """

    chainIds = [a['chain_id'] for a in atoms]
    seqIds = [a['seq_id'] for a in atoms]
    atomIds = [a['atom_id'] for a in atoms]

    if len(collections.Counter(chainIds).most_common()) > 1:
        return None

    commonSeqId = collections.Counter(seqIds).most_common()

    lenCommonSeqId = len(commonSeqId)

    if polypeptide:

        if lenCommonSeqId == 2:

            phiPsiCommonAtomIds = ['N', 'CA', 'C']

            # PHI or PSI
            if commonSeqId[0][1] == 3 and commonSeqId[1][1] == 1:

                # PHI
                prevSeqId = commonSeqId[1][0]

                if commonSeqId[0][0] == prevSeqId + 1:

                    j = 0
                    if seqIds[j] == prevSeqId and atomIds[j] == 'C':
                        atomIds.pop(j)
                        if atomIds == phiPsiCommonAtomIds:
                            return 'PHI'

                # PSI
                nextSeqId = commonSeqId[1][0]

                if commonSeqId[0][0] == nextSeqId - 1:

                    j = 3
                    if seqIds[j] == nextSeqId and atomIds[j] == 'N':
                        atomIds.pop(j)
                        if atomIds == phiPsiCommonAtomIds:
                            return 'PSI'

            # OMEGA
            if atomIds[0] == 'CA' and atomIds[1] == 'N' and atomIds[2] == 'C' and atomIds[3] == 'CA'\
               and seqIds[0] == seqIds[1] and seqIds[1] - 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

            if atomIds[0] == 'CA' and atomIds[1] == 'C' and atomIds[2] == 'N' and atomIds[3] == 'CA'\
               and seqIds[0] == seqIds[1] and seqIds[1] + 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

            # OMEGA - modified CYANA definition
            if atomIds[0] == 'O' and atomIds[1] == 'C' and atomIds[2] == 'N'\
               and (atomIds[3] == 'H' or atomIds[3] == 'CD')\
               and seqIds[0] == seqIds[1] and seqIds[1] + 1 == seqIds[2] and seqIds[2] == seqIds[3]:
                return 'OMEGA'

        elif lenCommonSeqId == 1:

            testDataType = ['CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                            'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42']

            for dataType in testDataType:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                    if isinstance(angAtomId, str):
                        if atomId != angAtomId:
                            found = False
                            break

                    else:
                        if not angAtomId.match(atomId):
                            found = False
                            break

                if found:
                    return dataType

        testDataType = ['PHI', 'PSI', 'OMEGA',
                        'CHI1', 'CHI2', 'CHI3', 'CHI4', 'CHI5',
                        'CHI21', 'CHI22', 'CHI31', 'CHI32', 'CHI42']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

    elif polynucleotide:

        if lenCommonSeqId == 3:

            # ETA or ETA'
            _seqIds = [s - o for s, o in zip(seqIds, KNOWN_ANGLE_SEQ_OFFSET['ETA'])]
            _commonSeqId = collections.Counter(_seqIds).most_common()

            if len(_commonSeqId) == 1:

                testDataType = ['ETA', "ETA'"]

                for dataType in testDataType:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        elif lenCommonSeqId == 2:

            # ALPHA or EPSILON or ZETA or THETA or or THETA'
            testDataType = ['ALPHA', 'EPSILON', 'ZETA', 'THETA', "THETA'"]

            for dataType in testDataType:
                _seqIds = [s - o for s, o in zip(seqIds, KNOWN_ANGLE_SEQ_OFFSET[dataType])]
                _commonSeqId = collections.Counter(_seqIds).most_common()

                if len(_commonSeqId) == 1:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        elif lenCommonSeqId == 1:

            if 'N1' in atomIds:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']):

                    if atomId != angAtomId:
                        found = False
                        break

                if found:
                    return 'CHI'

            elif 'N9' in atomIds:

                found = True

                for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['R']):

                    if atomId != angAtomId:
                        found = False
                        break

                if found:
                    return 'CHI'

            else:

                # BETA or GAMMA or DELTA or NU0 or NU1 or NU2 or NU4
                testDataType = ['BETA', 'GAMMA', 'DELTA', 'NU0', 'NU1', 'NU2', 'NU3', 'NU4']

                for dataType in testDataType:

                    found = True

                    for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                        if atomId != angAtomId:
                            found = False
                            break

                    if found:
                        return dataType

        testDataType = ['ETA', "ETA'",
                        'ALPHA', 'EPSILON', 'ZETA', 'THETA', "THETA'",
                        'BETA', 'GAMMA', 'DELTA', 'NU0', 'NU1', 'NU2', 'NU3', 'NU4']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

        if 'N1' in atomIds:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['Y']):

                if atomId != angAtomId:
                    found = False
                    break

            if found:
                return None

        elif 'N9' in atomIds:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_ATOM_NAMES['CHI']['R']):

                if atomId != angAtomId:
                    found = False
                    break

            if found:
                return None

    elif carbohydrates:

        if lenCommonSeqId == 2:

            # PHI or PSI or OMEGA
            testDataType = ['PHI', 'PSI', 'OMEGA']

            for dataType in testDataType:
                seqId1 = seqIds[0]
                seqId4 = seqIds[3]

                if seqId1 > seqId4:
                    m = seqId1 - seqId4
                    _seqIds = [s - o * m for s, o in zip(seqIds, KNOWN_ANGLE_CARBO_SEQ_OFFSET[dataType])]
                    _commonSeqId = collections.Counter(_seqIds).most_common()

                    if len(_commonSeqId) == 1:

                        found = True

                        for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_CARBO_ATOM_NAMES[dataType]):

                            if isinstance(angAtomId, str):
                                if atomId != angAtomId:
                                    found = False
                                    break

                            else:
                                if not angAtomId.match(atomId):
                                    found = False
                                    break

                        if found:
                            return dataType

        testDataType = ['PHI', 'PSI', 'OMEGA']

        for dataType in testDataType:

            found = True

            for atomId, angAtomId in zip(atomIds, KNOWN_ANGLE_CARBO_ATOM_NAMES[dataType]):

                if isinstance(angAtomId, str):
                    if atomId != angAtomId:
                        found = False
                        break

                else:
                    if not angAtomId.match(atomId):
                        found = False
                        break

            if found:
                return None

    return '.' if lenCommonSeqId == 1 else None


def startsWithPdbRecord(line):
    """ Return whether a given line string starts with legacy PDB records.
    """

    if any(line.startswith(pdb_record) for pdb_record in LEGACY_PDB_RECORDS):
        return True

    return any(line[:-1] == pdb_record[:-1] for pdb_record in LEGACY_PDB_RECORDS if pdb_record.endswith(' '))


def isCyclicPolymer(cR, polySeq, authAsymId, representativeModelId=1, modelNumName='PDB_model_num'):
    """ Return whether a given chain is cyclic polymer based on coordinate annotation.
    """

    if cR is None or polySeq is None:
        return False

    ps = next((ps for ps in polySeq if ps['auth_chain_id'] == authAsymId), None)

    if ps is None:
        return False

    labelAsymId = ps['chain_id']
    begAuthSeqId = ps['auth_seq_id'][0]
    endAuthSeqId = ps['auth_seq_id'][-1]
    begLabelSeqId = ps['seq_id'][0]
    endLabelSeqId = ps['seq_id'][-1]

    try:

        if cR.hasItem('struct_conn', 'pdbx_leaving_atom_flag'):
            struct_conn = cR.getDictListWithFilter('struct_conn',
                                                   [{'name': 'conn_type_id', 'type': 'str'}
                                                    ],
                                                   [{'name': 'pdbx_leaving_atom_flag', 'type': 'str', 'value': 'both'},
                                                    {'name': 'ptnr1_label_asym_id', 'type': 'str', 'value': labelAsymId},
                                                    {'name': 'ptnr2_label_asym_id', 'type': 'str', 'value': labelAsymId},
                                                    {'name': 'ptnr1_label_seq_id', 'type': 'int', 'value': begLabelSeqId},
                                                    {'name': 'ptnr2_label_seq_id', 'type': 'int', 'value': endLabelSeqId},
                                                    ])
        else:
            struct_conn = cR.getDictListWithFilter('struct_conn',
                                                   [{'name': 'conn_type_id', 'type': 'str'}
                                                    ],
                                                   [{'name': 'ptnr1_label_asym_id', 'type': 'str', 'value': labelAsymId},
                                                    {'name': 'ptnr2_label_asym_id', 'type': 'str', 'value': labelAsymId},
                                                    {'name': 'ptnr1_label_seq_id', 'type': 'int', 'value': begLabelSeqId},
                                                    {'name': 'ptnr2_label_seq_id', 'type': 'int', 'value': endLabelSeqId},
                                                    ])

    except Exception:
        return False

    if len(struct_conn) == 0:

        try:

            close_contact = cR.getDictListWithFilter('pdbx_validate_close_contact',
                                                     [{'name': 'dist', 'type': 'float'}
                                                      ],
                                                     [{'name': modelNumName, 'type': 'int', 'value': representativeModelId},
                                                      {'name': 'auth_asym_id_1', 'type': 'str', 'value': authAsymId},
                                                      {'name': 'auth_seq_id_1', 'type': 'int', 'value': begAuthSeqId},
                                                      {'name': 'auth_atom_id_1', 'type': 'str', 'value': 'N'},
                                                      {'name': 'auth_asym_id_2', 'type': 'str', 'value': authAsymId},
                                                      {'name': 'auth_seq_id_2', 'type': 'int', 'value': endAuthSeqId},
                                                      {'name': 'auth_atom_id_2', 'type': 'str', 'value': 'C'}
                                                      ])

        except Exception:
            return False

        if len(close_contact) == 0:

            bond = getCoordBondLength(cR, labelAsymId, begLabelSeqId, 'N', labelAsymId, endLabelSeqId, 'C', modelNumName)

            if bond is None:
                return False

            distance = next((b['distance'] for b in bond if b['model_id'] == representativeModelId), None)

            if distance is None:
                return False

            return 1.2 < distance < 1.4

        return 1.2 < close_contact[0]['dist'] < 1.4

    return struct_conn[0]['conn_type_id'] == 'covale'


def getCoordBondLength(cR, labelAsymId1, labelSeqId1, labelAtomId1, labelAsymId2, labelSeqId2, labelAtomId2, modelNumName='PDB_model_num'):
    """ Return the bond length of given two CIF atoms.
        @return: the bond length
    """

    try:

        atom_site_1 = cR.getDictListWithFilter('atom_site',
                                               [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                {'name': modelNumName, 'type': 'int', 'alt_name': 'model_id'}
                                                ],
                                               [{'name': 'label_asym_id', 'type': 'str', 'value': labelAsymId1},
                                                {'name': 'label_seq_id', 'type': 'int', 'value': labelSeqId1},
                                                {'name': 'label_atom_id', 'type': 'str', 'value': labelAtomId1},
                                                {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                ])

        atom_site_2 = cR.getDictListWithFilter('atom_site',
                                               [{'name': 'Cartn_x', 'type': 'float', 'alt_name': 'x'},
                                                {'name': 'Cartn_y', 'type': 'float', 'alt_name': 'y'},
                                                {'name': 'Cartn_z', 'type': 'float', 'alt_name': 'z'},
                                                {'name': modelNumName, 'type': 'int', 'alt_name': 'model_id'}
                                                ],
                                               [{'name': 'label_asym_id', 'type': 'str', 'value': labelAsymId2},
                                                {'name': 'label_seq_id', 'type': 'int', 'value': labelSeqId2},
                                                {'name': 'label_atom_id', 'type': 'str', 'value': labelAtomId2},
                                                {'name': 'label_alt_id', 'type': 'enum', 'enum': ('A')}
                                                ])

    except Exception:
        return None

    model_ids = set(a['model_id'] for a in atom_site_1) | set(a['model_id'] for a in atom_site_2)

    bond = []

    for model_id in model_ids:
        a_1 = next((a for a in atom_site_1 if a['model_id'] == model_id), None)
        a_2 = next((a for a in atom_site_2 if a['model_id'] == model_id), None)

        if a_1 is None or a_2 is None:
            continue

        bond.append({'model_id': model_id, 'distance': float(f"{numpy.linalg.norm(toNpArray(a_1) - toNpArray(a_2)):.3f}")})

    if len(bond) > 0:
        return bond

    return None


def getRestraintName(subtype):
    """ Return human-readable restraint name for a given internal content subtype.
    """

    if subtype.startswith('dist'):
        return "Distance restraints"
    if subtype.startswith('dihed'):
        return "Dihedral angle restraints"
    if subtype.startswith('rdc'):
        return "RDC restraints"
    if subtype.startswith('plane'):
        return "Planarity constraints"
    if subtype.startswith('hbond'):
        return "Hydrogen bond restraints"
    if subtype.startswith('ssbond'):
        return "Disulfide bond constraints"
    if subtype.startswith('fchiral'):
        return "Floating chiral stereo assignments"
    if subtype.startswith('adist'):
        return "Anti-distance restraints"
    if subtype.startswith('jcoup'):
        return "Scalar J-coupling restraints"
    if subtype.startswith('hvycs'):
        return "Carbon chemical shift restraints"
    if subtype.startswith('procs'):
        return "Proton chemical shift restraints"
    if subtype.startswith('rama'):
        return "Dihedral angle database restraints"
    if subtype.startswith('radi'):
        return "Radius of gyration restraints"
    if subtype.startswith('diff'):
        return "Diffusion anisotropy restraints"
    if subtype.startswith('nbase'):
        return "Nucleic acid base orientation database restraints"
    if subtype.startswith('csa'):
        return "CSA restraints"
    if subtype.startswith('ang'):
        return "Angle database restraints"
    if subtype.startswith('pre'):
        return "PRE restraints"
    if subtype.startswith('pcs'):
        return "PCS restraints, "
    if subtype.startswith('prdc'):
        return "Paramagnetic RDC restraints"
    if subtype.startswith('pang'):
        return "Paramagnetic orientation restraints"
    if subtype.startswith('pccr'):
        return "Paramagnetic CCR restraints"
    if subtype.startswith('geo'):
        return "Coordinate geometry restraints"
    if subtype.startswith('noepk'):
        return "NOESY peak volume restraints"
    raise KeyError(f'Internal subtype {subtype!r} is not defined.')


def getValidSubType(subtype):
    """ Return legitimate content subtype of NmrDpUtility.py for a given internal content subtype.
    """

    if subtype in ('dist', 'dihed', 'rdc', 'jcoup', 'hvycs', 'procs', 'csa', 'fchical'):
        return subtype + '_restraint'

    if subtype == 'hbond':
        return 'dist_restraint'

    if subtype == 'ssbond':
        return 'dist_restraint'

    if subtype == 'prdc':
        return 'rdc_restraints'

    if subtype == 'pcs':
        return 'csp_restraints'

    if subtype == 'pre':
        return 'auto_realx_restraint'

    if subtype == 'pccr':
        return 'ccr_dd_restraint'

    if subtype in ('plane', 'adist', 'rama', 'radi', 'diff', 'nbase', 'ang', 'pang', 'geo'):
        return 'other_restraint'

    raise KeyError(f'Internal subtype {subtype!r} is not defined.')


def initListIdCounter():
    """ Initialize list id counter.
    """

    return {'dist_restraint': 0,
            'dihed_restraint': 0,
            'rdc_restraint': 0,
            'noepk_restraint': 0,
            'jcoup_restraint': 0,
            'csa_restraint': 0,
            'ddc_restraint': 0,
            'hvycs_restraint': 0,
            'procs_restraint': 0,
            'csp_restraint': 0,
            'auto_relax_restraint': 0,
            'ccr_d_csa_restraint': 0,
            'ccr_dd_restraint': 0,
            'fchiral_restraint': 0,
            'other_restraint': 0
            }


def incListIdCounter(subtype, listIdCounter):
    """ Increment list id counter for a given internal content subtype.
    """

    if len(listIdCounter) == 0:
        listIdCounter = initListIdCounter()

    _subtype = getValidSubType(subtype)

    if _subtype is None or _subtype not in listIdCounter:
        return listIdCounter

    listIdCounter[_subtype] = listIdCounter[_subtype] + 1

    return listIdCounter


def getSaveframe(subtype, sf_framecode, listId=None, entryId=None, fileName=None,
                 constraintType=None, alignCenter=None):
    """ Return pynmrstar saveframe for a given internal content subtype.
        @return: pynmrstar saveframe
    """

    _subtype = getValidSubType(subtype)

    if _subtype is None:
        return None

    if _subtype not in NMR_STAR_SF_CATEGORIES:
        return None

    sf = pynmrstar.Saveframe.from_scratch(sf_framecode)
    sf.set_tag_prefix(NMR_STAR_SF_TAG_PREFIXES[_subtype])

    for sf_tag_item in NMR_STAR_SF_TAG_ITEMS[_subtype]:
        tag_item_name = sf_tag_item['name']

        if tag_item_name == 'Sf_category':
            sf.add_tag(tag_item_name, NMR_STAR_SF_CATEGORIES[_subtype])
        elif tag_item_name == 'Sf_framecode':
            sf.add_tag(tag_item_name, sf_framecode)
        elif tag_item_name == 'ID' and listId is not None:
            sf.add_tag(tag_item_name, listId)
        elif tag_item_name == 'Entry_ID' and entryId is not None:
            sf.add_tag(tag_item_name, entryId)
        elif tag_item_name == 'Data_file_name' and fileName is not None:
            sf.add_tag(tag_item_name, fileName)
        elif tag_item_name == 'Constraint_type' and subtype == 'dist':
            sf.add_tag(tag_item_name, 'NOE')
        elif tag_item_name == 'Constraint_type' and subtype == 'hbond':
            sf.add_tag(tag_item_name, 'hydrogen bond')
        elif tag_item_name == 'Constraint_type' and subtype == 'ssbond':
            sf.add_tag(tag_item_name, 'disulfide bond')
        elif tag_item_name == 'Constraint_type' and constraintType is not None:
            sf.add_tag(tag_item_name, constraintType)
        elif tag_item_name == 'Constraint_type' and subtype == 'rdc':
            sf.add_tag(tag_item_name, 'RDC')
        elif tag_item_name == 'Homonuclear_NOE_val_type' and subtype == 'noepk':
            sf.add_tag(tag_item_name, 'peak volume')
        elif tag_item_name == 'Val_units' and subtype in ('csa', 'pccr'):
            sf.add_tag(tag_item_name, 'ppm')
        elif tag_item_name == 'Units' and subtype in ('hvycs', 'procs'):
            sf.add_tag(tag_item_name, 'ppm')
        elif tag_item_name == 'Type' and subtype == 'pcs':
            sf.add_tag(tag_item_name, 'paramagnetic ligand binding')
        elif tag_item_name == 'Common_relaxation_type_name' and subtype == 'pre':
            sf.add_tag(tag_item_name, 'paramagnetic relaxation enhancement')
        elif tag_item_name == 'Relaxation_coherence_type' and subtype == 'pre':
            sf.add_tag(tag_item_name, "S+")
        elif tag_item_name == 'Relaxation_val_units' and subtype == 'pre':
            sf.add_tag(tag_item_name, 's-1')
        elif tag_item_name == 'Definition' and _subtype == 'other_restraint' and constraintType is not None:
            sf.add_tag(tag_item_name, constraintType)
        elif tag_item_name == 'Tensor_auth_asym_ID' and subtype == 'prdc' and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['chain_id'])
        elif tag_item_name == 'Tensor_auth_seq_ID' and subtype == 'prdc' and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['seq_id'])
        elif tag_item_name == 'Tensor_auth_comp_ID' and subtype == 'prdc' and alignCenter is not None:
            sf.add_tag(tag_item_name, alignCenter['comp_id'])
        else:
            sf.add_tag(tag_item_name, '.')

    return sf


def getLoop(subtype):
    """ Return pynmrstart loop for a given content subtype.
        @return: pynmrstar loop
    """

    _subtype = getValidSubType(subtype)

    if _subtype is None:
        return None

    if _subtype not in NMR_STAR_LP_CATEGORIES:
        return None

    if _subtype == 'other_restraint':
        return {'tag': [], 'data': []}  # dictionary for _Other_data_type_list.Text_data

    prefix = NMR_STAR_LP_CATEGORIES[_subtype] + '.'

    lp = pynmrstar.Loop.from_scratch()

    tags = [prefix + item['name'] for item in NMR_STAR_LP_KEY_ITEMS[_subtype]]
    tags.extend([prefix + item['name'] for item in NMR_STAR_LP_DATA_ITEMS[_subtype]])

    for tag in tags:
        lp.add_tag(tag)

    return lp


def getRow(subtype, id, indexId, combinationId, code, listId, entryId, dstFunc, atom1, atom2=None, atom3=None, atom4=None, atom5=None):
    """ Return row data for a given restraint.
        @return: data array
    """

    _subtype = getValidSubType(subtype)

    if _subtype is None:
        return None

    if _subtype == 'other_restraint':
        return None

    key_size = len(NMR_STAR_LP_KEY_ITEMS)
    data_size = len(NMR_STAR_LP_DATA_ITEMS)

    row = [None] * (key_size + data_size)

    row[0] = id

    if atom1 is not None:
        row[1], row[2], row[3], row[4] = atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
    elif atom2 is not None:  # procs
        row[1], row[2], row[3], row[4] = atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
    elif atom2 is not None:
        row[5], row[6], row[7], row[8] = atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    if subtype in ('dist', 'dihed', 'rdc', 'hbond', 'ssbond'):
        row[key_size] = indexId

    row[-2] = listId
    row[-1] = entryId

    if subtype in ('dist', 'hbond', 'ssbond'):
        row[key_size + 1] = combinationId
        if isinstance(combinationId, int):
            row[key_size + 2] = code
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 3] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 4] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 5] = dstFunc['lower_linear_limit']
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 6] = dstFunc['lower_limit']
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 7] = dstFunc['upper_limit']
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 8] = dstFunc['upper_linear_limit']
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 9] = dstFunc['weight']
        # Distance val

        row[key_size + 11], row[key_size + 12], row[key_size + 13], row[key_size + 14] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 15] = atom1['auth_atom_id']
        row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 20] = atom2['auth_atom_id']

    elif subtype == 'dihed':
        if atom1 is not None:
            row[9], row[10], row[11], row[12] = atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[9], row[10], row[11] = atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom2 is not None:
            row[13], row[14], row[15], row[16] = atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[13], row[14], row[15] = atom5['chain_id'], atom5['seq_id'], atom5['comp_id']

        # row[key_size + 1] = combinationId
        row[key_size + 2] = code
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 3] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 4] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 5] = dstFunc['lower_linear_limit']
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 6] = dstFunc['lower_limit']
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 7] = dstFunc['upper_limit']
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 8] = dstFunc['upper_linear_limit']
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 9] = dstFunc['weight']

        if atom1 is not None:
            row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
            if hasKeyValue(atom1, 'auth_atom_id'):
                row[key_size + 14] = atom1['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 10], row[key_size + 11], row[key_size + 12] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom2 is not None:
            row[key_size + 15], row[key_size + 16], row[key_size + 17], row[key_size + 18] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
            if hasKeyValue(atom2, 'auth_atom_id'):
                row[key_size + 19] = atom2['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 15], row[key_size + 16], row[key_size + 17] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom3 is not None:
            row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
                atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
            if hasKeyValue(atom3, 'auth_atom_id'):
                row[key_size + 24] = atom3['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 20], row[key_size + 21], row[key_size + 22] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']
        if atom4 is not None:
            row[key_size + 25], row[key_size + 26], row[key_size + 27], row[key_size + 28] =\
                atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
            if hasKeyValue(atom4, 'auth_atom_id'):
                row[key_size + 29] = atom4['auth_atom_id']
        elif atom5 is not None:  # PPA, phase angle of pseudorotation
            row[key_size + 25], row[key_size + 26], row[key_size + 27] =\
                atom5['chain_id'], atom5['seq_id'], atom5['comp_id']

    elif subtype == 'rdc':
        # row[key_size + 1] = combinationId
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 3] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'lower_linear_limit'):
            row[key_size + 4] = dstFunc['lower_linear_limit']
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 5] = dstFunc['lower_limit']
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 6] = dstFunc['upper_limit']
        if hasKeyValue(dstFunc, 'upper_linear_limit'):
            row[key_size + 7] = dstFunc['upper_linear_limit']
        if hasKeyValue(dstFunc, 'weight'):
            row[key_size + 8] = dstFunc['weight']
        # Rdc_val
        # Rdc_val_err
        # RDC_val_scale_factor
        # RDC_distance_depedent

        row[key_size + 13], row[key_size + 14], row[key_size + 15], row[key_size + 16] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        if hasKeyValue(atom1, 'auth_atom_id'):
            row[key_size + 17] = atom1['auth_atom_id']
        row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[key_size + 22] = atom2['auth_atom_id']

    elif subtype == 'noepk':
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 1] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 2] = dstFunc['linear_limit']
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 3] = dstFunc['upper_limit']

        row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 8] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 9], row[key_size + 10], row[key_size + 11], row[key_size + 12] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

        if hasKeyValue(atom1, 'auth_atom_id'):
            row[4] = row[key_size + 8] = atom1['auth_atom_id']
        if hasKeyValue(atom2, 'auth_atom_id'):
            row[8] = row[key_size + 12] = atom1['auth_atom_id']

    elif subtype == 'jcoup':
        row[key_size] = code
        row[key_size + 1] = atomType = atom1['atom_id'][0]
        row[key_size + 2] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        # Ambiguity_code_1
        row[key_size + 4] = atomType = atom2['atom_id'][0]
        row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        # Ambiguity_code_2
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 7] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 8] = dstFunc['target_value_uncertainty']
        if hasKeyValue(dstFunc, 'lower_limit'):
            row[key_size + 9] = dstFunc['lower_limit']
        if hasKeyValue(dstFunc, 'upper_limit'):
            row[key_size + 10] = dstFunc['upper_limit']

        row[key_size + 11], row[key_size + 12], row[key_size + 13], row[key_size + 14] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 15], row[key_size + 16], row[key_size + 17], row[key_size + 18] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif subtype == 'csa':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'target_value_uncertainty'):
            row[key_size + 3] = dstFunc['target_value_uncertainty']
        # Principal_value_sigma_11_val
        # Principal_value_sigma_22_val
        # Principal_value_sigma_33_val
        # Principal_Euler_angle_alpha_val
        # Principal_Euler_angle_beta_val
        # Principal_Euler_angle_gamma_val
        # Bond_length

        row[key_size + 11], row[key_size + 12], row[key_size + 13], row[key_size + 14] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif subtype == 'hvycs':
        row[key_size] = dstFunc['ca_shift']
        # CA_chem_shift_val_err
        row[key_size + 2] = dstFunc['cb_shift']
        # CB_chem_shift_val_err
        row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 8], row[key_size + 9], row[key_size + 10], row[key_size + 11] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']
        row[key_size + 12], row[key_size + 13], row[key_size + 14], row[key_size + 15] =\
            atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        row[key_size + 16], row[key_size + 17], row[key_size + 18], row[key_size + 19] =\
            atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']
        row[key_size + 20], row[key_size + 21], row[key_size + 22], row[key_size + 23] =\
            atom5['chain_id'], atom5['seq_id'], atom5['comp_id'], atom5['atom_id']

    elif subtype == 'procs':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        row[key_size + 2] = dstFunc['obs_value'] if atom2 is None else dstFunc['obs_value_2']
        # Chem_shift_val_err

        if atom2 is None:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        else:
            row[key_size + 4], row[key_size + 5], row[key_size + 6], row[key_size + 7] =\
                atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif subtype == 'pcs':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        # Chem_shift_val
        # Chem_shift_val_err
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 4] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 5] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0

        row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif subtype == 'pre':
        row[key_size] = atomType = atom1['atom_id'][0]
        row[key_size + 1] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 2] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 3] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0
        # Rex_val
        # Rex_val_err

        row[key_size + 6], row[key_size + 7], row[key_size + 8], row[key_size + 9] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    elif subtype == 'fchiral':
        row[key_size] = code
        row[key_size + 1], row[key_size + 2], row[key_size + 3], row[key_size + 4] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 5], row[key_size + 6], row[key_size + 7], row[key_size + 8] =\
            atom2['chain_id'], atom2['seq_id'], atom2['comp_id'], atom2['atom_id']

    elif subtype == 'pccr':
        row[9], row[10], row[11], row[12] = atom3['chain_id'], atom3['seq_id'], atom3['comp_id'], atom3['atom_id']
        row[13], row[14], row[15], row[16] = atom4['chain_id'], atom4['seq_id'], atom4['comp_id'], atom4['atom_id']

        row[key_size] = atom1['atom_id']
        # Dipole_1_atom_isotope_number_1
        # Dipole_1_atom_type_2
        # Dipole_1_atom_isotope_number_2
        row[key_size + 4] = atomType = atom3['atom_id'][0]
        row[key_size + 5] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        row[key_size + 6] = atomType = atom4['atom_id'][0]
        row[key_size + 7] = ISOTOPE_NUMBERS_OF_NMR_OBS_NUCS[atomType][0]
        if hasKeyValue(dstFunc, 'target_value'):
            row[key_size + 8] = dstFunc['target_value']
        if hasKeyValue(dstFunc, 'lower_value') and hasKeyValue(dstFunc, 'upper_value'):
            row[key_size + 9] = (dstFunc['upper_value'] - dstFunc['lower_value']) / 2.0

        row[key_size + 10], row[key_size + 11], row[key_size + 12], row[key_size + 13] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        # Dipole_1_auth_entity_assembly_ID_2
        # Dipole_1_auth_seq_ID_2
        # Dipole_1_auth_comp_ID_2
        # Dipole_1_auth_atom_ID_2
        row[key_size + 18], row[key_size + 19], row[key_size + 20], row[key_size + 21] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']
        row[key_size + 22], row[key_size + 23], row[key_size + 24], row[key_size + 25] =\
            atom1['chain_id'], atom1['seq_id'], atom1['comp_id'], atom1['atom_id']

    return row


def hasKeyValue(d=None, key=None):
    """ Return whether a given dictionary has effective value for a key.
        @return: True if d[key] has effective value, False otherwise
    """

    if d is None or key is None:
        return False

    if key in d:
        return not d[key] is None

    return False
