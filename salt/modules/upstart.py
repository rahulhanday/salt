'''
Module for the management of upstart systems. The Upstart system only supports
service starting, stopping and restarting.

DO NOT use this module on red hat systems, as red hat systems should use the
rh_service module, since red hat systems support chkconfig
'''

import os
import re
from salt import utils


def __virtual__():
    '''
    Only work on Ubuntu
    '''
    # Disable on these platforms, specific service modules exist:
    if __grains__['os'] == 'Ubuntu':
        return 'service'
    return False


def _runlevel():
    '''
    Return the current runlevel
    '''
    out = __salt__['cmd.run']('runlevel').strip()
    return out.split()[1]


def start(name):
    '''
    Start the specified service

    CLI Example::

        salt '*' service.start <service name>
    '''
    cmd = 'service {0} start'.format(name)
    return not __salt__['cmd.retcode'](cmd)


def stop(name):
    '''
    Stop the specified service

    CLI Example::

        salt '*' service.stop <service name>
    '''
    cmd = 'service {0} stop'.format(name)
    return not __salt__['cmd.retcode'](cmd)


def restart(name):
    '''
    Restart the named service

    CLI Example::

        salt '*' service.restart <service name>
    '''
    cmd = 'service {0} restart'.format(name)
    return not __salt__['cmd.retcode'](cmd)


def status(name, sig=None):
    '''
    Return the status for a service, returns a bool whether the service is
    running.

    CLI Example::

        salt '*' service.status <service name>
    '''
    cmd = 'service {0} status'.format(name)
    return 'start/running' in __salt__['cmd.run'](cmd)


def _get_service_exec():
    executable = 'update-rc.d'
    utils.check_or_die(executable)
    return executable


def enable(name):
    '''
    Enable the named service to start at boot

    CLI Example::

        salt '*' service.enable <service name>
    '''
    executable = _get_service_exec()
    cmd = '{0} -n -f {1} defaults'.format(executable, name)
    return not __salt__['cmd.retcode'](cmd)


def disable(name):
    '''
    Disable the named service from starting on boot

    CLI Example::

        salt '*' service.disable <service name>
    '''
    executable = _get_service_exec()
    cmd = '{0} -n -f {1} defaults'.format(executable, name)
    return not __salt__['cmd.retcode'](cmd)
