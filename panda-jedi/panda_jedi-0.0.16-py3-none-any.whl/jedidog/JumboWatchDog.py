import os
import sys
import socket
import traceback

from six import iteritems

from pandajedi.jedicore.JediTaskSpec import JediTaskSpec

# watchdog to take actions for jumbo jobs
class JumboWatchDog:

    # constructor
    def __init__(self, taskBufferIF, ddmIF, log, vo, prodSourceLabel):
        self.taskBufferIF = taskBufferIF
        self.ddmIF = ddmIF
        self.pid = '{0}-{1}_{2}-jumbo'.format(socket.getfqdn().split('.')[0], os.getpid(), os.getpgrp())
        self.log = log
        self.vo = vo
        self.prodSourceLabel = prodSourceLabel
        self.component = 'JumboWatchDog'
        self.dryRun = True


    # main
    def run(self):
        try:
            # get process lock
            locked = self.taskBufferIF.lockProcess_JEDI(vo=self.vo, prodSourceLabel=self.prodSourceLabel,
                                                        cloud=None, workqueue_id=None, resource_name=None,
                                                        component=self.component, pid=self.pid, timeLimit=10)
            if not locked:
                self.log.debug('component={0} skipped since locked by another'.format(self.component))
                return
            # get parameters for conversion
            self.log.debug('component={0} start'.format(self.component))
            maxTasks = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MAX_TASKS', 'jedi', self.vo)
            if maxTasks is None:
                maxTasks = 1
            nEventsToDisable = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MIN_EVENTS_DISABLE', 'jedi', self.vo)
            if nEventsToDisable is None:
                nEventsToDisable = 100000
            nEventsToEnable = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MIN_EVENTS_ENABLE', 'jedi', self.vo)
            if nEventsToEnable is None:
                nEventsToEnable = nEventsToDisable * 10
            maxEvents = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MAX_EVENTS', 'jedi', self.vo)
            if maxEvents is None:
                maxEvents = maxTasks * nEventsToEnable // 2
            nJumboPerTask = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_PER_TASK', 'jedi', self.vo)
            if nJumboPerTask is None:
                nJumboPerTask = 1
            nJumboPerSite = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_PER_SITE', 'jedi', self.vo)
            if nJumboPerSite is None:
                nJumboPerSite = 1
            maxPrio = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MAX_CURR_PRIO', 'jedi', self.vo)
            if maxPrio is None:
                maxPrio = 500
            progressToBoost = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_PROG_TO_BOOST', 'jedi', self.vo)
            if progressToBoost is None:
                progressToBoost = 95
            maxFilesToBoost = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_MAX_FILES_TO_BOOST', 'jedi', self.vo)
            if maxFilesToBoost is None:
                maxFilesToBoost = 500
            prioToBoost = 900
            prioWhenDisabled = self.taskBufferIF.getConfigValue(self.component, 'JUMBO_PRIO_DISABLED', 'jedi', self.vo)
            if prioWhenDisabled is None:
                prioWhenDisabled = 500
            # get current info
            tasksWithJumbo = self.taskBufferIF.getTaskWithJumbo_JEDI(self.vo, self.prodSourceLabel)
            totEvents = 0
            doneEvents = 0
            nTasks = 0
            for jediTaskID, taskData in iteritems(tasksWithJumbo):
                # disable jumbo
                if taskData['useJumbo'] != JediTaskSpec.enum_useJumbo['disabled'] and taskData['site'] is None:
                    if  taskData['nEvents'] - taskData['nEventsDone'] < nEventsToDisable:
                        # disable
                        self.log.info('component={0} disable jumbo in jediTaskID={1} due to n_events_to_process={2} < {3}'.format(self.component, jediTaskID,
                                                                                                                                  taskData['nEvents'] - taskData['nEventsDone'],
                                                                                                                                  nEventsToDisable))
                        self.taskBufferIF.enableJumboJobs(jediTaskID, 0, 0)
                    else:
                        # wait
                        nTasks += 1
                        totEvents += taskData['nEvents']
                        doneEvents += taskData['nEventsDone']
                        self.log.info('component={0} keep jumbo in jediTaskID={1} due to n_events_to_process={2} > {3}'.format(self.component, jediTaskID,
                                                                                                                               taskData['nEvents'] - taskData['nEventsDone'],
                                                                                                                               nEventsToDisable))
                # increase priority for jumbo disabled
                if taskData['useJumbo'] == JediTaskSpec.enum_useJumbo['disabled'] and taskData['currentPriority'] < prioWhenDisabled:
                    self.taskBufferIF.changeTaskPriorityPanda(jediTaskID, prioWhenDisabled)
                    self.log.info('component={0} priority boost to {1} after disabing jumbo in in jediTaskID={2}'.format(self.component, prioWhenDisabled, jediTaskID))
                # increase priority when close to completion
                if taskData['nEvents'] > 0 and (taskData['nEvents'] - taskData['nEventsDone']) * 100 // taskData['nEvents'] < progressToBoost \
                        and taskData['currentPriority'] < prioToBoost and (taskData['nFiles'] - taskData['nFilesDone']) < maxFilesToBoost:
                    # boost
                    tmpStr = 'component={0} priority boost to {5} for jediTaskID={1} due to n_events_done={2} > {3}*{4}% '.format(self.component, jediTaskID,
                                                                                                                                  taskData['nEventsDone'],
                                                                                                                                  taskData['nEvents'],
                                                                                                                                  progressToBoost,
                                                                                                                                  prioToBoost)
                    tmpStr += 'n_files_remaining={0} < {1}'.format(taskData['nFiles'] - taskData['nFilesDone'], maxFilesToBoost)
                    self.log.info(tmpStr)
                    self.taskBufferIF.changeTaskPriorityPanda(jediTaskID, prioToBoost)
                # kick pending
                if taskData['taskStatus'] in ['pending', 'running'] and taskData['useJumbo'] in [JediTaskSpec.enum_useJumbo['pending'], JediTaskSpec.enum_useJumbo['running']]:
                    nActiveJumbo = 0
                    for computingSite, jobStatusMap in iteritems(taskData['jumboJobs']):
                        for jobStatus, nJobs in iteritems(jobStatusMap):
                            if jobStatus in ['defined', 'assigned', 'activated', 'sent', 'starting', 'running', 'transferring', 'holding']:
                                nActiveJumbo += nJobs
                    if nActiveJumbo == 0:
                        self.log.info('component={0} kick jumbo in {2} jediTaskID={1}'.format(self.component,
                                                                                              jediTaskID,
                                                                                              taskData['taskStatus']))
                        self.taskBufferIF.kickPendingTasksWithJumbo_JEDI(jediTaskID)
                # reset input to re-generate co-jumbo
                if taskData['currentPriority'] >= prioToBoost:
                    nReset = self.taskBufferIF.resetInputToReGenCoJumbo_JEDI(jediTaskID)
                    if nReset is not None and nReset > 0:
                        self.log.info('component={0} reset {1} inputs to regenerate co-jumbo for jediTaskID={2}'.format(self.component, nReset, jediTaskID))
                    else:
                        self.log.debug('component={0} tried to reset inputs to regenerate co-jumbo with {1} for jediTaskID={2}'.format(self.component, nReset, jediTaskID))
            self.log.info('component={0} total_events={1} n_events_to_process={2} n_tasks={3} available for jumbo'.format(self.component, totEvents,
                                                                                                                          totEvents - doneEvents, nTasks))

            self.log.debug('component={0} done'.format(self.component))
        except Exception:
            # error
            errtype, errvalue = sys.exc_info()[:2]
            errStr = ": %s %s" % (errtype.__name__, errvalue)
            errStr.strip()
            errStr += traceback.format_exc()
            self.log.error(errStr)
