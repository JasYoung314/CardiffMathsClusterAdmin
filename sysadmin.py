"""
Script maintain all machines

Usage: sysadmin.py [options] <machines>...
       sysadmin.py [options]

Arguments:
    machines specifies individual machines to run commands on 
Options:
    --update      update all specified machines.
    --upgrade     upgrade all specified machines
    --reboot      reboot all specified machines
    --check_mem   prints free memory to screen across all machines
    --timeout=<tme>  a timeout option so that ssh will move on if machine is blocked [default: 600]
    --file_name=<fle>  which file to pull machines from use [default: sysadmin.yml]
    --install=<pkg>  installs a package across all machines
    --command=<cmd>  runs a generic command across all machines

Examples:

Check the memory on all machines with a timeout of 10 seconds:

    python sysadmin.py --check_mem --timeout=10

When using things that might take longer it is probably worth using a timeout of around 5 minutes:

    python sysadmin.py --check_mem --timeout=300

By default the commands will be run for the machines found in 'sysadmin.yml'. This command will reboot all machines listed in that file:
    
    python sysadmin --reboot

A different admin file can be specified:
    
    python sysadmin.py --reboot --file_name=other_admin_file.yml

Specific machines can be entered as arguments:

    python sysadmin.py --reboot pg11 pg14 
"""

from subprocess import call
from docopt import docopt
from signal import SIGALRM, signal, alarm
import getpass
import yaml

class Alarm(Exception):
    """
    A class for an exception that will kick in if timeout is reached
    """
    pass

def alarm_handler(signum, frame):
    """
    A function to raise an alarm
    """
    raise Alarm

def run_command_with_timeout(cmd, timeout):
    """
    Run a command with a timeout
    """
    signal(SIGALRM, alarm_handler)
    alarm(timeout)
    if timeout:
        try:
            call(['ssh','-t' ,machine, cmd])
            alarm(0)  # reset the alarm
        except Alarm:
            print "Timeout for: %s" % cmd
    else:
        call(['ssh','-t' ,machine, cmd])




arguments = docopt(__doc__)
file_name = arguments['--file_name']
upgrade= arguments['--upgrade']
update = arguments['--update']
reboot = arguments['--reboot']
check_mem = arguments['--check_mem']
install = arguments['--install']
timeout = int(arguments['--timeout'])
machines = arguments['<machines>']
command = arguments['--command']



if not machines:
    fle = open(file_name,'r')
    machines = yaml.load(fle)
    fle.close()
    machines = machines['machines']


if __name__ == '__main__':

    if upgrade or update or install or update:
        password = getpass.getpass()
    for machine in machines:

        print 'Attempting to access %s' %machine

        if update:
            cmd = 'echo %s | sudo -S apt-get update' %(password)
            run_command_with_timeout(cmd, timeout)

        if upgrade:
            cmd = 'echo %s | sudo -S apt-get -y upgrade' %(password)
            run_command_with_timeout(cmd, timeout)

        if install:
            cmd = 'echo %s | sudo -S apt-get -y install %s' %(password,install)
            run_command_with_timeout(cmd, timeout)

        if reboot:
            cmd = 'echo %s | sudo -S reboot' %(password)
            run_command_with_timeout(cmd, timeout)

        if check_mem:
            cmd = ' cat /proc/meminfo | grep MemFree'
            run_command_with_timeout(cmd, timeout)

        if command:
            cmd = command
            run_command_with_timeout(cmd, timeout)
