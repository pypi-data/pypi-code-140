""" LSF mn adaptor implementation
"""

import re
import os
import time
import threading
# noinspection PyDeprecation
from cgi import parse_qs

# noinspection PyPackageRequirements
import radical.utils.threads as sut
import radical.saga as saga
import saga.url as surl
import saga.utils.pty_shell
import saga.adaptors.base
import saga.adaptors.cpi.job

import saga.adaptors.cpi.decorators

SYNC_CALL = saga.adaptors.cpi.decorators.SYNC_CALL
ASYNC_CALL = saga.adaptors.cpi.decorators.ASYNC_CALL

SYNC_WAIT_UPDATE_INTERVAL = 1  # seconds
MONITOR_UPDATE_INTERVAL = 3  # seconds


# --------------------------------------------------------------------
#
# noinspection PyProtectedMember,PyPep8Naming,PyMissingOrEmptyDocstring
class _job_state_monitor(threading.Thread):
    """ thread that periodically monitors job states
    """

    def __init__(self, job_service):

        self.logger = job_service._logger
        self.js = job_service
        self._stop = sut.Event()

        super(_job_state_monitor, self).__init__()
        self.setDaemon(True)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while self.stopped() is False:
            try:
                # do bulk updates here! we don't want to pull information
                # job by job. that would be too inefficient!
                jobs = self.js.jobs
                job_keys = jobs.keys()

                for job in job_keys:
                    # if the job hasn't been started, we can't update its
                    # state. we can tell if a job has been started if it
                    # has a job id
                    if jobs[job].get('job_id', None) is not None:
                        # we only need to monitor jobs that are not in a
                        # terminal state, so we can skip the ones that are
                        # either done, failed or canceled
                        state = jobs[job]['state']
                        if state not in [saga.job.DONE, saga.job.FAILED, saga.job.CANCELED]:

                            job_info = self.js._job_get_info(job)
                            self.logger.info(
                                "Job monitoring thread updating Job %s (state: %s)" % (job, job_info['state']))

                            if job_info['state'] != state:
                                # fire job state callback if 'state' has changed
                                job._api()._attributes_i_set('state', job_info['state'], job._api()._UP, True)

                            # update job info
                            self.js.jobs[job] = job_info

                time.sleep(MONITOR_UPDATE_INTERVAL)
            except Exception as e:
                self.logger.warning("Exception caught in job monitoring thread: %s" % e)


# --------------------------------------------------------------------
#
def log_error_and_raise(message, exception, logger):
    """
    logs an 'error' message and subsequently throws an exception

    :param message: message to log
    :param exception: exception to rise
    :param logger: logger to use
    """
    logger.error(message)
    raise exception(message)


# --------------------------------------------------------------------
#
def _mn_to_saga_jobstate(mnjs):
    """ translates a mn one-letter state to saga
    """
    if mnjs in ['RUN']:
        return saga.job.RUNNING
    elif mnjs in ['WAIT', 'PEND']:
        return saga.job.PENDING
    elif mnjs in ['DONE']:
        return saga.job.DONE
    elif mnjs in ['ZOMBI', 'EXIT']:
        return saga.job.FAILED
    elif mnjs in ['USUSP', 'SSUSP', 'PSUSP']:
        return saga.job.SUSPENDED
    else:
        return saga.job.UNKNOWN


# --------------------------------------------------------------------
#
def _mnscript_generator(jd, queue=None):
    """ generates an LSF script from a SAGA job description
    """
    mn_params = str()
    exec_n_args = str()

    if jd.executable is not None:
        exec_n_args += "%s " % jd.executable
    if jd.arguments is not None:
        for arg in jd.arguments:
            exec_n_args += "%s " % arg

    if jd.name is not None:
        mn_params += "#BSUB -J %s \n" % jd.name

    if jd.environment is not None:
        env_variable_list = "export "
        for key in jd.environment.keys():
            env_variable_list += " %s=%s " % (key, jd.environment[key])
    else:
        env_variable_list = ""

    # a workaround is to do an explicit 'cd'
    if jd.working_directory is not None:
        mn_params += "#BSUB -cwd %s \n" % jd.working_directory

    if jd.output is not None:
        # if working directory is set, we want stdout to end up in
        # the working directory as well, unless it containes a specific
        # path name.
        if jd.working_directory is not None:
            if os.path.isabs(jd.output):
                mn_params += "#BSUB -o %s \n" % jd.output
            else:
                # user provided a relative path for STDOUT. in this case
                # we prepend the working directory path before passing
                # it on to LSF.
                mn_params += "#BSUB -o %s/%s \n" % (jd.working_directory, jd.output)
        else:
            mn_params += "#BSUB -o %s \n" % jd.output

    if jd.error is not None:
        # if working directory is set, we want stderr to end up in
        # the working directory as well, unless it contains a specific
        # path name.
        if jd.working_directory is not None:
            if os.path.isabs(jd.error):
                mn_params += "#BSUB -e %s \n" % jd.error
            else:
                # user provided a relative path for STDERR. in this case
                # we prepend the working directory path before passing
                # it on to LSF.
                mn_params += "#BSUB -e %s/%s \n" % (jd.working_directory, jd.error)
        else:
            mn_params += "#BSUB -e %s \n" % jd.error

    if jd.wall_time_limit is not None:
        hours = jd.wall_time_limit / 60
        minutes = jd.wall_time_limit % 60
        mn_params += "#BSUB -W %s:%s \n" \
                     % (str(hours), str(minutes))

    if (jd.queue is not None) and (queue is not None):
        mn_params += "#BSUB -q %s \n" % queue
    elif (jd.queue is not None) and (queue is None):
        mn_params += "#BSUB -q %s \n" % jd.queue
    elif (jd.queue is None) and (queue is not None):
        mn_params += "#BSUB -q %s \n" % queue

    if jd.project is not None:
        if ':' not in jd.project:
            account = jd.project
        else:
            account, reservation, exclusivity = jd.project.split(':')
            if reservation != '':
                mn_params += "#BSUB -U %s \n" % str(reservation)
            if exclusivity == 'true':
                mn_params += "#BSUB -x \n"

        mn_params += "#BSUB -P %s \n" % str(account)
    if jd.job_contact is not None:
        mn_params += "#BSUB -u %s \n" % str(jd.job_contact)

    # if total_cpu_count is not defined, we assume 1
    if jd.total_cpu_count is None:
        jd.total_cpu_count = 1

    mn_params += "#BSUB -n %s \n" % str(jd.total_cpu_count)

    if jd.processes_per_host:
        mn_params += '#BSUB -R "span[ptile=%s]"\n' % str(jd.processes_per_host)

    # escape all double quotes and dollarsigns, otherwise 'echo |'
    # further down won't work
    # only escape '$' in args and exe. not in the params
    # exec_n_args = workdir_directives exec_n_args
    exec_n_args = exec_n_args.replace('$', '\\$')

    mnscript = "\n#!/bin/bash \n%s\n%s\n%s" % (mn_params, env_variable_list, exec_n_args)

    mnscript = mnscript.replace('"', '\\"')
    return mnscript

# --------------------------------------------------------------------
# some private defs
#
_PTY_TIMEOUT = 2.0

# --------------------------------------------------------------------
# the adaptor name
#
_ADAPTOR_NAME = "autosubmit.platforms.mn_adaptor"
_ADAPTOR_SCHEMAS = ["mn", "mn+ssh", "mn+gsissh"]
_ADAPTOR_OPTIONS = []

# --------------------------------------------------------------------
# the adaptor capabilities & supported attributes
#
_ADAPTOR_CAPABILITIES = {
    "jdes_attributes": [saga.job.NAME,
                        saga.job.EXECUTABLE,
                        saga.job.ARGUMENTS,
                        saga.job.ENVIRONMENT,
                        saga.job.INPUT,
                        saga.job.OUTPUT,
                        saga.job.ERROR,
                        saga.job.QUEUE,
                        saga.job.PROJECT,
                        saga.job.WALL_TIME_LIMIT,
                        saga.job.WORKING_DIRECTORY,
                        saga.job.SPMD_VARIATION,  # TODO: 'hot'-fix for BigJob
                        saga.job.PROCESSES_PER_HOST,
                        saga.job.TOTAL_CPU_COUNT],
    "job_attributes": [saga.job.EXIT_CODE,
                       saga.job.EXECUTION_HOSTS,
                       saga.job.CREATED,
                       saga.job.STARTED,
                       saga.job.FINISHED],
    "metrics": [saga.job.STATE],
    "callbacks": [saga.job.STATE],
    "contexts": {"ssh": "SSH public/private keypair",
                 "x509": "GSISSH X509 proxy context",
                 "userpass": "username/password pair (ssh)"}
}

# --------------------------------------------------------------------
# the adaptor documentation
#
_ADAPTOR_DOC = {
    "name": _ADAPTOR_NAME,
    "cfg_options": _ADAPTOR_OPTIONS,
    "capabilities": _ADAPTOR_CAPABILITIES,
    "description": """
The MN adaptor allows to run and manage jobs on MareNostrum 3
""",
    "schemas": {"mn": "connect to a local cluster",
                "mn+ssh": "connect to a remote cluster via SSH",
                "mn+gsissh": "connect to a remote cluster via GSISSH"}
}

# --------------------------------------------------------------------
# the adaptor info is used to register the adaptor with SAGA
#
_ADAPTOR_INFO = {
    "name": _ADAPTOR_NAME,
    "version": "v0.2",
    "schemas": _ADAPTOR_SCHEMAS,
    "capabilities": _ADAPTOR_CAPABILITIES,
    "cpis": [
        {
            "type": "saga.job.Service",
            "class": "MNJobService"
        },
        {
            "type": "saga.job.Job",
            "class": "MNJob"
        }
    ]
}


###############################################################################
# The adaptor class
# noinspection PyMissingOrEmptyDocstring
class Adaptor(saga.adaptors.base.Base):
    """ this is the actual adaptor class, which gets loaded by SAGA (i.e. by
        the SAGA engine), and which registers the CPI implementation classes
        which provide the adaptor's functionality.
    """

    # ----------------------------------------------------------------
    #
    def __init__(self):
        # noinspection PyCallByClass,PyTypeChecker
        saga.adaptors.base.Base.__init__(self, _ADAPTOR_INFO, _ADAPTOR_OPTIONS)

        self.id_re = re.compile('^\[(.*)\]-\[(.*?)\]$')
        self.opts = self.get_config(_ADAPTOR_NAME)

    # ----------------------------------------------------------------
    #
    def sanity_check(self):
        # FIXME: also check for gsissh
        pass

    # ----------------------------------------------------------------
    #
    def parse_id(self, job_id):
        # split the id '[rm]-[pid]' in its parts, and return them.

        match = self.id_re.match(job_id)

        if not match or len(match.groups()) != 2:
            raise saga.BadParameter("Cannot parse job id '%s'" % job_id)

        return match.group(1), match.group(2)


###############################################################################
#
# noinspection PyMethodOverriding,PyMethodOverriding,PyProtectedMember, PyMissingOrEmptyDocstring
class MNJobService(saga.adaptors.cpi.job.Service):
    """ implements saga.adaptors.cpi.job.Service
    """

    # ----------------------------------------------------------------
    #
    # noinspection PyMissingConstructor
    def __init__(self, api, adaptor):

        self._mt = None
        _cpi_base = super(MNJobService, self)
        _cpi_base.__init__(api, adaptor)

        self._adaptor = adaptor

    # ----------------------------------------------------------------
    #
    def __del__(self):

        self.close()

    # ----------------------------------------------------------------
    #
    def close(self):

        if self.mt:
            self.mt.stop()
            self.mt.join(10)  # don't block forever on join()

        self._logger.info("Job monitoring thread stopped.")

        self.finalize(True)

    # ----------------------------------------------------------------
    #
    def finalize(self, kill_shell=False):

        if kill_shell:
            if self.shell:
                self.shell.finalize(True)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def init_instance(self, adaptor_state, rm_url, session):
        """
        service instance constructor

        :param adaptor_state: state of the adaptor
        :param rm_url: machine url
        :param session: SAGA session to use
        """
        self.rm = rm_url
        self.session = session
        self.ppn = 1
        self.queue = None
        self.shell = None
        self.jobs = dict()

        # the monitoring thread - one per service instance
        # noinspection PyTypeChecker
        self.mt = _job_state_monitor(job_service=self)
        self.mt.start()

        rm_scheme = rm_url.scheme
        pty_url = surl.Url(rm_url)

        # this adaptor supports options that can be passed via the
        # 'query' component of the job service URL.
        if rm_url.query is not None:
            # noinspection PyDeprecation
            for key, val in parse_qs(rm_url.query).iteritems():
                if key == 'queue':
                    self.queue = val[0]
                elif key == 'span':
                    self.span = val[0]

        # we need to extrac the scheme for PTYShell. That's basically the
        # job.Serivce Url withou the mn+ part. We use the PTYShell to execute
        # mn commands either locally or via gsissh or ssh.
        if rm_scheme == "mn":
            pty_url.scheme = "fork"
        elif rm_scheme == "mn+ssh":
            pty_url.scheme = "ssh"
        elif rm_scheme == "mn+gsissh":
            pty_url.scheme = "gsissh"

        # these are the commands that we need in order to interact with LSF.
        # the adaptor will try to find them during initialize(self) and bail
        # out in case they are note avaialbe.
        self._commands = {'bqueues': '9.1.2.0',
                          'bjobs': '9.1.2.0',
                          'bsub': '9.1.2.0',
                          'bkill': '9.1.2.0'}

        self.shell = saga.utils.pty_shell.PTYShell(pty_url, self.session)

        # self.shell.set_initialize_hook(self.initialize)
        # self.shell.set_finalize_hook(self.finalize)

        self.initialize()
        return self.get_api()

    # ----------------------------------------------------------------
    #
    def initialize(self):
        # check if all required mn tools are available
        # for cmd in self._commands.keys():
        #     ret, out, _ = self.shell.run_sync("which %s " % cmd)
        #     if ret != 0:
        #         message = "Couldn't find LSF tools: %s" % out
        #         log_error_and_raise(message, saga.NoSuccess, self._logger)
        #     else:
        #         path = out.strip()  # strip removes newline
        #     ret, out, _ = self.shell.run_sync("%s -V" % cmd)
        #     if ret != 0:
        #         message = "Couldn't find LSF tools: %s" % out
        #         log_error_and_raise(message, saga.NoSuccess, self._logger)
        #     else:
        #         # version is reported as: "version: x.y.z"
        #         version = out.split("\n")[0]
        #
        #         # add path and version to the command dictionary
        #         self._commands[cmd] = {"path":    cmd,
        #                                "version": version}

        self._logger.info("Found LSF tools: %s" % self._commands)

        # see if we can get some information about the cluster, e.g.,
        # different queues, number of processes per node, etc.
        # TODO: this is quite a hack. however, it *seems* to work quite
        #       well in practice.
        # ret, out, _ = self.shell.run_sync('unset GREP_OPTIONS; %s -a | grep -E "(np|pcpu)"' % \
        #    self._commands['pbsnodes']['path'])
        # if ret != 0:
        #
        #    message = "Error running pbsnodes: %s" % out
        #    log_error_and_raise(message, saga.NoSuccess, self._logger)
        # else:
        # this is black magic. we just assume that the highest occurence
        # of a specific np is the number of processors (cores) per compute
        # node. this equals max "PPN" for job scripts
        #    ppn_list = dict()
        #    for line in out.split('\n'):
        #        np = line.split(' = ')
        #        if len(np) == 2:
        #            np = np[1].strip()
        #            if np in ppn_list:
        #                ppn_list[np] += 1
        #            else:
        #                ppn_list[np] = 1
        #    self.ppn = max(ppn_list, key=ppn_list.get)
        #    self._logger.debug("Found the following 'ppn' configurations: %s. \

    # Using %s as default ppn."
    #           % (ppn_list, self.ppn))

    # ----------------------------------------------------------------
    #
    def _job_run(self, job_obj):
        """ runs a job via qsub
        """
        # get the job description
        jd = job_obj.jd

        # normalize working directory path
        if jd.working_directory:
            jd.working_directory = os.path.normpath(jd.working_directory)

        if (self.queue is not None) and (jd.queue is not None):
            self._logger.warning("Job service was instantiated explicitly with \
'queue=%s', but job description tries to a differnt queue: '%s'. Using '%s'." %
                                 (self.queue, jd.queue, self.queue))

        try:
            # create an LSF job script from SAGA job description
            script = _mnscript_generator(jd=jd, queue=self.queue)

            self._logger.info("Generated LSF script: %s" % script)
        except Exception as ex:
            script = ''
            log_error_and_raise(str(ex), saga.BadParameter, self._logger)

        # try to create the working directory (if defined)
        # WARNING: this assumes a shared filesystem between login node and
        #          compute nodes.
        if jd.working_directory is not None:
            self._logger.info("Creating working directory %s" % jd.working_directory)
            ret, out, _ = self.shell.run_sync("mkdir -p %s" % jd.working_directory)
            if ret != 0:
                # something went wrong
                message = "Couldn't create working directory - %s" % out
                log_error_and_raise(message, saga.NoSuccess, self._logger)

        # Now we want to execute the script. This process consists of two steps:
        # (1) we create a temporary file with 'mktemp' and write the contents of
        #     the generated PBS script into it
        # (2) we call 'qsub <tmpfile>' to submit the script to the queueing system
        # noinspection PyPep8
        cmdline = """SCRIPTFILE=`mktemp -t SAGA-Python-LSFJobScript.XXXXXX` && echo "%s" > $SCRIPTFILE && %s < $SCRIPTFILE && rm -f $SCRIPTFILE""" % (script, 'bsub')
        ret, out, _ = self.shell.run_sync(cmdline)

        if ret != 0:
            # something went wrong
            message = "Error running job via 'bsub': %s. Commandline was: %s" \
                      % (out, cmdline)
            log_error_and_raise(message, saga.NoSuccess, self._logger)
        else:
            # parse the job id. bsub's output looks like this:
            # Job <901545> is submitted to queue <regular>
            lines = out.split("\n")
            lines = filter(lambda l: l != '', lines)  # remove empty

            self._logger.info('bsub: %s' % ''.join(lines))

            mn_job_id = None
            for line in lines:
                if re.search('Job <.+> is submitted to', line):
                    mn_job_id = re.findall(r'<(.*?)>', line)[0]
                    break

            if not mn_job_id:
                raise Exception("Failed to detect job id after submission.")

            job_id = "[%s]-[%s]" % (self.rm, mn_job_id)

            self._logger.info("Submitted LSF job with id: %s" % job_id)

            # update job dictionary
            self.jobs[job_obj]['job_id'] = job_id
            self.jobs[job_obj]['submitted'] = job_id

            # set status to 'pending' and manually trigger callback
            # self.jobs[job_obj]['state'] = saga.job.PENDING
            # job_obj._api()._attributes_i_set('state', self.jobs[job_obj]['state'], job_obj._api()._UP, True)

            # return the job id
            return job_id

    # ----------------------------------------------------------------
    #
    def _retrieve_job(self, job_id):
        """ see if we can get some info about a job that we don't
            know anything about
        """
        rm, pid = self._adaptor.parse_id(job_id)

        ret, out, _ = self.shell.run_sync(
            "%s -noheader %s" % ('bjobs', pid))

        if ret != 0:
            message = "Couldn't reconnect to job '%s': %s" % (job_id, out)
            log_error_and_raise(message, saga.NoSuccess, self._logger)

        else:
            # the job seems to exist on the backend. let's gather some data
            job_info = {
                'state': saga.job.UNKNOWN,
                'exec_hosts': None,
                'returncode': None,
                'create_time': None,
                'start_time': None,
                'end_time': None,
                'gone': False
            }

            results = out.split()
            job_info['state'] = _mn_to_saga_jobstate(results[2])
            job_info['exec_hosts'] = results[5]
            job_info['create_time'] = results[7]

            return job_info

    # ----------------------------------------------------------------
    #
    def _job_get_info(self, job_obj):
        """ get job attributes via bjob
        """

        # if we don't have the job in our dictionary, we don't want it
        if job_obj not in self.jobs:
            message = "Unknown job object: %s. Can't update state." % job_obj._id
            log_error_and_raise(message, saga.NoSuccess, self._logger)

        # prev. info contains the info collect when _job_get_info
        # was called the last time
        prev_info = self.jobs[job_obj]

        # if the 'gone' flag is set, there's no need to query the job
        # state again. it's gone forever
        if prev_info['gone'] is True:
            return prev_info

        # curr. info will contain the new job info collect. it starts off
        # as a copy of prev_info (don't use deepcopy because there is an API
        # object in the dict -> recursion)
        curr_info = dict()
        curr_info['job_id'] = prev_info.get('job_id')
        curr_info['state'] = prev_info.get('state')
        curr_info['exec_hosts'] = prev_info.get('exec_hosts')
        curr_info['returncode'] = prev_info.get('returncode')
        curr_info['create_time'] = prev_info.get('create_time')
        curr_info['start_time'] = prev_info.get('start_time')
        curr_info['end_time'] = prev_info.get('end_time')
        curr_info['gone'] = prev_info.get('gone')

        rm, pid = self._adaptor.parse_id(job_obj._id)

        # run the LSF 'bjobs' command to get some infos about our job
        # the result of bjobs <id> looks like this:
        #
        # JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
        # 901545  oweidne DONE  regular    yslogin5-ib ys3833-ib   *FILENAME  Nov 11 12:06
        #
        # If we add the -nodeader flag, the first row is ommited

        ret, out, _ = self.shell.run_sync("%s -noheader %s" % ('bjobs', pid))

        if ret != 0:
            if "Illegal job ID" in out or "is not found" in out:
                # Let's see if the previous job state was running or pending. in
                # that case, the job is gone now, which can either mean DONE,
                # or FAILED. the only thing we can do is set it to 'DONE'
                curr_info['gone'] = True
                # we can also set the end time
                self._logger.warning("Previously running job has disappeared." +
                                     "This probably means that the backend doesn't " +
                                     "store informations about finished jobs." +
                                     "Setting state to 'DONE'.")

                if prev_info['state'] in [saga.job.RUNNING, saga.job.PENDING]:
                    curr_info['state'] = saga.job.DONE
                else:
                    curr_info['state'] = saga.job.FAILED
            else:
                # something went wrong
                message = "Error retrieving job info via 'bjobs': %s" % out
                log_error_and_raise(message, saga.NoSuccess, self._logger)
        else:
            # parse the result
            results = out.split()
            curr_info['state'] = _mn_to_saga_jobstate(results[2])
            curr_info['exec_hosts'] = results[5]

        # return the new job info dict
        return curr_info

    # ----------------------------------------------------------------
    #
    def _job_get_state(self, job_obj):
        """ get the job's state
        """
        return self.jobs[job_obj]['state']

    # ----------------------------------------------------------------
    #
    def _job_get_exit_code(self, job_obj):
        """ get the job's exit code
        """
        ret = self.jobs[job_obj]['returncode']

        # FIXME: 'None' should cause an exception
        if ret is None:
            return None
        else:
            return int(ret)

    # ----------------------------------------------------------------
    #
    def _job_get_execution_hosts(self, job_obj):
        """ get the job's exit code
        """
        return self.jobs[job_obj]['exec_hosts']

    # ----------------------------------------------------------------
    #
    def _job_get_create_time(self, job_obj):
        """ get the job's creation time
        """
        return self.jobs[job_obj]['create_time']

    # ----------------------------------------------------------------
    #
    def _job_get_start_time(self, job_obj):
        """ get the job's start time
        """
        return self.jobs[job_obj]['start_time']

    # ----------------------------------------------------------------
    #
    def _job_get_end_time(self, job_obj):
        """ get the job's end time
        """
        return self.jobs[job_obj]['end_time']

    # ----------------------------------------------------------------
    #
    def _job_cancel(self, job_obj):
        """ cancel the job via 'qdel'
        """
        rm, pid = self._adaptor.parse_id(job_obj._id)

        ret, out, _ = self.shell.run_sync("%s %s\n" % ('qdel', pid))

        if ret != 0:
            message = "Error canceling job via 'qdel': %s" % out
            log_error_and_raise(message, saga.NoSuccess, self._logger)

        # assume the job was succesfully canceled
        self.jobs[job_obj]['state'] = saga.job.CANCELED

    # ----------------------------------------------------------------
    #
    def _job_wait(self, job_obj, timeout):
        """ wait for the job to finish or fail
        """
        time_start = time.time()
        time_now = time_start
        self._adaptor.parse_id(job_obj._id)

        while True:
            # state = self._job_get_state(job_id=job_id, job_obj=job_obj)
            state = self.jobs[job_obj]['state']  # this gets updated in the bg.

            if state == saga.job.DONE or \
               state == saga.job.FAILED or \
               state == saga.job.CANCELED:
                return True

            # avoid busy poll
            time.sleep(SYNC_WAIT_UPDATE_INTERVAL)

            # check if we hit timeout
            if timeout >= 0:
                time_now = time.time()
                if time_now - time_start > timeout:
                    return False

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def create_job(self, jd):
        """
        implements saga.adaptors.cpi.job.Service.get_url()

        :param jd: job description
        """
        # this dict is passed on to the job adaptor class -- use it to pass any
        # state information you need there.
        adaptor_state = {"job_service": self,
                         "job_description": jd,
                         "job_schema": self.rm.schema,
                         "reconnect": False
                         }

        # create a new job object
        job_obj = saga.job.Job(_adaptor=self._adaptor,
                               _adaptor_state=adaptor_state)

        # add job to internal list of known jobs.
        self.jobs[job_obj._adaptor] = {
            'state': saga.job.NEW,
            'job_id': None,
            'exec_hosts': None,
            'returncode': None,
            'create_time': None,
            'start_time': None,
            'end_time': None,
            'gone': False,
            'submitted': False
        }

        return job_obj

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_job(self, jobid):
        """
        Implements saga.adaptors.cpi.job.Service.get_job()

        :param jobid: job identifier
        :type jobid: str
        """

        # try to get some information about this job
        job_info = self._retrieve_job(jobid)

        # this dict is passed on to the job adaptor class -- use it to pass any
        # state information you need there.
        adaptor_state = {"job_service": self,
                         # TODO: fill job description
                         "job_description": saga.job.Description(),
                         "job_schema": self.rm.schema,
                         "reconnect": True,
                         "reconnect_jobid": jobid
                         }

        job = saga.job.Job(_adaptor=self._adaptor,
                           _adaptor_state=adaptor_state)

        # throw it into our job dictionary.
        self.jobs[job._adaptor] = job_info
        return job

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_url(self):
        """ implements saga.adaptors.cpi.job.Service.get_url()
        """
        return self.rm

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def list(self):
        """ implements saga.adaptors.cpi.job.Service.list()
        """
        ids = []

        ret, out, _ = self.shell.run_sync("%s -a -noheader" % 'bjobs')

        if ret != 0 and len(out) > 0:
            message = "failed to list jobs via 'bjobs': %s" % out
            log_error_and_raise(message, saga.NoSuccess, self._logger)
        elif ret != 0 and len(out) == 0:

            pass
        else:
            for line in out.split("\n"):
                # output looks like this:
                # 112059.svc.uc.futuregrid testjob oweidner 0 Q batch
                # 112061.svc.uc.futuregrid testjob oweidner 0 Q batch
                if len(line.split()) > 1:
                    jobid = "[%s]-[%s]" % (self.rm, line.split()[0])
                    ids.append(str(jobid))

        return ids

        # # ----------------------------------------------------------------
        # #
        # def container_run (self, jobs) :
        #     self._logger.debug ("container run: %s"  %  str(jobs))
        #     # TODO: this is not optimized yet
        #     for job in jobs:
        #         job.run ()
        #
        #
        # # ----------------------------------------------------------------
        # #
        # def container_wait (self, jobs, mode, timeout) :
        #     self._logger.debug ("container wait: %s"  %  str(jobs))
        #     # TODO: this is not optimized yet
        #     for job in jobs:
        #         job.wait ()
        #
        #
        # # ----------------------------------------------------------------
        # #
        # def container_cancel (self, jobs) :
        #     self._logger.debug ("container cancel: %s"  %  str(jobs))
        #     raise saga.NoSuccess ("Not Implemented");


###############################################################################
#
# noinspection PyMethodOverriding,PyProtectedMember,PyMissingOrEmptyDocstring
class MNJob(saga.adaptors.cpi.job.Job):
    """ implements saga.adaptors.cpi.job.Job
    """

    # noinspection PyMissingConstructor
    def __init__(self, api, adaptor):

        # initialize parent class
        _cpi_base = super(MNJob, self)
        _cpi_base.__init__(api, adaptor)

    def _get_impl(self):
        return self

    @SYNC_CALL
    def init_instance(self, job_info):
        """
        implements saga.adaptors.cpi.job.Job.init_instance()

        :param job_info: job descriptiom
        :type job_info: dict
        """
        # init_instance is called for every new saga.job.Job object
        # that is created
        self.jd = job_info["job_description"]
        self.js = job_info["job_service"]

        if job_info['reconnect'] is True:
            self._id = job_info['reconnect_jobid']
            self._name = self.jd.get(saga.job.NAME)
            self._started = True
        else:
            self._id = None
            self._name = self.jd.get(saga.job.NAME)
            self._started = False

        return self.get_api()

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_state(self):
        """ implements saga.adaptors.cpi.job.Job.get_state()
        """
        return self.js._job_get_state(job_obj=self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def wait(self, timeout):
        """
        implements saga.adaptors.cpi.job.Job.wait()

        :param timeout: time to wait
        :type timeout: int
        """
        if self._started is False:
            log_error_and_raise("Can't wait for job that hasn't been started",
                                saga.IncorrectState, self._logger)
        else:
            self.js._job_wait(job_obj=self, timeout=timeout)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def cancel(self, timeout):
        """
        implements saga.adaptors.cpi.job.Job.cancel()

        :param timeout: time to wait
        :type timeout: int
        """
        if self._started is False:
            log_error_and_raise("Can't wait for job that hasn't been started",
                                saga.IncorrectState, self._logger)
        else:
            self.js._job_cancel(self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def run(self):
        """ implements saga.adaptors.cpi.job.Job.run()
        """
        self._id = self.js._job_run(self)
        self._started = True

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_service_url(self):
        """ implements saga.adaptors.cpi.job.Job.get_service_url()
        """
        return self.js.rm

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_id(self):
        """ implements saga.adaptors.cpi.job.Job.get_id()
        """
        return self._id

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_name (self):
        """ Implements saga.adaptors.cpi.job.Job.get_name() """
        return self._name

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_exit_code(self):
        """ implements saga.adaptors.cpi.job.Job.get_exit_code()
        """
        if self._started is False:
            return None
        else:
            return self.js._job_get_exit_code(self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_created(self):
        """ implements saga.adaptors.cpi.job.Job.get_created()
        """
        if self._started is False:
            return None
        else:
            return self.js._job_get_create_time(self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_started(self):
        """ implements saga.adaptors.cpi.job.Job.get_started()
        """
        if self._started is False:
            return None
        else:
            return self.js._job_get_start_time(self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_finished(self):
        """ implements saga.adaptors.cpi.job.Job.get_finished()
        """
        if self._started is False:
            return None
        else:
            return self.js._job_get_end_time(self)

    # ----------------------------------------------------------------
    #
    @SYNC_CALL
    def get_execution_hosts(self):
        """ implements saga.adaptors.cpi.job.Job.get_execution_hosts()
        """
        if self._started is False:
            return None
        else:
            return self.js._job_get_execution_hosts(self)
