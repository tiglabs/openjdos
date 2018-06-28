# -*- coding:utf-8 -*-
import threading
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.simple_sqlite import *

del_task_timeout = 60  ## task完成，且通过get查询过后，60s 删除改task
# 任务队列
tasks_run = {}
tasks_time = {}  ##
locklist = {
    "thread_list_lock": "", }

thread_list = {}


def init_threadlock():
    global locklist
    for x in locklist:
        locklist[x] = threading.Lock()
    return True


def lock_acquire(lockname):
    return locklist[lockname].acquire()


def lock_release(lockname):
    return locklist[lockname].release()


LOGGER_DIR = "/var/log/onekey_deploy/"
LOGGER_FILE = "onekey_deploy.log"
logger = logging.getLogger("onekey_deploy_Log")


def create_log(logger_dir, logger_file):
    if not os.path.exists(logger_dir):
        os.makedirs(logger_dir)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.handlers.RotatingFileHandler(logger_dir + '/' + logger_file, maxBytes=10 * 1024 * 1024,
                                                   backupCount=30)
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)


create_log(LOGGER_DIR, LOGGER_FILE)  ##创建日志

sqlite = None
try:
    sqlite = cluster_sqlplite3()
except:
    logger.error("init sqlite3 error")
else:
    logger.info("init sqlite3 success")


def warn(msg):
    sys.stdout.write(colored('WARNING: %s\n' % msg, 'yellow'))


def error(msg):
    sys.stderr.write(colored('ERROR: %s\n' % msg, 'red'))
    sys.exit(1)


def error_not_exit(msg):
    sys.stderr.write(colored('ERROR: %s\n' % msg, 'red'))


def info(*msg):
    if len(msg) == 1:
        out = '%s\n' % ''.join(msg)
    else:
        out = ''.join(msg)
    now = datetime.now()
    out = "%s " % str(now) + out
    sys.stdout.write(out)


services_map = {
    1: "create_k8s_cluster",  ### create k8s clusert
    2: "get_k8s_status",  ### get cluster status
    3: "k8s_add_node",  ### add  nodes to exist k8s cluster
    4: "k8s_del_node",  ### del  nodes from exist k8s cluster
    5: "create_nodes",  ### create machines ,support aws ec2
    6: "get_nodes_info"  ##
}
