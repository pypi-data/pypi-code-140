import os
import socket
import time
import datetime
import json
import functools
import traceback
import copy

import numpy as np

from zlib import adler32

from pandacommon.pandalogger.PandaLogger import PandaLogger
from pandacommon.pandalogger import logger_utils

from pandaserver.config import panda_config
from pandaserver.daemons.scripts.metric_collector import MetricsDB

from scipy import stats


# logger
main_logger = PandaLogger().getLogger('task_evaluator')

# dry run
DRY_RUN = False

# list of metrics in FetchData to fetch data and update to DB. Format: (metric, period_minutes)
metric_list = [
    ('analy_task_eval', 10),
]

# constant maps
# class_value_rank_map = {1: 'A_sites', 0: 'B_sites', -1: 'C_sites'}


class TaskEvaluationDB(object):
    """
    Proxy to access the task_evaluation table in DB
    """

    def __init__(self, tbuf):
        self.tbuf = tbuf

    def _decor(method):
        def _decorator(_method, *args, **kwargs):
            @functools.wraps(_method)
            def _wrapped_method(self, *args, **kwargs):
                try:
                    _method(self, *args, **kwargs)
                except Exception as exc:
                    pass
            return _wrapped_method
        return _decorator(method)

    def update(self, metric, entity_dict):
        tmp_log = logger_utils.make_logger(main_logger, 'TaskEvaluationDB.update')
        tmp_log.debug('start metric={}'.format(metric))
        # sql
        sql_query_taskid = (
            """SELECT jediTaskID """
            """FROM ATLAS_PANDA.Task_Evaluation """
            """WHERE metric = :metric """
        )
        sql_update = (
            """UPDATE ATLAS_PANDA.Task_Evaluation SET """
                """value_json = :patch_value_json, """
                """timestamp = :timestamp """
            """WHERE jediTaskID=:taskID AND metric=:metric """
        )
        sql_insert = (
            """INSERT INTO ATLAS_PANDA.Task_Evaluation """
                """VALUES ( """
                    """:taskID, :metric, :patch_value_json, :timestamp """
                """) """
        )
        # now
        now_time = datetime.datetime.utcnow()
        # get existing taskID list
        res = self.tbuf.querySQL(sql_query_taskid, {':metric': metric})
        existing_taskID_list = [ taskID for (taskID, ) in res ]
        # var map template
        varMap_template = {
            ':taskID': None,
            ':metric': metric,
            ':timestamp': now_time,
            ':patch_value_json': None
        }
        # make var map lists
        update_varMap_list = []
        insert_varMap_list = []
        for taskID, v in entity_dict.items():
            # values to json string
            try:
                patch_value_json = json.dumps(v)
            except Exception:
                tmp_log.error(traceback.format_exc() + ' ' + str(v))
                return
            # update varMap
            varMap = varMap_template.copy()
            varMap[':taskID'] = taskID
            varMap[':patch_value_json'] = patch_value_json
            # append to the list
            if taskID in existing_taskID_list:
                update_varMap_list.append(varMap)
            else:
                insert_varMap_list.append(varMap)
        # update
        n_row = self.tbuf.executemanySQL(sql_update, update_varMap_list)
        if n_row < len(update_varMap_list):
            tmp_log.warning('only {n_row}/{len_list} rows updated for metric={metric}'.format(
                                n_row=n_row, len_list=len(update_varMap_list), metric=metric))
        else:
            tmp_log.debug('updated {len_list} rows for metric={metric}'.format(
                            metric=metric, len_list=len(update_varMap_list)))
        # insert
        n_row = self.tbuf.executemanySQL(sql_insert, insert_varMap_list)
        if n_row < len(insert_varMap_list):
            tmp_log.warning('only {n_row}/{len_list} rows inserted for metric={metric}'.format(
                                n_row=n_row, len_list=len(insert_varMap_list), metric=metric))
        else:
            tmp_log.debug('inserted {len_list} rows for metric={metric}'.format(
                            metric=metric, len_list=len(insert_varMap_list)))
        # done
        tmp_log.debug('done metric={}'.format(metric))

    def get_metrics(self, metric, fresher_than_minutes_ago=120):
        tmp_log = logger_utils.make_logger(main_logger, 'TaskEvaluationDB.update')
        tmp_log.debug('start metric={}'.format(metric))
        # sql
        sql_query = (
            """SELECT jediTaskID, value_json """
            """FROM ATLAS_PANDA.Task_Evaluation """
            """WHERE metric = :metric """
                """AND timestamp >= :min_timestamp """
        )
        # now
        now_time = datetime.datetime.utcnow()
        # var map
        varMap = {
            ':metric': metric,
            ':min_timestamp': now_time - datetime.timedelta(minutes=fresher_than_minutes_ago),
        }
        # query
        res = self.tbuf.querySQL(sql_query, varMap)
        if res is None:
            tmp_log.warning('failed to query metric={metric}'.format(metric=metric))
            return
        # return map
        ret_map = {}
        for (taskID, value_json) in res:
            try:
                ret_map[taskID] = value_dict
            except Exception:
                tmp_log.error(traceback.format_exc() + ' ' + str(taskID) + str(value_json))
                continue
        # return
        return ret_map

    def clean_up(self, metric, fresher_than_minutes_ago=120):
        tmp_log = logger_utils.make_logger(main_logger, 'TaskEvaluationDB.clean_up')
        tmp_log.debug('start metric={}'.format(metric))
        #sql
        sql_delete_terminated_tasks = (
            "DELETE "
            "FROM ATLAS_PANDA.Task_Evaluation te "
            "WHERE te.jediTaskID IN ( "
                    "SELECT jt.jediTaskID "
                    "FROM ATLAS_PANDA.JEDI_Tasks jt, ATLAS_PANDA.Task_Evaluation tez "
                    "WHERE tez.jediTaskID = jt.jediTaskID "
                        "AND jt.status IN ('done', 'finished', 'failed', 'broken', 'aborted', 'exhausted') "
                ") "
                "AND te.metric = :metric "
                "AND te.timestamp <= :max_timestamp "
        )
        # now
        now_time = datetime.datetime.utcnow()
        # var map
        varMap = {
            ':metric': metric,
            ':max_timestamp': now_time - datetime.timedelta(minutes=fresher_than_minutes_ago),
        }
        # clean up
        n_row = self.tbuf.querySQL(sql_delete_terminated_tasks, varMap)
        tmp_log.debug('cleaned up {n_row} rows for metric={metric}'.format(
                        metric=metric, n_row=n_row))



class FetchData(object):
    """
    methods to fetch or evaluate data values to store
    """

    def __init__(self, tbuf):
        self.tbuf = tbuf
        # initialize stored data
        self.gshare_status = None

    def analy_task_eval(self):
        tmp_log = logger_utils.make_logger(main_logger, 'FetchData')
        #sql
        sql_get_active_tasks = (
            "SELECT jt.jediTaskID, jt.userName, jt.gshare "
            "FROM ATLAS_PANDA.JEDI_Tasks jt, ATLAS_PANDA.JEDI_AUX_Status_MinTaskID asm "
            "WHERE jt.taskType = 'anal' AND jt.prodSourceLabel = 'user' "
                "AND jt.status=asm.status AND jt.jediTaskID >= asm.min_jediTaskID "
                "AND jt.status IN ('scouting', 'scouted', 'running', 'pending', 'throttled') "
                "AND jt.userName NOT IN ('gangarbt') "
                "AND jt.modificationTime >= CURRENT_DATE - 30 "
        )
        sql_get_task_dsinfo = (
            "SELECT ds.jediTaskID, SUM(ds.nFiles), SUM(ds.nFilesFinished), SUM(ds.nFilesFailed) "
            "FROM ATLAS_PANDA.JEDI_Datasets ds "
            "WHERE ds.jediTaskID = :taskID "
                "AND ds.type IN ('input', 'pseudo_input') "
                "AND ds.masterID IS NULL "
            "GROUP BY ds.jediTaskID "
        )
        try:
            # initialize
            # tmp_site_dict = dict()
            task_dict = dict()
            # now time
            now_time = datetime.datetime.utcnow()
            # MetricsDB
            mdb = MetricsDB(self.tbuf)
            # get user evaluation
            ue_dict = mdb.get_metrics('analy_user_eval', 'neither', fresher_than_minutes_ago=20)
            # get active tasks
            varMap = {}
            active_tasks_list = self.tbuf.querySQL(sql_get_active_tasks, varMap)
            taskID_list = [ task[0] for task in active_tasks_list ]
            n_tot_tasks = len(active_tasks_list)
            tmp_log.debug('got total {0} tasks'.format(n_tot_tasks))
            # counter
            cc = 0
            # loop over tasks
            for taskID, user, gshare in active_tasks_list:
                # initialize
                task_class = 1
                n_files_total = 0
                n_files_finished = 0
                n_files_failed = 0
                pct_finished = 0
                pct_failed = 0
                # get dataset info of each task
                varMap = {':taskID': taskID}
                dsinfo_list = self.tbuf.querySQL(sql_get_task_dsinfo, varMap)
                dsinfo_dict = { tup[0]: {'nFiles': tup[1], 'nFilesFinished': tup[2], 'nFilesFailed': tup[3]} \
                                for tup in dsinfo_list  }
                # get task proceeding progress
                ds_info = dsinfo_dict.get(taskID)
                if ds_info is not None:
                    n_files_total = ds_info.get('nFiles', 0)
                    n_files_finished = ds_info.get('nFilesFinished', 0)
                    n_files_failed = ds_info.get('nFilesFailed', 0)
                    if n_files_total > 0:
                        pct_finished = n_files_finished*100/n_files_total
                        pct_failed = n_files_failed*100/n_files_total
                # classify
                # parameters
                progress_to_boost_A = self.tbuf.getConfigValue('analy_eval', 'PROGRESS_TO_BOOST_A')
                if progress_to_boost_A is None:
                    progress_to_boost_A = 90
                progress_to_boost_B = self.tbuf.getConfigValue('analy_eval', 'PROGRESS_TO_BOOST_B')
                if progress_to_boost_B is None:
                    progress_to_boost_B = 95
                # check usage of the user
                usage_dict = ue_dict.get(user)
                if usage_dict is None:
                    continue
                if usage_dict['rem_slots_A'] <= 0:
                    if usage_dict['rem_slots_B'] <= 0:
                        task_class = -1
                    else:
                        task_class = 0
                # boost for nearly done tasks
                if task_class == 1 and pct_finished >= progress_to_boost_A:
                    # almost done A-tasks, to boost
                    task_class = 2
                elif task_class == 0 and pct_finished >= progress_to_boost_B:
                    # almost done B-tasks, to boost
                    task_class = 2
                # fill in task class
                task_dict[taskID] = {
                        'task_id': taskID,
                        'user': user,
                        'gshare': gshare,
                        'n_files_total': n_files_total,
                        'n_files_finished': n_files_finished,
                        'n_files_failed': n_files_failed,
                        'pct_finished': pct_finished,
                        'pct_failed': pct_failed,
                        'class': task_class,
                    }
                # counter
                cc += 1
                if cc % 5000 == 0:
                    tmp_log.debug('evaluated {0:9d} tasks'.format(cc))
            tmp_log.debug('evaluated {0:9d} tasks in total'.format(cc))
            # return
            # tmp_log.debug('{}'.format(str([ v for v in task_dict.values() if v['class'] != 1 ])[:3000]))
            tmp_log.debug('done')
            return task_dict
        except Exception:
            tmp_log.error(traceback.format_exc())


# main
def main(tbuf=None, **kwargs):
    # instantiate TB
    if tbuf is None:
        from pandaserver.taskbuffer.TaskBuffer import taskBuffer
        taskBuffer.init(panda_config.dbhost, panda_config.dbpasswd, nDBConnection=1, useTimeout=True)
    else:
        taskBuffer = tbuf
    # pid
    my_pid = os.getpid()
    my_full_pid = '{0}-{1}-{2}'.format(socket.getfqdn().split('.')[0], os.getpgrp(), my_pid)
    # go
    if DRY_RUN:
        # dry run, regardless of lock, not update DB
        fetcher = FetchData(taskBuffer)
        # loop over all fetch data methods to run and update to DB
        for metric_name, period in metric_list:
            main_logger.debug('(dry-run) start {metric_name}'.format(metric_name=metric_name))
            # fetch data and update DB
            the_method = getattr(fetcher, metric_name)
            fetched_data = the_method()
            if fetched_data is None:
                main_logger.warning('(dry-run) {metric_name} got no valid data'.format(metric_name=metric_name))
                continue
            main_logger.debug('(dry-run) done {metric_name}'.format(metric_name=metric_name))
    else:
        # real run, will update DB
        # instantiate
        tedb = TaskEvaluationDB(taskBuffer)
        fetcher = FetchData(taskBuffer)
        # loop over all fetch data methods to run and update to DB
        for metric_name, period in metric_list:
            # metric lock
            lock_component_name = 'pandaTaskEval.{0:.30}.{1:0x}'.format(metric_name, adler32(metric_name.encode('utf-8')))
            # try to get lock
            got_lock = taskBuffer.lockProcess_PANDA(component=lock_component_name, pid=my_full_pid, time_limit=period)
            if got_lock:
                main_logger.debug('got lock of {metric_name}'.format(metric_name=metric_name))
            else:
                main_logger.debug('{metric_name} locked by other process; skipped...'.format(metric_name=metric_name))
                continue
            main_logger.debug('start {metric_name}'.format(metric_name=metric_name))
            # clean up
            tedb.clean_up(metric=metric_name, fresher_than_minutes_ago=120)
            main_logger.debug('cleaned up {metric_name}'.format(metric_name=metric_name))
            # fetch data and update DB
            the_method = getattr(fetcher, metric_name)
            fetched_data = the_method()
            if fetched_data is None:
                main_logger.warning('{metric_name} got no valid data'.format(metric_name=metric_name))
                continue
            tedb.update(metric=metric_name, entity_dict=fetched_data)
            main_logger.debug('done {metric_name}'.format(metric_name=metric_name))

# run
if __name__ == '__main__':
    main()
