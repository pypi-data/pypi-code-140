#!/usr/bin/env python

# Copyright 2015 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

"""
Module containing functions to manage autosubmit's experiments.
"""
import os
import time
import pickle
import traceback
import datetime
import json
import multiprocessing
import subprocess
from collections import deque
from autosubmit_api.autosubmit_legacy.autosubmit import Autosubmit
import autosubmit_api.database.db_common as db_common
import autosubmit_api.experiment.common_db_requests as DbRequests
import autosubmit_api.database.db_jobdata as JobData
import autosubmit_api.autosubmit_legacy.job.job_utils as LegacyJobUtils
import autosubmit_api.common.utils as common_utils
import autosubmit_api.components.jobs.utils as JUtils

from autosubmit_api.autosubmit_legacy.job.job_list import JobList
from autosubmit_api.autosubmit_legacy.job.job import Job

from autosubmit_api.performance.utils import calculate_ASYPD_perjob, calculate_SYPD_perjob
from autosubmit_api.monitor.monitor import Monitor

from autosubmit_api.statistics.statistics import Statistics

from autosubmit_api.config.basicConfig import BasicConfig
from autosubmit_api.config.config_common import AutosubmitConfig
from bscearth.utils.config_parser import ConfigParserFactory

from autosubmit_api.components.representations.tree.tree import TreeRepresentation
from autosubmit_api.components.representations.graph.graph import GraphRepresentation, GroupedBy, Layout

from autosubmit_api.builders.experiment_history_builder import ExperimentHistoryDirector, ExperimentHistoryBuilder
from autosubmit_api.builders.configuration_facade_builder import ConfigurationFacadeDirector, AutosubmitConfigurationFacadeBuilder
from autosubmit_api.builders.joblist_loader_builder import JobListLoaderBuilder, JobListLoaderDirector
from autosubmit_api.components.jobs.job_support import JobSupport
from typing import Dict, Any

BasicConfig.read()

SAFE_TIME_LIMIT = 300
SAFE_TIME_LIMIT_STATUS = 180


def get_experiment_stats(expid, filter_period, filter_type):
    # type: (str, int, str) -> Dict[str, Any]
    """
    Lite version of the stats generator from Autosubmit autosubmit.py
    """
    error = False
    error_message = ""
    period_fi = ""
    period_ini = ""
    considered_jobs = list()
    result = None
    summary = None
    try:
        if filter_period:
            filter_period = int(filter_period)

        job_list_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
        considered_jobs = job_list_loader.jobs
        if filter_type and filter_type != 'Any':
            considered_jobs = [job for job in job_list_loader.jobs if job.section == filter_type]

        period_fi = datetime.datetime.now().replace(second=0, microsecond=0)
        if filter_period and filter_period > 0:
            period_ini = period_fi - datetime.timedelta(hours=filter_period)
            filtered_jobs = []
            for job in considered_jobs:
                job_support = JobSupport(expid, job, BasicConfig)
                if job_support.check_started_after(period_ini) or job_support.check_running_after(period_ini):
                    filtered_jobs.append(job)
            considered_jobs = filtered_jobs
        else:
            period_ini = None

        if len(considered_jobs) > 0:
            statistics = Statistics(expid=expid, jobs=considered_jobs, start=period_ini, end=period_fi, queue_time_fix={}, basic_config=BasicConfig)
            result = statistics.get_statistics()
            statistics.calculate_summary()
            summary = statistics.get_summary_as_dict()
        else:
            raise Exception("Autosubmit API couldn't find jobs that match your search critearia (Section: {0}) in the period from {1} to {2}.".format(filter_type, period_ini, period_fi))

    except Exception as e:
        print(traceback.format_exc())
        error_message = str(e)
        error = True

    return {
        'error': error,
        'error_message': error_message,
        'Statistics': result,
        'summary': summary,
    }


def get_experiment_data(expid):
    """
    Get data of the experiment. Depends on the worker that updates ecearth.db.
    """
    result = {
            'expid': expid,
            'path': "NA",
            'owner_id': 0,
            'owner': "NA",
            'time_last_access': "",
            'time_last_mod': "",
            'error_message': "",
            'description': "",
            'version': "",
            'model': "",
            'branch': "",
            'hpc': "",
            'updateTime': 0,
            'error': False,
            'running': False,
            'pkl_timestamp': int(time.time()),
            "chunk_size": 0,
            "chunk_unit": "default",
            'total_jobs': 0,
            'completed_jobs': 0,
            'db_historic_version': "NA"}
    try:
        autosubmit_config_facade = ConfigurationFacadeDirector(AutosubmitConfigurationFacadeBuilder(expid)).build_autosubmit_configuration_facade()
        result["path"] = autosubmit_config_facade.experiment_path
        result["owner_id"] = autosubmit_config_facade.get_owner_id()
        result["owner"] = autosubmit_config_facade.get_owner_name()
        result["time_last_access"] = autosubmit_config_facade.get_experiment_last_access_time_as_datetime()
        result["time_last_mod"] = autosubmit_config_facade.get_experiment_last_modified_time_as_datetime()
        result["description"] = db_common.get_experiment_by_id(expid)["description"]
        result["version"] = autosubmit_config_facade.get_autosubmit_version()
        result["model"] = autosubmit_config_facade.get_model()
        result["branch"] = autosubmit_config_facade.get_branch()
        result["hpc"] = autosubmit_config_facade.get_main_platform()
        result["updateTime"] = autosubmit_config_facade.get_safety_sleep_time()
        result["pkl_timestamp"] = autosubmit_config_facade.get_pkl_last_modified_timestamp()
        result["chunk_size"] = autosubmit_config_facade.chunk_size
        result["chunk_unit"] = autosubmit_config_facade.chunk_unit
        experiment_history = ExperimentHistoryDirector(ExperimentHistoryBuilder(expid)).build_reader_experiment_history()
        experiment_run = experiment_history.manager.get_experiment_run_dc_with_max_id()
        if experiment_run and experiment_run.total > 0:
            result["total_jobs"] = experiment_run.total
            result["completed_jobs"] = experiment_run.completed
            result["db_historic_version"] = experiment_history.manager.db_version
        else:
            _, result["total_jobs"], result["completed_jobs"] =  DbRequests.get_experiment_times_by_expid(expid)
            result["db_historic_version"] = "NA"

    except Exception as exp:
        result["error"] = True
        result["error_message"] = str(exp)
        pass
    return result


def get_current_status_log_plus(expid):
    """
    Get the current status, name of current log, last time modified, and last 5 lines of the latest log of the experiment.
    Presents _is_exp_running as a JSON object.
    """
    error, error_message, is_running, timediff, log_path = _is_exp_running(
        expid)
    return {"error": error,
            "error_message": error_message,
            "is_running": is_running,
            "timediff": timediff,
            "log_path": log_path}


def _is_exp_running(expid, time_condition=300):
    """
    Tests if experiment is running
    :param expid: Experiment name
    :param time_condition: Time constraint, 120 by default. Represents max seconds before an experiment is considered as NOT RUNNING
    :return: (error (true if error is found, false otherwise), error_message, is_running (true if running, false otherwise), timediff, path_to_log)
    :rtype: tuple (bool, string, bool, int)
    """
    is_running = False
    error = False
    error_message = ""
    timediff = 0
    definite_log_path = None
    try:
        BasicConfig.read()
        pathlog_aslog = BasicConfig.LOCAL_ROOT_DIR + '/' + expid + '/' + \
            BasicConfig.LOCAL_TMP_DIR + '/' + BasicConfig.LOCAL_ASLOG_DIR
        pathlog_tmp = BasicConfig.LOCAL_ROOT_DIR + '/' + \
            expid + '/' + BasicConfig.LOCAL_TMP_DIR
        # Basic Configuration
        look_old_folder = False
        current_version = None
        try:
            as_conf = AutosubmitConfig(
                expid, BasicConfig, ConfigParserFactory())
            as_conf.reload()
            current_version = as_conf.get_version()
        except Exception as exp:
            # print(exp)
            pass
        look_old_folder = True if current_version is not None and (str(current_version).startswith(
            "3.11") or str(current_version).startswith("3.9") or str(current_version).startswith("3.12")) else False

        pathlog_first = pathlog_aslog if look_old_folder == False else pathlog_tmp
        pathlog_second = pathlog_aslog if look_old_folder == True else pathlog_tmp
        # print("Experiment {0} version {1} \nLook {2} \nLook {3}".format(
        #     expid, current_version, pathlog_first, pathlog_second))
        # print(pathlog)
        reading = os.popen(
            'ls -t ' + pathlog_first + ' | grep "_run.log"').read() if (os.path.exists(pathlog_first)) else ""

        #print("Length {0}".format(len(reading)))
        if (reading) and len(reading) > 0:
            log_file_name = reading.split()[0]
            definite_log_path = pathlog_first + '/' + log_file_name
            current_stat = os.stat(definite_log_path)
            timest = current_stat.st_mtime
            # system_stat = os.stat(BasicConfig.LOCAL_ROOT_DIR)
            timesys = time.time()
            timediff = int(timesys - timest)
            # print(timediff)
            if (timediff < time_condition):
                is_running = True
            else:
                is_running = False
            return (error, error_message, is_running, timediff, definite_log_path)

        # print(pathlog)
        reading = os.popen(
            'ls -t ' + pathlog_second + ' | grep "_run.log"').read() if (os.path.exists(pathlog_second)) else ""
        #print("Second reading {0}".format(reading))
        if (reading) and len(reading) > 0:
            log_file_name = reading.split()[0]
            definite_log_path = pathlog_second + '/' + log_file_name
            current_stat = os.stat(definite_log_path)
            timest = current_stat.st_mtime
            # system_stat = os.stat(BasicConfig.LOCAL_ROOT_DIR),
            timesys = time.time()
            timediff = int(timesys - timest)
            if (timediff < time_condition):
                is_running = True
            else:
                is_running = False
            return (error, error_message, is_running, timediff, definite_log_path)
        # If nothing is found
        return (error, error_message, is_running, timediff, definite_log_path)

    except Exception as ex:
        error = True
        is_running = False
        timediff = time_condition
        error_message = str(ex)
        # print(traceback.format_exc())
        # print("Error in test: " + error_message)
        return (error, error_message, is_running, timediff, definite_log_path)


def get_experiment_summary(expid):
    """
    Gets job summary for the experiment. Consider seconds.
    :param expid: Name of experiment
    :rtype expid: str
    :return: Object
    """
    BasicConfig.read()

    running = suspended = queuing = failed = submitted = total_q_time = total_r_time = 0
    q_count = r_count = 0
    # avg_q_time = avg_r_time = sim_avg_q_time = sim_avg_r_time =
    avg_q_time = avg_r_time = sim_avg_q_time = sim_avg_r_time = 0
    str_avg_q_time = str_avg_r_time = str_sim_avg_q_time = str_sim_avg_r_time = "NA"
    sim_q_count = sim_r_count = sim_total_q_time = sim_total_r_time = sim_count = 0
    # type_avg_q_time = type_avg_r_time = type_sim_avg_q_time = type_sim_avg_r_time = "min"
    failed_list = list()
    error = False
    error_message = ""
    try:
        # Basic paths
        BasicConfig.read()
        path = BasicConfig.LOCAL_ROOT_DIR + '/' + expid + '/pkl'
        tmp_path = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, expid, BasicConfig.LOCAL_TMP_DIR)
        pkl_filename = "job_list_" + str(expid) + ".pkl"
        path_pkl = path + "/" + pkl_filename
        # Try to get packages
        job_to_package = dict()
        package_to_jobs = dict()
        package_to_package_id = dict()
        package_to_symbol = dict()
        job_to_package, package_to_jobs, package_to_package_id, package_to_symbol = JobList.retrieve_packages(
            BasicConfig, expid)
        # Basic data
        job_running_to_seconds = dict()
        job_running_to_runtext = dict()
        jobs_in_pkl = dict()
        fakeAllJobs = list()

        if os.path.exists(path_pkl):
            fd = open(path_pkl, 'r')
            for item in pickle.load(fd):
                status_code = int(item[2])
                job_name = item[0]
                priority = item[3]
                id_number = item[1]
                out = str(item[8]) if len(item) >= 9 else ""
                err = str(item[9]) if len(item) >= 10 else ""
                status_color = Monitor.color_status(status_code)
                status_text = str(common_utils.Status.VALUE_TO_KEY[status_code])
                jobs_in_pkl[job_name] = (
                    status_code, status_color, status_text, out, err, priority, id_number)
                fakeAllJobs.append(
                    LegacyJobUtils.SimpleJob(job_name, tmp_path, status_code))
            job_running_to_seconds, job_running_to_runtext, _ = JobList.get_job_times_collection(
                BasicConfig, fakeAllJobs, expid, job_to_package, package_to_jobs, timeseconds=True)
        # Main Loop
        if len(job_running_to_seconds.keys()) > 0:
            for job_name in jobs_in_pkl.keys():
                # print(value)
                job_info = job_running_to_seconds[job_name] if job_name in job_running_to_seconds.keys(
                ) else None
                queue_seconds = job_info.queue_time if job_info else 0
                running_seconds = job_info.run_time if job_info else 0
                status = job_info.status if job_info else "UNKNOWN"
                energy = job_info.energy if job_info else 0
                # Identifying SIM
                name_components = job_name.split('_')
                if "SIM" in name_components:
                    # print(name_components)
                    sim_count += 1
                    if status in ["QUEUING"]:
                        sim_q_count += 1
                        sim_total_q_time += queue_seconds
                        # print(sim_total_q_time)
                    elif status in ["COMPLETED", "RUNNING", "FAILED"]:
                        sim_q_count += 1
                        sim_r_count += 1
                        sim_total_q_time += queue_seconds
                        sim_total_r_time += running_seconds

                # print(str(key) + " ~ " + str(status))
                if status == "FAILED":
                    failed += 1
                    q_count += 1
                    r_count += 1
                    total_q_time += queue_seconds
                    total_r_time += running_seconds
                    failed_list.append(job_name)
                elif status == "SUBMITTED":
                    submitted += 1
                    q_count += 1
                    total_q_time += queue_seconds
                elif status == "QUEUING":
                    queuing += 1
                    q_count += 1
                    total_q_time += queue_seconds
                elif status == "SUSPENDED":
                    suspended += 1
                elif status == "RUNNING":
                    running += 1
                    q_count += 1
                    r_count += 1
                    total_q_time += queue_seconds
                    total_r_time += running_seconds
                elif status == "COMPLETED":
                    q_count += 1
                    r_count += 1
                    total_q_time += queue_seconds
                    total_r_time += running_seconds
        # All jobs: Average queuing time
        avg_q_time = int(total_q_time / q_count) if q_count > 0 else 0
        str_avg_q_time = str(datetime.timedelta(seconds=avg_q_time))

        # All jobs: Average running time
        avg_r_time = int(total_r_time / r_count) if r_count > 0 else 0
        str_avg_r_time = str(datetime.timedelta(seconds=avg_r_time))

        # Sim jobs: Average queuing time
        sim_avg_q_time = int(sim_total_q_time /
                             sim_q_count) if sim_q_count > 0 else 0
        str_sim_avg_q_time = str(datetime.timedelta(seconds=sim_avg_q_time))

        # Sim jobs: Average running time
        sim_avg_r_time = int(sim_total_r_time /
                             sim_r_count) if sim_r_count > 0 else 0
        str_sim_avg_r_time = str(datetime.timedelta(seconds=sim_avg_r_time))
    except Exception as exp:
        error = True
        error_message = str(exp)

    return {
        'n_running': running,
        'n_suspended': suspended,
        'n_queuing': queuing,
        'n_failed': failed,
        'n_submitted': submitted,
        'avg_queue_time': str_avg_q_time,
        'avg_run_time': str_avg_r_time,
        'n_sim': sim_count,
        'avg_sim_queue_time': str_sim_avg_q_time,
        'avg_sim_run_time': str_sim_avg_r_time,
        'sim_queue_considered': sim_q_count,
        'sim_run_considered': sim_r_count,
        'failed_jobs': failed_list,
        'error': error,
        'error_message': error_message
    }


def quick_test_run(expid):
    """
    Quick test run that queries the database
    :param expid: Experiment name
    :type expid: str
    :return: running status
    :rtype: JSON object
    """
    running = True
    error = False
    error_message = ""

    try:
        name, status = DbRequests.get_specific_experiment_status(expid)
        if status != "RUNNING":
            running = False
    except Exception as exp:
        error = True
        error_message = str(exp)
        print(traceback.format_exc())

    return {
        'running': running,
        'error': error,
        'error_message': error_message
    }


def test_run(expid):
    """
    Tests if experiment is running.\n
    :param expid: Experiment name
    :type expid: str
    :return: running status
    :rtype: JSON object
    """
    running = False
    error = False
    error_message = ""

    try:
        error, error_message, running, _, _ = _is_exp_running(expid, time_condition=120)
    except Exception as ex:
        error = True
        error_message = str(ex)

    return {'running': running,
            'error': error,
            'error_message': error_message}


def get_experiment_log_last_lines(expid):
    """
    Gets last 150 lines of the log content
    """
    # Initializing results:
    log_file_name = ""
    found = False
    log_file_lastmodified = ""
    timest = ""
    error = False
    error_message = ""
    logcontent = []
    reading = ""

    try:
        BasicConfig.read()
        path = BasicConfig.LOCAL_ROOT_DIR + '/' + expid + '/' + BasicConfig.LOCAL_TMP_DIR + '/' + BasicConfig.LOCAL_ASLOG_DIR
        reading = os.popen('ls -t ' + path + ' | grep "run.log"').read() if (os.path.exists(path)) else ""

        # Finding log files
        if len(reading) == 0:
            path = BasicConfig.LOCAL_ROOT_DIR + '/' + expid + '/' + BasicConfig.LOCAL_TMP_DIR
            reading = os.popen('ls -t ' + path + ' | grep "run.log"').read() if (os.path.exists(path)) else ""

        if len(reading) > 0:
            log_file_name = reading.split()[0]
            current_stat = os.stat(path + '/' + log_file_name)
            timest = int(current_stat.st_mtime)
            log_file_lastmodified = common_utils.timestamp_to_datetime_format(timest)
            found = True
            request = 'tail -150 ' + path + '/' + log_file_name
            last_lines = os.popen(request)
            for i, item in enumerate(last_lines.readlines()):
                logcontent.append({'index': i, 'content': item[0:-1]})
    except Exception as e:
        error = True
        error_message = str(e)

    return {
        'logfile': log_file_name,
        'found': found,
        'lastModified': log_file_lastmodified,
        'timeStamp': timest,
        'error': error,
        'error_message': error_message,
        'logcontent': logcontent}


def get_job_log(expid, logfile, nlines=150):
    """
    Returns the last 150 lines of the log file. Targets out or err.
    :param logfilepath: path to the log file
    :type logfilepath: str
    :return: List of string
    :rtype: list
    """
    # Initializing results:
    found = False
    log_file_lastmodified = ""
    timest = ""
    error = False
    error_message = ""
    logcontent = []
    reading = ""
    BasicConfig.read()
    logfilepath = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, BasicConfig.LOCAL_TMP_DIR, "LOG_{0}".format(expid), logfile)
    try:
        if os.path.exists(logfilepath):
            current_stat = os.stat(logfilepath)
            timest = int(current_stat.st_mtime)
            log_file_lastmodified = common_utils.timestamp_to_datetime_format(timest)
            found = True
            request = "tail -{0} {1}".format(nlines, logfilepath)
            last50 = os.popen(request)
            i = 0
            for item in last50.readlines():
                logcontent.append({'index': i, 'content': item[0:-1]})
                i += 1
    except Exception as e:
        error = True
        error_message = str(e)

    return {
        'logfile': logfilepath,
        'found': found,
        'lastModified': log_file_lastmodified,
        'timeStamp': timest,
        'error': error,
        'error_message': error_message,
        'logcontent': logcontent}


def get_experiment_pkl(expid):
    # type: (str) -> Dict[str, Any]
    """
    Gets the current state of the pkl in a format proper for graph update.
    """
    pkl_file_path = ""
    error = False
    error_message = ""
    pkl_content = list()
    pkl_timestamp = 0
    package_to_jobs = dict()
    try:
        autosubmit_config_facade = ConfigurationFacadeDirector(AutosubmitConfigurationFacadeBuilder(expid)).build_autosubmit_configuration_facade()
        pkl_file_path = autosubmit_config_facade.pkl_path
        pkl_timestamp = autosubmit_config_facade.get_pkl_last_modified_timestamp()

        if not os.path.exists(autosubmit_config_facade.pkl_path):
            raise Exception("Pkl file {} not found.".format(autosubmit_config_facade.pkl_path))

        job_list_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
        package_to_jobs = job_list_loader.joblist_helper.package_to_jobs

        for job in job_list_loader.jobs:
            pkl_content.append({'name': job.name,
                                'rm_id': job.rm_id,
                                'status_code': job.status,
                                'SYPD': calculate_SYPD_perjob(autosubmit_config_facade.chunk_unit, autosubmit_config_facade.chunk_size, job.chunk, job.run_time, job.status),
                                'minutes': job.run_time,
                                'minutes_queue': job.queue_time,
                                'submit': common_utils.timestamp_to_datetime_format(job.submit),
                                'start': common_utils.timestamp_to_datetime_format(job.start),
                                'finish': common_utils.timestamp_to_datetime_format(job.finish),
                                'running_text': job.running_time_text,
                                'dashed': True if job.package else False,
                                'shape': job_list_loader.joblist_helper.package_to_symbol.get(job.package, "dot"),
                                'package': job.package,
                                'status': job.status_text,
                                'status_color': job.status_color,
                                'out': job.out_file_path,
                                'err': job.err_file_path,
                                'priority': job.priority})

    except Exception as e:
        error = True
        error_message = str(e)

    return {
        'pkl_file_name': pkl_file_path,
        'error': error,
        'error_message': error_message,
        'has_changed': True,
        'pkl_content': pkl_content,
        'pkl_timestamp': pkl_timestamp,
        'packages': package_to_jobs,
    }


def get_experiment_tree_pkl(expid):
    # type: (str) -> Dict[str, Any]
    """
    Gets the current state of the pkl in a format for tree update
    """
    pkl_file_path = ""
    error = False
    error_message = ""
    pkl_content = list()
    package_to_jobs = {}
    pkl_timestamp = 0

    try:
        autosubmit_config_facade = ConfigurationFacadeDirector(AutosubmitConfigurationFacadeBuilder(expid)).build_autosubmit_configuration_facade()
        pkl_file_path = autosubmit_config_facade.pkl_path
        pkl_timestamp = autosubmit_config_facade.get_pkl_last_modified_timestamp()

        if not os.path.exists(autosubmit_config_facade.pkl_path):
            raise Exception("Pkl file {} not found.".format(autosubmit_config_facade.pkl_path))

        job_list_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
        package_to_jobs = job_list_loader.joblist_helper.package_to_jobs
        for job in job_list_loader.jobs:
            pkl_content.append({'name': job.name,
                                'rm_id': job.rm_id,
                                'status_code': job.status,
                                'SYPD': calculate_SYPD_perjob(autosubmit_config_facade.chunk_unit, autosubmit_config_facade.chunk_size, job.chunk, job.run_time, job.status),
                                'minutes': job.run_time,
                                'minutes_queue': job.queue_time,
                                'submit': common_utils.timestamp_to_datetime_format(job.submit),
                                'start': common_utils.timestamp_to_datetime_format(job.start),
                                'finish': common_utils.timestamp_to_datetime_format(job.finish),
                                'running_text': job.running_time_text,
                                'status': job.status_text,
                                'status_color': job.status_color,
                                'wrapper': job.package,
                                'wrapper_tag': job.package_tag,
                                'wrapper_id': job.package_code,
                                'out': job.out_file_path,
                                'err': job.err_file_path,
                                'title': job.tree_title,
                                'priority': job.priority})
    except Exception as e:
        error = True
        error_message = str(e)

    return {
        'pkl_file_name': pkl_file_path,
        'error': error,
        'error_message': error_message,
        'has_changed': True,
        'pkl_content': pkl_content,
        'packages': list(package_to_jobs.keys()),
        'pkl_timestamp': pkl_timestamp,
        'source_tag': JUtils.source_tag,
        'target_tag': JUtils.target_tag,
        'sync_tag': JUtils.sync_tag,
        'check_mark': JUtils.checkmark_tag,
    }


def get_experiment_graph(expid, log, layout=Layout.STANDARD, grouped=GroupedBy.NO_GROUP):
    """
    Gets graph representation
    """
    base_list = dict()
    pkl_timestamp = 10000000
    try:
        # autosubmit_configuration_facade = ConfigurationFacadeDirector(AutosubmitConfigurationFacadeBuilder(expid)).build_autosubmit_configuration_facade()

        BasicConfig.read()
        autosubmit_configuration_facade = AutosubmitConfig(
            expid, BasicConfig, ConfigParserFactory())
        autosubmit_configuration_facade.reload()
        # raise Exception("json config autosubmitgraph: " + str(autosubmit_configuration_facade.__dict__))
        try:
            if common_utils.is_version_historical_ready(autosubmit_configuration_facade.get_version()):
                job_list_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
                graph = GraphRepresentation(expid, job_list_loader, layout, grouped)
                graph.perform_calculations()
                return graph.get_graph_representation_data()
        except Exception as exp:
            # print(traceback.format_exc())
            print("New Graph Representation failed: {0}".format(exp))
            log.info("Could not generate graph with faster method")

        # Getting platform data
        hpcarch = autosubmit_configuration_facade.get_platform()

        # Submitter
        submitter = Autosubmit._get_submitter(autosubmit_configuration_facade)
        submitter.load_platforms(autosubmit_configuration_facade)
        # JobList construction
        job_list = Autosubmit.load_job_list(expid, autosubmit_configuration_facade, notransitive=False)

        if job_list.graph == None:
            raise Exception("Graph generation is not possible for this experiment.")

        # Platform update
        for job in job_list.get_job_list():
            if job.platform_name is None:
                job.platform_name = hpcarch
            job.platform = submitter.platforms[job.platform_name.lower()]

        # Chunk unit and chunk size
        chunk_unit = autosubmit_configuration_facade.get_chunk_size_unit()
        chunk_size = autosubmit_configuration_facade.get_chunk_size()

        job_list.sort_by_id()

        base_list = job_list.get_graph_representation(
            BasicConfig, layout, grouped, chunk_unit=chunk_unit, chunk_size=chunk_size
        )
        # raise Exception("Base list graph: ", str(base_list))
    except Exception as e:
        print(traceback.format_exc())
        log.info("Could not generate Graph and recieved the following exception: " + str(e))
        return {'nodes': [],
                'edges': [],
                'fake_edges': [],
                'groups': [],
                'groups_data': {},
                'error': True,
                'error_message': str(e),
                'graphviz': False,
                'max_children': 0,
                'max_parents': 0,
                'total_jobs': 0,
                'pkl_timestamp': 0}

    base_list['error'] = False
    base_list['error_message'] = ""
    base_list['pkl_timestamp'] = pkl_timestamp
    return base_list


def get_experiment_tree_rundetail(expid, run_id):
    """
    """
    base_list = dict()
    pkl_timestamp = 10000000
    try:
        print("Received Tree RunDetail " + str(expid))
        BasicConfig.read()
        tree_structure, current_collection, reference = JobList.get_tree_structured_from_previous_run(expid, BasicConfig, run_id=run_id)
        base_list['tree'] = tree_structure
        base_list['jobs'] = current_collection
        base_list['total'] = len(current_collection)
        base_list['reference'] = reference
    except Exception as e:
        print(traceback.format_exc())
        return {'tree': [], 'jobs': [], 'total': 0, 'reference': [], 'error': True, 'error_message': str(e), 'pkl_timestamp': 0}
    base_list['error'] = False
    base_list['error_message'] = 'None'
    base_list['pkl_timestamp'] = pkl_timestamp
    return base_list


def get_experiment_tree_structured(expid, log):
    """
    Current version of the tree visualization algorithm.
    :param expid: Name of experiment
    :type expid: String
    :return: Dictionary [Variable Name] to Value
    :rtype: Dictionary Key: String, Value: Object
    """
    base_list = dict()
    pkl_timestamp = 10000000
    try:
        notransitive = False
        BasicConfig.read()

        # TODO: Encapsulate this following 2 lines or move to the parent function in app.py
        curr_exp_as_version = db_common.get_autosubmit_version(expid)
        main, secondary = common_utils.parse_version_number(curr_exp_as_version)
        if main >= "4":
            # TODO: new YAML parser
            test = 1
        else:
            log.info("EXPERIMENT VERSION = " + str(curr_exp_as_version))
            as_conf = AutosubmitConfig(expid, BasicConfig, ConfigParserFactory())
            as_conf.reload()


        # If version is higher than 3.13, we can perform the new tree representation algorithm
        try:
            if common_utils.is_version_historical_ready(as_conf.get_version()):
                job_list_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
                tree = TreeRepresentation(expid, job_list_loader)
                tree.perform_calculations()
                # este return
                return tree.get_tree_structure()
            else:
                log.info("TREE|Not using first method|autosubmit_version=" + as_conf.get_version())
        except Exception as exp:
            print(traceback.format_exc())
            print("New Tree Representation failed: {0}".format(exp))
            log.info("New Tree Representation failed: {0}".format(exp))

        # Getting platform data
        # Main taget HPC
        hpcarch = as_conf.get_platform()

        # Submitter
        submitter = Autosubmit._get_submitter(as_conf)
        submitter.load_platforms(as_conf)
        # JobList construction
        job_list = Autosubmit.load_job_list(
            expid, as_conf, notransitive=notransitive)
        # print("Job list build completed")
        # Platform update
        for job in job_list.get_job_list():
            if job.platform_name is None:
                job.platform_name = hpcarch
            job.platform = submitter.platforms[job.platform_name.lower(
            )]
        # Chunk Unit and Size
        chunk_unit = as_conf.get_chunk_size_unit()
        chunk_size = as_conf.get_chunk_size()

        tree_structure, current_collection, reference = job_list.get_tree_structured(
            BasicConfig, chunk_unit=chunk_unit, chunk_size=chunk_size)

        base_list['tree'] = tree_structure
        base_list['jobs'] = current_collection
        base_list['total'] = len(current_collection)
        base_list['reference'] = reference
    except Exception as e:
        print(traceback.format_exc())
        return {'tree': [], 'jobs': [], 'total': 0, 'reference': [], 'error': True, 'error_message': str(e), 'pkl_timestamp': 0}
    base_list['error'] = False
    base_list['error_message'] = 'None'
    base_list['pkl_timestamp'] = pkl_timestamp
    return base_list


def retrieve_all_pkl_files():
    """
    Retrieves a list of all pkl files in /esarchive/autosubmit/*/pkl/ with timestamps for comparison purposes
    :return: Dictionary Key: expid, Value: 2-tuple (timestamp, path_to_pkl)
    """
    all_pkl = os.popen("find /esarchive/autosubmit/*/pkl/ -name \"*.pkl\"  -printf \"%p %Ts\n\"").read()
    all_pkl = all_pkl.split("\n")
    # print(all_pkl)
    exp_to_pkl = dict()
    #exp_to_modified = dict()
    for item in all_pkl:
        try:
            honk = item.split()
            timestamp = int(honk[1])
            file_name = str(honk[0]).split("/")
            exp_to_pkl[str(file_name[3])] = (timestamp, str(honk[0]))
            print(file_name[3] + " ~ " +
                  str(timestamp) + " :: " + str(honk[0]))
        except Exception as exp:
            pass
    return exp_to_pkl


def _get_hpcarch_project_from_experiment_run_metadata(run_id, experiment_runs_dict):
    """ """
    try:
        allowedKeys = ['conf', 'exp', 'jobs', 'platforms', 'proj']
        platform_projects = {}
        main_platform = ""
        run = experiment_runs_dict.get(run_id, None)
        if run and run.metadata:
            data = json.loads(run.metadata)
            main_platform = data["exp"]["experiment"].get("HPCARCH", "")
            for platform in data["platforms"]:
                platform_projects[platform] = data["platforms"][platform].get("PROJECT", "")
        else:
            raise Exception("NO METADATA ON RUN {0}".format(run_id))
        print("PLATFORMS")
        print(platform_projects)
        return (main_platform, platform_projects)
    except Exception as exp:
        print(exp)
        return ("", {})

def generate_all_experiment_data(exp_path, job_path):
    """
    Getting all data from experiments
    """
    target_experiment_file = str(exp_path)
    target_experiment_job_file = str(job_path)
    print("Experiment file path: " + target_experiment_file)
    print("Job file path: " + target_experiment_job_file)
    conn_ecearth = DbRequests.create_connection("/esarchive/autosubmit/ecearth.db")
    conn_as_times = DbRequests.create_connection("/esarchive/autosubmit/as_times.db")
    # print("Getting experiments")
    all_experiments = DbRequests._get_exps_complete(conn_ecearth)
    all_detailed = DbRequests.get_exps_detailed_complete(conn_ecearth)
    experiment_times = DbRequests.get_experiment_times()
    valid_id = dict()
    if (all_detailed) and (all_experiments) and (experiment_times):
        file1 = open(target_experiment_file, "w")
        file1.write(
            "id|name|completed|total|user|as_version|created|model|hpc|wrapper|maxwrap\n")
        for item in all_experiments:
            _id, name, _type, autosubmit_version, description, model_branch, template_name, template_branch, ocean_diag_branch = item
            wrapper_type, maxwrapped = get_auto_conf_data(name)
            #  description = description.replace('|', '~')
            # print(item)
            if _id in all_detailed.keys():
                user, created, model, branch, hpc = all_detailed[_id]

                completed = total = 0
                if name in experiment_times.keys():
                    # Exists register of experiment completed and total jobs
                    total, completed, _ = experiment_times[name]
                    file1.write(str(_id) + "|" + str(name) + "|" + str(completed) + "|" + str(total) + "|" + str(user) + "|" + str(autosubmit_version) + "|" + str(
                        created) + "|" + format_model(str(model)) + "|" + str(hpc) + "|" + str(wrapper_type) + "|" + str(maxwrapped) + "\n")
                    valid_id[_id] = name
        file1.close()

    # First step was successful, prepare to process jobs
    all_job_times = DbRequests.get_completed_times_detail()
    # if (all_job_times):
    file2 = open(target_experiment_job_file, "w")
    file2.write("exp_id|exp_name|job_name|type|submit|start|finish|status|wallclock|procs|threads|tasks|queue|platform|mainplatform|project\n")
    for exp_id in valid_id.keys():
        expid = valid_id.get(exp_id, None)
        historical_data = None # JobDataStructure(expid).get_all_current_job_data() TODO: Replace for new implementation
        experiment_runs = None # JobDataStructure(expid).get_experiment_runs() TODO: Replace for new implementation
        experiment_runs = experiment_runs if experiment_runs else []
        # print(experiment_runs)
        experiment_runs_dict = {run.run_id: run for run in experiment_runs}
        # print("run id -> (,)")
        experiment_runs_main_info = {run.run_id: _get_hpcarch_project_from_experiment_run_metadata(run.run_id, experiment_runs_dict) for run in experiment_runs}
        # print(experiment_runs_main_info)
        if historical_data:
            print("Using historical data for {}".format(exp_id))
            job_conf = None
            try:
                job_conf = get_job_conf_list(expid)
            except:
                pass
            job_conf_type = {}
            for job in historical_data:
                # Starting from DB VERSION 17, we go back to calling section -> section, and member -> member; instead of the previous erronous assignment.
                if job.member not in job_conf_type:
                    # Member was confused by section in DB version <= 15
                    if job_conf:
                        job_conf_type[job.member] = old_searcher(job_conf, job.job_name)
                main_platform = ""
                project = ""
                if job.run_id:
                    main_platform, platforms = experiment_runs_main_info.get(job.run_id, ("", {}))
                    project = platforms.get(job.platform, "")
                    if len(project) == 0:
                        try:
                            if job.member in job_conf_type:
                                job_conf_info, job_type = job_conf_type[job.member]
                                wallclock, processors, threads, tasks, memory, mem_task, queue, platform, main_platform, project = job_conf_info
                        except:
                            pass
                else:
                    try:
                        if job.member in job_conf_type:
                            job_conf_info, job_type = job_conf_type[job.member]
                            wallclock, processors, threads, tasks, memory, mem_task, queue, platform, main_platform, project = job_conf_info
                    except:
                        pass
                file2.write(str(exp_id) + "|" + str(expid) + "|" + str(job.job_name) + "|" + str(job.member) + "|" + str(
                    job.submit) + "|" + str(job.start) + "|" + str(job.finish) + "|" + str(job.status) + "|" + str(job.wallclock) + "|"
                    + str(common_utils.parse_number_processors(str(job.ncpus))) + "|" + str(0) + "|" + str(0) + "|" + str(job.qos) + "|" + str(job.platform) + "|" + str(main_platform) + "|"
                    + str(project) +  "\n")
        else:
            print("Using current data for {}".format(exp_id))
            if exp_id in all_job_times.keys():
                # print(exp_id)
                current = all_job_times[exp_id]
                exp_name = valid_id[exp_id]
                # print(exp_name)
                if (current):
                    ###
                    # TODO: Request Autosubmit Config here
                    job_conf = get_job_conf_list(exp_name)
                    ###
                    if (job_conf):
                        for job_name in current.keys():
                            job_conf_info, job_type = old_searcher(
                                job_conf, job_name)
                            if (job_conf_info):
                                submit, start, finish, status, detail_id = current[job_name]
                                wallclock, processors, threads, tasks, memory, mem_task, queue, platform, main_platform, project = job_conf_info
                                file2.write(str(exp_id) + "|" + str(exp_name) + "|" + str(job_name) + "|" + str(job_type) + "|" + str(
                                    submit) + "|" + str(start) + "|" + str(finish) + "|" + str(status) + "|" + str(wallclock) + "|"
                                    + str(common_utils.parse_number_processors(str(processors))) + "|" + str(threads) + "|" + str(tasks) + "|" + str(queue) + "|" + str(platform) + "|" + str(main_platform) + "|"
                                    + str(project) +  "\n")
                            else:
                                print(str(exp_name) + "  | job " +
                                      str(job_name) + " no job conf valid found.")
                    else:
                        print(str(exp_name) + " conf not valid.")
    file2.close()


def format_model(url):
    """
    Return model in proper format.
    Considers separator '/es/'
    """
    separator = '/es/'
    sec_separator = '.git'
    model = "NA"
    pos = url.find(separator)
    if pos > 0:
        pos = pos + len(separator)
        model = url[pos:]
        end = model.find(sec_separator)
        if end > 0:
            model = model[0:end]
    return model


def old_searcher(section_dict, job_name):
    """
    A very basic implementation to find the type of a job
    """
    for section in section_dict.keys():
        t_name = "_" + section
        # print(t_name)
        if job_name.find(t_name) >= 0:
            return section_dict[section], section
    return None, None


def get_job_conf_list(expid):
    """
    Gets list of jobs with attributes from parser
    """
    try:
        BasicConfig.read()
        as_conf = AutosubmitConfig(expid, BasicConfig, ConfigParserFactory())
        if not as_conf.check_conf_files():
            print('Can not create with invalid configuration')
            return None
        sections = as_conf.get_jobs_sections()
        result = dict()
        for section in set(sections):
            main_platform = as_conf.get_platform()
            job_platform = as_conf.get_job_platform(section)

            processors = as_conf.get_processors(section)
            threads = as_conf.get_threads(section)
            tasks = as_conf.get_tasks(section)
            memory = as_conf.get_memory(section)
            memory_per_task = as_conf.get_memory_per_task(section)
            queue = as_conf.get_queue(section)
            queue = queue if len(queue) > 0 else (as_conf.get_platform_queue(job_platform) if len(
                job_platform) > 0 else (as_conf.get_platform_queue(main_platform) if len(main_platform) > 0 else ""))
            final_platform = job_platform if len(
                job_platform) > 0 else main_platform
            wallclock = as_conf.get_wallclock(section)
            project = as_conf.get_platform_project(final_platform) # Section is not platform, must get platform from somwhere else.
            platform_wallclock = as_conf.get_platform_wallclock(final_platform)
            wallclock = wallclock if len(wallclock) > 0 else (
                platform_wallclock if len(platform_wallclock) > 0 else "")
            result[section] = (wallclock, processors, threads,
                               tasks, memory, memory_per_task, queue, final_platform, main_platform, project)
        return result
    except Exception as ex:
        print(str(ex) + "\n" + str(expid) +
              " : failed to retrieve info from jobs conf.\n")
        return None


def get_auto_conf_data(expid):
    """
    Gets autosubmit conf parser information per expid
    """
    try:
        wrapper_type = "None"
        max_wrapped = 0
        BasicConfig.read()
        as_conf = AutosubmitConfig(expid, BasicConfig, ConfigParserFactory())
        if not as_conf.check_conf_files():
            #print('Can not create with invalid configuration')
            return (wrapper_type, max_wrapped)
        wrapper_type = as_conf.get_wrapper_type()
        max_wrapped = as_conf.get_max_wrapped_jobs()
        return (wrapper_type, max_wrapped)
    except Exception as ex:
        print("Couldn't retrieve conf data (wrapper info) from {0}. Exception {1}.".format(expid, str(ex)))
        return ("None", 0)


def verify_last_completed(seconds=300):
    """
    Verifying last 300 seconds by default
    """
    # Basic info
    t0 = time.time()
    BasicConfig.read()
    # Current timestamp
    current_st = time.time()
    # Connection
    path = BasicConfig.LOCAL_ROOT_DIR
    db_file = os.path.join(path, DbRequests.DB_FILE_AS_TIMES)
    conn = DbRequests.create_connection(db_file)
    # Current latest detail
    td0 = time.time()
    latest_detail = DbRequests.get_latest_completed_jobs(seconds)
    t_data = time.time() - td0
    # Main Loop
    for job_name, detail in latest_detail.items():
        tmp_path = os.path.join(
            BasicConfig.LOCAL_ROOT_DIR, job_name[:4], BasicConfig.LOCAL_TMP_DIR)
        detail_id, submit, start, finish, status = detail
        submit_time, start_time, finish_time, status_text_res = JobList._job_running_check(
            common_utils.Status.COMPLETED, job_name, tmp_path)
        submit_ts = int(time.mktime(submit_time.timetuple())) if len(
            str(submit_time)) > 0 else 0
        start_ts = int(time.mktime(start_time.timetuple())) if len(
            str(start_time)) > 0 else 0
        finish_ts = int(time.mktime(finish_time.timetuple())) if len(
            str(finish_time)) > 0 else 0
        if (finish_ts != finish):
            #print("\tMust Update")
            DbRequests.update_job_times(detail_id,
                                        int(current_st),
                                        submit_ts,
                                        start_ts,
                                        finish_ts,
                                        status,
                                        debug=False,
                                        no_modify_time=True)
        t1 = time.time()
        # Timer safeguard
        if (t1 - t0) > SAFE_TIME_LIMIT:
            raise Exception(
                "Time limit reached {0:06.2f} seconds on verify_last_completed while reading {1}. Time spent on reading data {2:06.2f} seconds.".format((t1 - t0), job_name, t_data))


def get_experiment_counters(expid):
    """
    Returns status counters of the experiment.
    """
    error = False
    error_message = ""
    total = 0
    experiment_counters = dict()
    BasicConfig.read()
    path_pkl = os.path.join(BasicConfig.LOCAL_ROOT_DIR,
                            expid, "pkl", "job_list_{}.pkl".format(expid))
    # Default counter per status
    experiment_counters = {name: 0 for name in common_utils.Status.STRING_TO_CODE}
    try:
        if os.path.exists(path_pkl):
            fd = open(path_pkl, 'r')
            for item in pickle.load(fd):
                status_code = int(item[2])
                total += 1
                experiment_counters[common_utils.Status.VALUE_TO_KEY.get(status_code, "UNKNOWN")] = experiment_counters.get(
                    common_utils.Status.VALUE_TO_KEY.get(status_code, "UNKNOWN"), 0) + 1

        else:
            raise Exception("PKL file not found.")
    except Exception as exp:
        error = True
        error_message = str(exp)
        # print(traceback.format_exc())
        # print(exp)
    return {"error": error, "error_message": error_message, "expid": expid, "total": total, "counters": experiment_counters}


# TODO: Update to current representation standards and classes
def get_quick_view(expid):
    """ Lighter View """
    pkl_file_name = ""
    error = False
    error_message = ""
    #quick_view = list()
    view_data = []
    quick_tree_view = deque()
    source = JobList.get_sourcetag()
    target = JobList.get_targettag()
    sync = JobList.get_synctag()
    check_mark = JobList.get_checkmark()
    jobs_in_pkl = {}
    fakeAllJobs = []
    total_count = completed_count = failed_count = running_count = queuing_count = 0
    try:
        BasicConfig.read()
        path_pkl = BasicConfig.LOCAL_ROOT_DIR + '/' + expid + '/pkl'
        pkl_file = os.path.join(path_pkl, "job_list_{0}.pkl".format(expid))
        path_to_logs = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "tmp", "LOG_" + expid)
        tmp_path = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, BasicConfig.LOCAL_TMP_DIR)
        if os.path.exists(pkl_file):
            # Retrieving packages
            now_ = time.time()
            job_to_package, package_to_jobs, package_to_package_id, package_to_symbol = JobList.retrieve_packages(
                BasicConfig, expid)
            print("Retrieving packages {0} seconds.".format(
                str(time.time() - now_)))

            try:
                fd = open(pkl_file, 'r')
                for item in pickle.load(fd):
                    status_code = int(item[2])
                    # counters
                    if status_code == common_utils.Status.COMPLETED:
                        completed_count += 1
                    elif status_code == common_utils.Status.FAILED:
                        failed_count += 1
                    elif status_code == common_utils.Status.RUNNING:
                        running_count += 1
                    elif status_code == common_utils.Status.QUEUING:
                        queuing_count += 1
                    # end
                    job_name = item[0]
                    priority = item[3]
                    id_number = item[1]
                    out = str(item[8]) if len(item) >= 9 else ""
                    err = str(item[9]) if len(item) >= 10 else ""
                    status_color = Monitor.color_status(status_code)
                    status_text = str(common_utils.Status.VALUE_TO_KEY[status_code])
                    jobs_in_pkl[job_name] = (
                        status_code, status_color, status_text, out, err, priority, id_number)
            except Exception as exp:
                raise Exception(
                    "Autosubmit API couldn't open pkl file. If you are sure that your experiment is running correctly, try again.")

            total_count = len(jobs_in_pkl.keys())

            if len(jobs_in_pkl.keys()) > 0:
                # fd = open(path_pkl, 'r')
                for job_name in jobs_in_pkl.keys():
                    status_code, status_color, status_text, out, err, priority, id_number = jobs_in_pkl[
                        job_name]
                    wrapper_tag = ""
                    wrapper_id = 0
                    wrapper_name = ""
                    if job_name in job_to_package.keys():
                        wrapper_name = job_to_package[job_name]
                        wrapper_id = package_to_package_id[job_to_package[job_name]]
                        wrapper_tag = " <span class='badge' style='background-color:#94b8b8'>Wrapped " + \
                            wrapper_id + "</span>"

                    view_data.append({'name': job_name,
                                      'path_log': path_to_logs,
                                      'out': "/" + out,
                                      'err': "/" + err,
                                      })
                    if status_code in [common_utils.Status.COMPLETED, common_utils.Status.WAITING, common_utils.Status.READY]:
                        quick_tree_view.append({'title': Job.getTitle(job_name, status_color, status_text) + wrapper_tag,
                                                'refKey': job_name,
                                                'data': 'Empty',
                                                'children': []})
                    else:
                        quick_tree_view.appendleft({'title': Job.getTitle(job_name, status_color, status_text) + wrapper_tag,
                                                    'refKey': job_name,
                                                    'data': 'Empty',
                                                    'children': []})
                # return {}
                # quick_tree_view = list(quick_tree_view)
            else:
                raise Exception('File {0} does not exist'.format(path_pkl))
    except Exception as exp:
        error_message = "Exception: {0}".format(str(exp))
        error = True
        print(error_message)
        print(traceback.format_exc())
        pass

    return {"error": error, "error_message": error_message, "view_data": view_data, "tree_view": list(quick_tree_view), "total": total_count, "completed": completed_count, "failed": failed_count, "running": running_count, "queuing": queuing_count}


def get_job_history(expid, job_name):
    # type: (str, str) -> Dict[str, Any]
    error = False
    error_message = ""
    path_to_job_logs = ""
    result = None
    try:
        BasicConfig.read()
        path_to_job_logs = os.path.join(BasicConfig.LOCAL_ROOT_DIR, expid, "tmp", "LOG_" + expid)
        result = ExperimentHistoryDirector(ExperimentHistoryBuilder(expid)).build_reader_experiment_history().get_historic_job_data(job_name)
    except Exception as exp:
        print(traceback.format_exc())
        error = True
        error_message = str(exp)
        pass
    return {"error": error, "error_message": error_message, "history": result, "path_to_logs": path_to_job_logs}


def get_current_configuration_by_expid(expid, valid_user, log):
    """
    Gets the current configuration by expid. The procedure queries the historical database and the filesystem.
    :param expid: Experiment Identifier
    :type expdi: str
    :return: configuration content formatted as a JSON object
    :rtype: Dictionary
    """
    error = False
    warning = False
    error_message = ""
    warning_message = ""
    currentRunConfig = {}
    currentFileSystemConfig = {}

    def removeParameterDuplication(currentDict, keyToRemove, exceptionsKeys=[]):
        if currentDict and isinstance(currentDict, dict):
            try:
                for k, nested_d in currentDict.items():
                    if k not in exceptionsKeys and isinstance(nested_d, dict):
                        nested_d.pop(keyToRemove, None)
            except Exception as exp:
                log.info("Error while trying to eliminate duplicated key from config.")
                pass
        return currentDict

    try:
        if not valid_user:
            raise Exception(
                "You have to be logged in to access this information.")
        allowedConfigKeys = ['conf', 'exp', 'jobs', 'platforms', 'proj']
        BasicConfig.read()
        historicalDatabase = JobData.JobDataStructure(expid, BasicConfig)
        experimentRun = historicalDatabase.get_max_id_experiment_run()
        currentMetadata = json.loads(
            experimentRun.metadata) if experimentRun and experimentRun.metadata else None
        currentRunId = experimentRun.run_id if experimentRun else None
        # Main keys = conf, exp, jobs, platforms, proj
        # Can we ignore proj by now? Including it.
        # TODO: Define which keys should be included in the answer
        if currentMetadata:
            currentRunConfig = {
                key: currentMetadata[key] for key in currentMetadata if key in allowedConfigKeys}
        currentRunConfig["contains_nones"] = True if not currentMetadata or None in currentMetadata.values(
        ) else False

        BasicConfig.read()
        autosubmitConfig = AutosubmitConfig(
            expid, BasicConfig, ConfigParserFactory())
        try:
            autosubmitConfig.reload()
            currentFileSystemConfigContent = autosubmitConfig.get_full_config_as_dict()
            if currentFileSystemConfigContent:
                currentFileSystemConfig = {
                    key: currentFileSystemConfigContent[key] for key in currentFileSystemConfigContent if key in allowedConfigKeys}
            currentFileSystemConfig["contains_nones"] = True if not currentFileSystemConfigContent or None in currentFileSystemConfigContent.values(
            ) else False

        except Exception as exp:
            warning = True
            warning_message = "The filesystem system configuration can't be retrieved because '{}'".format(
                exp)
            currentFileSystemConfig["contains_nones"] = True
            pass

        removeParameterDuplication(currentRunConfig['exp'], "EXPID", ["experiment"])
        removeParameterDuplication(currentFileSystemConfig['exp'], "EXPID", ["experiment"])

    except Exception as exp:
        error = True
        error_message = str(exp)
        currentRunConfig["contains_nones"] = True
        currentFileSystemConfig["contains_nones"] = True
        pass
    return {"error": error, "error_message": error_message, "warning": warning, "warning_message": warning_message, "configuration_current_run": currentRunConfig, "configuration_filesystem": currentFileSystemConfig, "are_equal": currentRunConfig == currentFileSystemConfig}



def get_experiment_runs(expid):
    """
    Get runs of the same experiment from historical db
    """
    error = False
    error_message = ""
    result = []

    def assign_current(job_dictionary, job_data_list, exp_history):
        for job_data in job_data_list:
            if job_data._finish == 0:
                job_current_info = job_dictionary.get(job_data.job_name, None)
                if job_current_info and job_current_info.finish_ts > 0:
                    job_data._finish = job_current_info.finish_ts
                    exp_history.update_job_finish_time_if_zero(job_data.job_name, job_data._finish)


    try:
        # TODO: TEST TEST TEST TEST
        # Current data
        joblist_loader = JobListLoaderDirector(JobListLoaderBuilder(expid)).build_loaded_joblist_loader()
        experiment_history = ExperimentHistoryDirector(ExperimentHistoryBuilder(expid)).build_reader_experiment_history()
        # time_0 = time.time()
        experiment_runs = experiment_history.manager.get_experiment_runs_dcs() # job_data_structure.get_experiment_runs()
        sim_jobs = experiment_history.manager.get_job_data_dcs_COMPLETED_by_section("SIM")
        post_jobs = experiment_history.manager.get_job_data_dcs_COMPLETED_by_section("POST")
        run_id_job_name_to_job_data_dc_COMPLETED = {}
        for job_dc in experiment_history.manager.get_job_data_dcs_all():
            if job_dc.status_code == common_utils.Status.COMPLETED:
                run_id_job_name_to_job_data_dc_COMPLETED[(job_dc.run_id, job_dc.job_name)] = job_dc
        run_id_wrapper_code_to_job_dcs = {}
        for key, job_dc in run_id_job_name_to_job_data_dc_COMPLETED.items():
            if job_dc.wrapper_code:
                run_id, _ = key
                run_id_wrapper_code_to_job_dcs.setdefault((run_id, job_dc.wrapper_code), []).append(job_dc)

        run_dict_SIM = {}
        for job_data_dc in sim_jobs:
            run_dict_SIM.setdefault(job_data_dc.run_id, []).append(job_data_dc)
        run_dict_POST = {}
        for job_data_dc in post_jobs:
            run_dict_POST.setdefault(job_data_dc.run_id, []).append(job_data_dc)
        max_run_id = 0
        # print("Time spent in data retrieval and pre-process: {}".format(time.time() - time_0))
        if experiment_runs:
            for experiment_run in experiment_runs:
                max_run_id = max(experiment_run.run_id, max_run_id)
                valid_SIM_in_run = run_dict_SIM.get(experiment_run.run_id, [])
                valid_POST_in_run = run_dict_POST.get(experiment_run.run_id, [])
                # The content of the if block try to correct lack of finish time information in the Historical database
                # It may not be necessary in the future.
                if max_run_id == experiment_run.run_id:
                   assign_current(joblist_loader.job_dictionary, valid_SIM_in_run, experiment_history)
                   assign_current(joblist_loader.job_dictionary, valid_POST_in_run, experiment_history)
                result.append({"run_id": experiment_run.run_id,
                                "created": experiment_run.created,
                                "finish": common_utils.timestamp_to_datetime_format(experiment_run.finish),
                                "chunk_unit": experiment_run.chunk_unit,
                                "chunk_size": experiment_run.chunk_size,
                                "submitted": experiment_run.submitted,
                                "queuing": experiment_run.queuing,
                                "running": experiment_run.running,
                                "completed": experiment_run.completed,
                                "failed": experiment_run.failed,
                                "total": experiment_run.total,
                                "suspended": experiment_run.suspended,
                                "SYPD": experiment_run.getSYPD(valid_SIM_in_run),
                                "ASYPD": experiment_run.getASYPD(valid_SIM_in_run, valid_POST_in_run, run_id_wrapper_code_to_job_dcs)})
            result.sort(key=lambda x: x["run_id"], reverse=True)
        else:
            error = True
            error_message = "No data"
    except Exception as exp:
        print(traceback.format_exc())
        error = True
        error_message = str(exp)
        pass
    return {"error": error, "error_message": error_message, "runs": result}


def read_esarchive(result):
    # t0 = time.time()
    # Using as_times.db as reference
    current_latency = 10000
    current_bandwidth = 10000
    avg_latency = 1000
    avg_bandwidth = 1000
    if os.path.exists('/esarchive/scratch/pbretonn/monitor-esarchive/plot/io-benchmark/stats-io.txt'):
        output = subprocess.check_output(['tail', '-n', '49', '/esarchive/scratch/pbretonn/monitor-esarchive/plot/io-benchmark/stats-io.txt'])

        if len(output) > 0:
            lines = output.split('\n')[:-1]  # Get rid of last line
            last_line = lines[-1].split()
            try:
                current_bandwidth = float(last_line[1])
            except IndexError:
                # Default to 90.0
                current_bandwidth = 90.0
            try:
                current_latency = float(last_line[2])
            except IndexError:
                current_latency = 2.0
            try:
                last_day = [line.split() for line in lines[:-1]]
                avg_bandwidth = sum(float(last[1])
                                    for last in last_day if len(last) > 1) / len(last_day)
                avg_latency = sum(float(last[2])
                                  for last in last_day if len(last) > 2) / len(last_day)
            except IndexError:
                avg_bandwidth = 90.0
                avg_latency = 2.0

        result.append(True)
    else:
        result.append(False)
    result.append(avg_bandwidth)
    result.append(avg_latency)
    result.append(current_bandwidth)
    result.append(current_latency)


def test_esarchive_status():
    try:
        t0 = time.time()
        manager = multiprocessing.Manager()
        result = manager.list()
        p = multiprocessing.Process(target=read_esarchive, name="ESARCHIVE", args=(result,))
        p.start()
        p.join(10)
        if p.is_alive():
            print("Test running... killing it")
            p.terminate()
            p.join()
            result = [False, -1.0, -1.0, 0.0, 0.0]
        t1 = time.time()
        #print(t1 - t0)
        rtime = t1 - t0
        # print(result)
        status = result[0]
        abandwith = result[1]
        alatency = result[2]
        cbandwidth = result[3]
        clatency = result[4]
        DbRequests.insert_archive_status(
            status, alatency, abandwith, clatency, cbandwidth, rtime)
    except Exception as exp:
        print(traceback.format_exc())
        # error_message = str(exp)


def get_last_test_archive_status():
    error = False
    error_message = ""
    str_status = "OFFLINE"
    latency_warning = None
    bandwidth_warning = None
    response_warning = None
    try:
        status, alatency, abandwidth, clatency, cbandwidth, rtime, date = DbRequests.get_last_read_archive_status()
        if status == 1:
            str_status = "ONLINE"
            # 4.0 as a standard
            latency_warning = "Higher latency than usual" if clatency > (
                alatency + alatency * 0.1) or clatency > 4.0 else None
            # 90.0  as a standard
            bandwidth_warning = "Lower bandwidth than usual" if cbandwidth < (
                abandwidth - abandwidth * 0.1) or cbandwidth < 90.0 else None
            response_warning = "Higher response times than usual" if int(
                rtime) > 1 else None
        else:
            str_status = "OFFLINE"
    except Exception as exp:
        error = True
        error_message = ""

    return {"status": str_status,
            "error": error,
            "error_message": error_message,
            "avg_latency": alatency,
            "avg_bandwidth": abandwidth,
            "current_latency": clatency,
            "current_bandwidth": cbandwidth,
            "reponse_time": rtime,
            "datetime": date,
            "latency_warning": latency_warning,
            "bandwidth_warning": bandwidth_warning,
            "response_warning": response_warning,
            }
