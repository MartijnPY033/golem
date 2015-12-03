import subprocess
import psutil

from common import is_windows


def exec_cmd(cmd, nice=20, wait=True):
    """ Execute a child process from command in a new process
    :param list|str cmd: sequence of program arguments or a single string. On Unix single string is interpreted
    as the path of the program to execute, but it's only working if not passing arguments to the program.
    :param int nice: *Default: 20 * process priority to bet set (Unix only). For windows lowest priority is always set.
    :param bool wait: *Default: True* if True, program will wait for child process to terminate
    :return:
    """
    pc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pc.communicate()
    if is_windows():
        import win32process
        import win32api
        import win32con
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pc.pid)
        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
    else:
        p = psutil.Process(pc.pid)
        p.nice(nice)

    if wait:
        pc.wait()
