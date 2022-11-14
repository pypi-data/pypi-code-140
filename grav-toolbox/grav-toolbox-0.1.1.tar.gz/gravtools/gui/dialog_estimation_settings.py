# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gravtools/gui/dialog_estimation_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_estimation_settings(object):
    def setupUi(self, Dialog_estimation_settings):
        Dialog_estimation_settings.setObjectName("Dialog_estimation_settings")
        Dialog_estimation_settings.resize(589, 599)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog_estimation_settings)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget_estimation_settings = QtWidgets.QTabWidget(Dialog_estimation_settings)
        self.tabWidget_estimation_settings.setEnabled(True)
        self.tabWidget_estimation_settings.setObjectName("tabWidget_estimation_settings")
        self.tab_general_settings = QtWidgets.QWidget()
        self.tab_general_settings.setObjectName("tab_general_settings")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_general_settings)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_adjustment_settings = QtWidgets.QGroupBox(self.tab_general_settings)
        self.groupBox_adjustment_settings.setObjectName("groupBox_adjustment_settings")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_adjustment_settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_adjustment_settings)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox_adjustment_method = QtWidgets.QComboBox(self.groupBox_adjustment_settings)
        self.comboBox_adjustment_method.setObjectName("comboBox_adjustment_method")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_adjustment_method)
        self.label_5 = QtWidgets.QLabel(self.groupBox_adjustment_settings)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_comment = QtWidgets.QLineEdit(self.groupBox_adjustment_settings)
        self.lineEdit_comment.setObjectName("lineEdit_comment")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_comment)
        self.verticalLayout.addLayout(self.formLayout)
        self.checkBox_iterative_s0_scaling = QtWidgets.QCheckBox(self.groupBox_adjustment_settings)
        self.checkBox_iterative_s0_scaling.setChecked(False)
        self.checkBox_iterative_s0_scaling.setObjectName("checkBox_iterative_s0_scaling")
        self.verticalLayout.addWidget(self.checkBox_iterative_s0_scaling)
        self.verticalLayout_8.addWidget(self.groupBox_adjustment_settings)
        self.groupBox_parameters = QtWidgets.QGroupBox(self.tab_general_settings)
        self.groupBox_parameters.setObjectName("groupBox_parameters")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_parameters)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_parameters)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spinBox_degree_drift_polynomial = QtWidgets.QSpinBox(self.groupBox_parameters)
        self.spinBox_degree_drift_polynomial.setMinimum(1)
        self.spinBox_degree_drift_polynomial.setMaximum(3)
        self.spinBox_degree_drift_polynomial.setProperty("value", 1)
        self.spinBox_degree_drift_polynomial.setObjectName("spinBox_degree_drift_polynomial")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_degree_drift_polynomial)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.verticalLayout_8.addWidget(self.groupBox_parameters)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem)
        self.tabWidget_estimation_settings.addTab(self.tab_general_settings, "")
        self.tab_advanced_settings = QtWidgets.QWidget()
        self.tab_advanced_settings.setObjectName("tab_advanced_settings")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_advanced_settings)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_constraints = QtWidgets.QGroupBox(self.tab_advanced_settings)
        self.groupBox_constraints.setObjectName("groupBox_constraints")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_constraints)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_constraints)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.doubleSpinBox_weight_factor_datum = QtWidgets.QDoubleSpinBox(self.groupBox_constraints)
        self.doubleSpinBox_weight_factor_datum.setDecimals(1)
        self.doubleSpinBox_weight_factor_datum.setMaximum(1000000.0)
        self.doubleSpinBox_weight_factor_datum.setProperty("value", 1.0)
        self.doubleSpinBox_weight_factor_datum.setObjectName("doubleSpinBox_weight_factor_datum")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_weight_factor_datum)
        self.doubleSpinBox_sig0 = QtWidgets.QDoubleSpinBox(self.groupBox_constraints)
        self.doubleSpinBox_sig0.setMaximum(1000000.0)
        self.doubleSpinBox_sig0.setProperty("value", 1.0)
        self.doubleSpinBox_sig0.setObjectName("doubleSpinBox_sig0")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_sig0)
        self.label_sig0 = QtWidgets.QLabel(self.groupBox_constraints)
        self.label_sig0.setObjectName("label_sig0")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_sig0)
        self.verticalLayout_4.addLayout(self.formLayout_3)
        self.verticalLayout_9.addWidget(self.groupBox_constraints)
        self.groupBox_observations = QtWidgets.QGroupBox(self.tab_advanced_settings)
        self.groupBox_observations.setObjectName("groupBox_observations")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_observations)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_2 = QtWidgets.QLabel(self.groupBox_observations)
        self.label_2.setObjectName("label_2")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.doubleSpinBox_add_const_sd = QtWidgets.QDoubleSpinBox(self.groupBox_observations)
        self.doubleSpinBox_add_const_sd.setDecimals(1)
        self.doubleSpinBox_add_const_sd.setMinimum(-100.0)
        self.doubleSpinBox_add_const_sd.setObjectName("doubleSpinBox_add_const_sd")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_add_const_sd)
        self.label_8 = QtWidgets.QLabel(self.groupBox_observations)
        self.label_8.setObjectName("label_8")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.doubleSpinBox_mult_factor_sd = QtWidgets.QDoubleSpinBox(self.groupBox_observations)
        self.doubleSpinBox_mult_factor_sd.setDecimals(1)
        self.doubleSpinBox_mult_factor_sd.setProperty("value", 1.0)
        self.doubleSpinBox_mult_factor_sd.setObjectName("doubleSpinBox_mult_factor_sd")
        self.formLayout_6.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_mult_factor_sd)
        self.verticalLayout_7.addLayout(self.formLayout_6)
        self.verticalLayout_9.addWidget(self.groupBox_observations)
        self.groupBox_statistical_tests = QtWidgets.QGroupBox(self.tab_advanced_settings)
        self.groupBox_statistical_tests.setObjectName("groupBox_statistical_tests")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_statistical_tests)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_statistical_tests)
        self.label_6.setObjectName("label_6")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.doubleSpinBox_conf_level_chi = QtWidgets.QDoubleSpinBox(self.groupBox_statistical_tests)
        self.doubleSpinBox_conf_level_chi.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.doubleSpinBox_conf_level_chi.setMaximum(1.0)
        self.doubleSpinBox_conf_level_chi.setSingleStep(0.01)
        self.doubleSpinBox_conf_level_chi.setProperty("value", 0.95)
        self.doubleSpinBox_conf_level_chi.setObjectName("doubleSpinBox_conf_level_chi")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_conf_level_chi)
        self.label_7 = QtWidgets.QLabel(self.groupBox_statistical_tests)
        self.label_7.setObjectName("label_7")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.doubleSpinBox_conf_level_tau = QtWidgets.QDoubleSpinBox(self.groupBox_statistical_tests)
        self.doubleSpinBox_conf_level_tau.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.doubleSpinBox_conf_level_tau.setMaximum(1.0)
        self.doubleSpinBox_conf_level_tau.setSingleStep(0.01)
        self.doubleSpinBox_conf_level_tau.setProperty("value", 0.95)
        self.doubleSpinBox_conf_level_tau.setObjectName("doubleSpinBox_conf_level_tau")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_conf_level_tau)
        self.verticalLayout_6.addLayout(self.formLayout_5)
        self.verticalLayout_9.addWidget(self.groupBox_statistical_tests)
        self.groupBox_drift_polynomial_advanced = QtWidgets.QGroupBox(self.tab_advanced_settings)
        self.groupBox_drift_polynomial_advanced.setObjectName("groupBox_drift_polynomial_advanced")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.groupBox_drift_polynomial_advanced)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_drift_polynomial_advanced)
        self.label_10.setObjectName("label_10")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.radioButton_drift_ref_epoch_first_ob_campaign = QtWidgets.QRadioButton(self.groupBox_drift_polynomial_advanced)
        self.radioButton_drift_ref_epoch_first_ob_campaign.setObjectName("radioButton_drift_ref_epoch_first_ob_campaign")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog_estimation_settings)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton_drift_ref_epoch_first_ob_campaign)
        self.verticalLayout_13.addWidget(self.radioButton_drift_ref_epoch_first_ob_campaign)
        self.radioButton_drift_ref_epoch_first_obs_survey = QtWidgets.QRadioButton(self.groupBox_drift_polynomial_advanced)
        self.radioButton_drift_ref_epoch_first_obs_survey.setChecked(True)
        self.radioButton_drift_ref_epoch_first_obs_survey.setObjectName("radioButton_drift_ref_epoch_first_obs_survey")
        self.buttonGroup.addButton(self.radioButton_drift_ref_epoch_first_obs_survey)
        self.verticalLayout_13.addWidget(self.radioButton_drift_ref_epoch_first_obs_survey)
        self.formLayout_9.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.verticalLayout_13)
        self.verticalLayout_14.addLayout(self.formLayout_9)
        self.verticalLayout_9.addWidget(self.groupBox_drift_polynomial_advanced)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem1)
        self.tabWidget_estimation_settings.addTab(self.tab_advanced_settings, "")
        self.tab_iterativ_scaling = QtWidgets.QWidget()
        self.tab_iterativ_scaling.setObjectName("tab_iterativ_scaling")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.tab_iterativ_scaling)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.groupBox_iterative_scaling = QtWidgets.QGroupBox(self.tab_iterativ_scaling)
        self.groupBox_iterative_scaling.setObjectName("groupBox_iterative_scaling")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_iterative_scaling)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_9 = QtWidgets.QLabel(self.groupBox_iterative_scaling)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.comboBox_iteration_approach = QtWidgets.QComboBox(self.groupBox_iterative_scaling)
        self.comboBox_iteration_approach.setObjectName("comboBox_iteration_approach")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_iteration_approach)
        self.label_target_s02 = QtWidgets.QLabel(self.groupBox_iterative_scaling)
        self.label_target_s02.setObjectName("label_target_s02")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_target_s02)
        self.doubleSpinBox_target_s02 = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling)
        self.doubleSpinBox_target_s02.setProperty("value", 1.0)
        self.doubleSpinBox_target_s02.setObjectName("doubleSpinBox_target_s02")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_target_s02)
        self.label_delta_target_s02 = QtWidgets.QLabel(self.groupBox_iterative_scaling)
        self.label_delta_target_s02.setObjectName("label_delta_target_s02")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_delta_target_s02)
        self.doubleSpinBox_delta_target_s02 = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling)
        self.doubleSpinBox_delta_target_s02.setMaximum(10.0)
        self.doubleSpinBox_delta_target_s02.setSingleStep(0.1)
        self.doubleSpinBox_delta_target_s02.setProperty("value", 0.1)
        self.doubleSpinBox_delta_target_s02.setObjectName("doubleSpinBox_delta_target_s02")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_delta_target_s02)
        self.label_max_number_of_iterations = QtWidgets.QLabel(self.groupBox_iterative_scaling)
        self.label_max_number_of_iterations.setObjectName("label_max_number_of_iterations")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_max_number_of_iterations)
        self.spinBox_max_number_of_iterations = QtWidgets.QSpinBox(self.groupBox_iterative_scaling)
        self.spinBox_max_number_of_iterations.setMinimum(1)
        self.spinBox_max_number_of_iterations.setMaximum(100)
        self.spinBox_max_number_of_iterations.setProperty("value", 10)
        self.spinBox_max_number_of_iterations.setObjectName("spinBox_max_number_of_iterations")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox_max_number_of_iterations)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        self.groupBox_iterative_scaling_multiplicative = QtWidgets.QGroupBox(self.groupBox_iterative_scaling)
        self.groupBox_iterative_scaling_multiplicative.setObjectName("groupBox_iterative_scaling_multiplicative")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_iterative_scaling_multiplicative)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_initial_step_size_percent = QtWidgets.QLabel(self.groupBox_iterative_scaling_multiplicative)
        self.label_initial_step_size_percent.setObjectName("label_initial_step_size_percent")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_initial_step_size_percent)
        self.doubleSpinBox_initial_step_size_percent = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling_multiplicative)
        self.doubleSpinBox_initial_step_size_percent.setDecimals(1)
        self.doubleSpinBox_initial_step_size_percent.setMinimum(0.0)
        self.doubleSpinBox_initial_step_size_percent.setProperty("value", 20.0)
        self.doubleSpinBox_initial_step_size_percent.setObjectName("doubleSpinBox_initial_step_size_percent")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_initial_step_size_percent)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling_multiplicative)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setDecimals(1)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setMinimum(100.0)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setMaximum(900.0)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setProperty("value", 200.0)
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setObjectName("doubleSpinBox_max_multiplicative_factor_to_sd_percent")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_max_multiplicative_factor_to_sd_percent)
        self.label_max_multiplicative_factor_to_sd_percent = QtWidgets.QLabel(self.groupBox_iterative_scaling_multiplicative)
        self.label_max_multiplicative_factor_to_sd_percent.setObjectName("label_max_multiplicative_factor_to_sd_percent")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_max_multiplicative_factor_to_sd_percent)
        self.label_min_multiplicative_factor_to_sd_percent = QtWidgets.QLabel(self.groupBox_iterative_scaling_multiplicative)
        self.label_min_multiplicative_factor_to_sd_percent.setObjectName("label_min_multiplicative_factor_to_sd_percent")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_min_multiplicative_factor_to_sd_percent)
        self.doubleSpinBox_min_multiplicative_factor_to_sd_percent = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling_multiplicative)
        self.doubleSpinBox_min_multiplicative_factor_to_sd_percent.setMinimum(1.0)
        self.doubleSpinBox_min_multiplicative_factor_to_sd_percent.setMaximum(100.0)
        self.doubleSpinBox_min_multiplicative_factor_to_sd_percent.setProperty("value", 50.0)
        self.doubleSpinBox_min_multiplicative_factor_to_sd_percent.setObjectName("doubleSpinBox_min_multiplicative_factor_to_sd_percent")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_min_multiplicative_factor_to_sd_percent)
        self.verticalLayout_12.addLayout(self.formLayout_8)
        self.verticalLayout_5.addWidget(self.groupBox_iterative_scaling_multiplicative)
        self.groupBox_iterative_scaling_additive = QtWidgets.QGroupBox(self.groupBox_iterative_scaling)
        self.groupBox_iterative_scaling_additive.setObjectName("groupBox_iterative_scaling_additive")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_iterative_scaling_additive)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_initial_setp_size = QtWidgets.QLabel(self.groupBox_iterative_scaling_additive)
        self.label_initial_setp_size.setObjectName("label_initial_setp_size")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_initial_setp_size)
        self.doubleSpinBox_initial_step_size = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling_additive)
        self.doubleSpinBox_initial_step_size.setMinimum(0.0)
        self.doubleSpinBox_initial_step_size.setMaximum(100.0)
        self.doubleSpinBox_initial_step_size.setProperty("value", 5.0)
        self.doubleSpinBox_initial_step_size.setObjectName("doubleSpinBox_initial_step_size")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_initial_step_size)
        self.doubleSpinBox_max_additive_const_to_sd = QtWidgets.QDoubleSpinBox(self.groupBox_iterative_scaling_additive)
        self.doubleSpinBox_max_additive_const_to_sd.setMaximum(900.0)
        self.doubleSpinBox_max_additive_const_to_sd.setProperty("value", 20.0)
        self.doubleSpinBox_max_additive_const_to_sd.setObjectName("doubleSpinBox_max_additive_const_to_sd")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_max_additive_const_to_sd)
        self.label_max_additive_const_to_sd = QtWidgets.QLabel(self.groupBox_iterative_scaling_additive)
        self.label_max_additive_const_to_sd.setObjectName("label_max_additive_const_to_sd")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_max_additive_const_to_sd)
        self.verticalLayout_11.addLayout(self.formLayout_7)
        self.verticalLayout_5.addWidget(self.groupBox_iterative_scaling_additive)
        self.verticalLayout_10.addWidget(self.groupBox_iterative_scaling)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem2)
        self.tabWidget_estimation_settings.addTab(self.tab_iterativ_scaling, "")
        self.tab_vg_estimation = QtWidgets.QWidget()
        self.tab_vg_estimation.setObjectName("tab_vg_estimation")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.tab_vg_estimation)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.groupBox_vg_polynomial = QtWidgets.QGroupBox(self.tab_vg_estimation)
        self.groupBox_vg_polynomial.setObjectName("groupBox_vg_polynomial")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_vg_polynomial)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_vg_polynomial_degree = QtWidgets.QLabel(self.groupBox_vg_polynomial)
        self.label_vg_polynomial_degree.setObjectName("label_vg_polynomial_degree")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_vg_polynomial_degree)
        self.spinBox_vg_polynomial_degree = QtWidgets.QSpinBox(self.groupBox_vg_polynomial)
        self.spinBox_vg_polynomial_degree.setMinimum(1)
        self.spinBox_vg_polynomial_degree.setMaximum(3)
        self.spinBox_vg_polynomial_degree.setObjectName("spinBox_vg_polynomial_degree")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox_vg_polynomial_degree)
        self.label_vg_polynomial_ref_height_offset_m = QtWidgets.QLabel(self.groupBox_vg_polynomial)
        self.label_vg_polynomial_ref_height_offset_m.setObjectName("label_vg_polynomial_ref_height_offset_m")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_vg_polynomial_ref_height_offset_m)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m = QtWidgets.QDoubleSpinBox(self.groupBox_vg_polynomial)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setDecimals(3)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setMaximum(99.999)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setSingleStep(0.001)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setObjectName("doubleSpinBox_vg_polynomial_ref_height_offset_m")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBox_vg_polynomial_ref_height_offset_m)
        self.verticalLayout_15.addLayout(self.formLayout_10)
        self.verticalLayout_16.addWidget(self.groupBox_vg_polynomial)
        spacerItem3 = QtWidgets.QSpacerItem(20, 419, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_16.addItem(spacerItem3)
        self.tabWidget_estimation_settings.addTab(self.tab_vg_estimation, "")
        self.verticalLayout_3.addWidget(self.tabWidget_estimation_settings)

        self.retranslateUi(Dialog_estimation_settings)
        self.tabWidget_estimation_settings.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog_estimation_settings)

    def retranslateUi(self, Dialog_estimation_settings):
        _translate = QtCore.QCoreApplication.translate
        Dialog_estimation_settings.setWindowTitle(_translate("Dialog_estimation_settings", "Estimation settings"))
        self.groupBox_adjustment_settings.setTitle(_translate("Dialog_estimation_settings", "Adjustment settings"))
        self.label.setToolTip(_translate("Dialog_estimation_settings", "Adjustment method."))
        self.label.setText(_translate("Dialog_estimation_settings", "Method"))
        self.comboBox_adjustment_method.setToolTip(_translate("Dialog_estimation_settings", "Adjustment method."))
        self.label_5.setToolTip(_translate("Dialog_estimation_settings", "Optional comment on the LSM run."))
        self.label_5.setText(_translate("Dialog_estimation_settings", "Comment"))
        self.lineEdit_comment.setToolTip(_translate("Dialog_estimation_settings", "Optional comment on the LSM run."))
        self.checkBox_iterative_s0_scaling.setText(_translate("Dialog_estimation_settings", "Adjust SD of setup observations to scale a posteriori s0"))
        self.groupBox_parameters.setTitle(_translate("Dialog_estimation_settings", "Estimated general parameters"))
        self.label_4.setToolTip(_translate("Dialog_estimation_settings", "Degree of the drift polynomial estimated for each survey."))
        self.label_4.setText(_translate("Dialog_estimation_settings", "Degree of drift Polynomials"))
        self.spinBox_degree_drift_polynomial.setToolTip(_translate("Dialog_estimation_settings", "Degree of the drift polynomial estimated for each survey."))
        self.tabWidget_estimation_settings.setTabText(self.tabWidget_estimation_settings.indexOf(self.tab_general_settings), _translate("Dialog_estimation_settings", "General settings"))
        self.groupBox_constraints.setTitle(_translate("Dialog_estimation_settings", "Datum constraints and weighting"))
        self.label_3.setToolTip(_translate("Dialog_estimation_settings", "Weight factor for datum constraints: The standard deviation of g at datum stations is divided by this factr in order to adjust the weights of the pseudo observations introduced as datum constraints."))
        self.label_3.setText(_translate("Dialog_estimation_settings", "Weight factor for datum"))
        self.doubleSpinBox_weight_factor_datum.setToolTip(_translate("Dialog_estimation_settings", "Weight factor for datum constraints: The standard deviation of g at datum stations is divided by this factr in order to adjust the weights of the pseudo observations introduced as datum constraints."))
        self.doubleSpinBox_sig0.setToolTip(_translate("Dialog_estimation_settings", "A priori standard deviation of the unit weight. The covariance matrix of observations including constraints (Sig_ll) will be divided by sig0²!"))
        self.label_sig0.setToolTip(_translate("Dialog_estimation_settings", "A priori standard deviation of the unit weight. The covariance matrix of observations including constraints (Sig_ll) will be divided by sig0²!"))
        self.label_sig0.setText(_translate("Dialog_estimation_settings", "A priori Sig0 [µGal]"))
        self.groupBox_observations.setTitle(_translate("Dialog_estimation_settings", "Manipulation of a priori SD of setup observations"))
        self.label_2.setToolTip(_translate("Dialog_estimation_settings", "The defined additive constant is added to the standard deviation (SD) of setup observations in order to scale the SD and the resulting weights to realistic values. The multiplicative scaling factor is applied first!"))
        self.label_2.setText(_translate("Dialog_estimation_settings", "Additive const. to SD [µGal]"))
        self.doubleSpinBox_add_const_sd.setToolTip(_translate("Dialog_estimation_settings", "The defined additive constant is added to the standard deviation (SD) of setup observations in order to scale the SD and the resulting weights to realistic values. The multiplicative scaling factor is applied first!"))
        self.label_8.setToolTip(_translate("Dialog_estimation_settings", "Multiplicative factor for scaling the standard deviation (SD) of setup observations."))
        self.label_8.setText(_translate("Dialog_estimation_settings", "Multiplicative factor for SD"))
        self.doubleSpinBox_mult_factor_sd.setToolTip(_translate("Dialog_estimation_settings", "Multiplicative factor for scaling the standard deviation (SD) of setup observations."))
        self.groupBox_statistical_tests.setTitle(_translate("Dialog_estimation_settings", "Statistical tests"))
        self.label_6.setToolTip(_translate("Dialog_estimation_settings", "Confidence level for the goodness-of-fit test (Chi²)."))
        self.label_6.setText(_translate("Dialog_estimation_settings", "Confidence level Chi²-test"))
        self.doubleSpinBox_conf_level_chi.setToolTip(_translate("Dialog_estimation_settings", "Confidence level for the goodness-of-fit test (Chi²)."))
        self.label_7.setToolTip(_translate("Dialog_estimation_settings", "Confidence level for the outlier detection test (tau-test)."))
        self.label_7.setText(_translate("Dialog_estimation_settings", "Confidence level tau-test"))
        self.doubleSpinBox_conf_level_tau.setToolTip(_translate("Dialog_estimation_settings", "Confidence level for the outlier detection test (tau-test)."))
        self.groupBox_drift_polynomial_advanced.setTitle(_translate("Dialog_estimation_settings", "Drift Polynomial"))
        self.label_10.setToolTip(_translate("Dialog_estimation_settings", "The refernce epoch for the estimated drift polynomials (one per survey) is either the epoch of the first observation on the campaign (same reference epoch for all surveys) or of the first observat in each survey of the campaign (different for each survey)."))
        self.label_10.setText(_translate("Dialog_estimation_settings", "Reference epoch t0"))
        self.radioButton_drift_ref_epoch_first_ob_campaign.setToolTip(_translate("Dialog_estimation_settings", "The epoch of the first observation in campaign is the reference epoch for the estimate drift polynomials for ALL surveys in the campaign. "))
        self.radioButton_drift_ref_epoch_first_ob_campaign.setText(_translate("Dialog_estimation_settings", "First observation in campaign"))
        self.radioButton_drift_ref_epoch_first_obs_survey.setToolTip(_translate("Dialog_estimation_settings", "The epoch of the first observation in each survey is used as reference epoch for the estimated drift polynomial (different for each survey in the campaign)."))
        self.radioButton_drift_ref_epoch_first_obs_survey.setText(_translate("Dialog_estimation_settings", "First observation of survey"))
        self.tabWidget_estimation_settings.setTabText(self.tabWidget_estimation_settings.indexOf(self.tab_advanced_settings), _translate("Dialog_estimation_settings", "Advanced  settings"))
        self.groupBox_iterative_scaling.setTitle(_translate("Dialog_estimation_settings", "Iterative scaling of SD of setup observations"))
        self.label_9.setToolTip(_translate("Dialog_estimation_settings", "Iteration approach."))
        self.label_9.setText(_translate("Dialog_estimation_settings", "Iteration approach"))
        self.comboBox_iteration_approach.setToolTip(_translate("Dialog_estimation_settings", "Iteration approach."))
        self.label_target_s02.setToolTip(_translate("Dialog_estimation_settings", "Target variance of unit weight for the iteration."))
        self.label_target_s02.setText(_translate("Dialog_estimation_settings", "Target s0² [ µGal²]"))
        self.doubleSpinBox_target_s02.setToolTip(_translate("Dialog_estimation_settings", "Target variance of unit weight for the iteration."))
        self.label_delta_target_s02.setToolTip(_translate("Dialog_estimation_settings", "Permitted deviation of the target variance of unit weight."))
        self.label_delta_target_s02.setText(_translate("Dialog_estimation_settings", "Delta target s0² [ µGal²]"))
        self.doubleSpinBox_delta_target_s02.setToolTip(_translate("Dialog_estimation_settings", "Permitted deviation of the target variance of unit weight."))
        self.label_max_number_of_iterations.setToolTip(_translate("Dialog_estimation_settings", "Maximum number of iterations."))
        self.label_max_number_of_iterations.setText(_translate("Dialog_estimation_settings", "Max. number of iterations"))
        self.spinBox_max_number_of_iterations.setToolTip(_translate("Dialog_estimation_settings", "Maximum number of iterations."))
        self.groupBox_iterative_scaling_multiplicative.setToolTip(_translate("Dialog_estimation_settings", "Settings for the multiplicative iteration approach."))
        self.groupBox_iterative_scaling_multiplicative.setTitle(_translate("Dialog_estimation_settings", "Multiplicative approach"))
        self.label_initial_step_size_percent.setToolTip(_translate("Dialog_estimation_settings", "Intial step size [%] for the iterative scaling of the SD of all setup observations when applying the multiplicative iteration approach."))
        self.label_initial_step_size_percent.setText(_translate("Dialog_estimation_settings", "Initial iteration step size [%]"))
        self.doubleSpinBox_initial_step_size_percent.setToolTip(_translate("Dialog_estimation_settings", "Intial step size [%] for the iterative scaling of the SD of all setup observations when applying the multiplicative iteration approach."))
        self.doubleSpinBox_max_multiplicative_factor_to_sd_percent.setToolTip(_translate("Dialog_estimation_settings", "Maximum multiplicative factor when scaling the SD of all setup observations wehen using the multiplicative iteration approach."))
        self.label_max_multiplicative_factor_to_sd_percent.setToolTip(_translate("Dialog_estimation_settings", "Maximum multiplicative factor when scaling the SD of all setup observations wehen using the multiplicative iteration approach."))
        self.label_max_multiplicative_factor_to_sd_percent.setText(_translate("Dialog_estimation_settings", "Max. multiplicative factor to SD [%]"))
        self.label_min_multiplicative_factor_to_sd_percent.setText(_translate("Dialog_estimation_settings", "Min. multiplicative factor to SD [%]"))
        self.groupBox_iterative_scaling_additive.setToolTip(_translate("Dialog_estimation_settings", "Settings for the additive iteration approach."))
        self.groupBox_iterative_scaling_additive.setTitle(_translate("Dialog_estimation_settings", "Additive approach"))
        self.label_initial_setp_size.setToolTip(_translate("Dialog_estimation_settings", "The initial iteration setp size defines how much the SD of all setup observationa is changed initially. Within the iteration process this step size may become smaller in order to reach the s0² target."))
        self.label_initial_setp_size.setText(_translate("Dialog_estimation_settings", "Initial iteration step size [µGal]"))
        self.doubleSpinBox_initial_step_size.setToolTip(_translate("Dialog_estimation_settings", "The initial iteration setp size defines how much the SD of all setup observationa is changed initially. Within the iteration process this step size may become smaller in order to reach the s0² target."))
        self.doubleSpinBox_max_additive_const_to_sd.setToolTip(_translate("Dialog_estimation_settings", "Definines the maximim permitted additive constant to the standard deviations of the setup observations at the end of the iteration process."))
        self.label_max_additive_const_to_sd.setToolTip(_translate("Dialog_estimation_settings", "Definines the maximim permitted additive constant to the standard deviations of the setup observations at the end of the iteration process."))
        self.label_max_additive_const_to_sd.setText(_translate("Dialog_estimation_settings", "Max. additive const. to SD [µGal]"))
        self.tabWidget_estimation_settings.setTabText(self.tabWidget_estimation_settings.indexOf(self.tab_iterativ_scaling), _translate("Dialog_estimation_settings", "Iterative Scaling"))
        self.groupBox_vg_polynomial.setToolTip(_translate("Dialog_estimation_settings", "Settings for the parameterization of the estimated vertical gravity gradient."))
        self.groupBox_vg_polynomial.setTitle(_translate("Dialog_estimation_settings", "Vertical Gradient Polynomial "))
        self.label_vg_polynomial_degree.setToolTip(_translate("Dialog_estimation_settings", "Degree of the estimated vertical gravity gradient polynomial"))
        self.label_vg_polynomial_degree.setText(_translate("Dialog_estimation_settings", "Degree of the VG polynomial"))
        self.spinBox_vg_polynomial_degree.setToolTip(_translate("Dialog_estimation_settings", "Degree of the estimated vertical gravity gradient polynomial"))
        self.label_vg_polynomial_ref_height_offset_m.setToolTip(_translate("Dialog_estimation_settings", "The reference height for the vertical gravity gradient polynomial ist the height of the control point. With this option it is possible to introduce an offset to the reference height."))
        self.label_vg_polynomial_ref_height_offset_m.setText(_translate("Dialog_estimation_settings", "Reference height offset [m]"))
        self.doubleSpinBox_vg_polynomial_ref_height_offset_m.setToolTip(_translate("Dialog_estimation_settings", "The reference height for the vertical gravity gradient polynomial ist the height of the control point. With this option it is possible to introduce an offset to the reference height."))
        self.tabWidget_estimation_settings.setTabText(self.tabWidget_estimation_settings.indexOf(self.tab_vg_estimation), _translate("Dialog_estimation_settings", "VG estimation"))
