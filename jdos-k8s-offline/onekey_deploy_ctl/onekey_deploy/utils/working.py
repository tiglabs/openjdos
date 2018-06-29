# -*- coding: utf-8 -*-

import time
import threading
import thread
import syslog
import traceback
import sys
import global_params
from global_params import logger


class InvalidFun(Exception):
    """Logged invalid message."""

    def __init__(self, message):
        """Logged invalid message"""

        # super(InvalidMessage, self).__init__()
        error_message = "Thread fun:%s not fount" % message
        # support.message.global_object.MSG_LOG_OBJECT.error(error_message)
        # support.log.log.Log(error_message).error()
        # syslog.syslog(syslog.LOG_ERR, "%s" % error_message)


class Vmdworker(threading.Thread):

    def __init__(self, threadname, func, args):

        self.func = func
        self.param = args
        self.cancel = "no"
        self.threadname = threadname
        threading.Thread.__init__(self)

    def cancelyes(self):
        self.cancel = "yes"

    #    def cancelno(self):
    #        self.cancel = "no"

    def checkcancel(self):
        return self.cancel

    def run(self):
        strs = ""
        num = len(self.param)

        for i in range(0, num):
            strs += "self.param[%d]" % i
            if i == num - 1:
                pass  # do nothing
            else:
                strs += ","
        try:
            eval("self.func(%s)" % strs)
        except:
            logger.error("thread_erro:" + str(sys.exc_info()))
            logger.error("thread_erro:" + traceback.format_exc())
            raise InvalidFun(self.threadname)
        finally:
            global_params.lock_acquire("thread_list_lock")
            try:
                del global_params.thread_list[self.threadname]
            except:
                pass
            global_params.lock_release("thread_list_lock")


def addtosubthread(threadname, func, *args):  # support compound

    worker = Vmdworker(threadname, func, args)
    if worker == None:
        return False
    worker.setDaemon(True)
    while True:
        try:
            worker.start()
        except thread.error:
            logger.error(str(sys.exc_info()))
            logger.error(traceback.format_exc())
            time.sleep(5)
        else:
            break
    global_params.lock_acquire("thread_list_lock")
    try:
        if worker.isAlive():
            thdes = {}
            thdes["threadobject"] = worker
            thdes["threadstepmeasure"] = 0
            global_params.thread_list[threadname] = thdes
    except:
        print "addtosubthread error"
    global_params.lock_release("thread_list_lock")
    time.sleep(0.1)
