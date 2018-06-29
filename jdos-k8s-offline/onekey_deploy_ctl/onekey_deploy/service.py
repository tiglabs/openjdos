# -*- coding: utf-8 -*-
import sys, os, json, time
import api_service.task
import global_params
from api_service.task_message import Task_Message, InvalidMessage
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from global_params import tasks_run, tasks_time, del_task_timeout, logger, services_map, sqlite
from utils.working import addtosubthread, InvalidFun
import datetime

app = Flask(__name__)
api = Api(app)


# 任务队列
# tasks_run = {}

# @app.route('/post_task/', methods=['POST'])
# def post_task_dispath():
#     if not request.json or 'id' not in request.json or 'info' not in request.json:
#         abort(400)
#     task = {
#         'id': request.json['id'],
#         'info': request.json['info']
#     }
#     tasks.append(task)
#     return jsonify({'result': 'success'})
#
# @app.route('/get_task/', methods=['GET'])
# def get_task_dispath():
#     print request.args
#     if not request.json or 'id' not in request.json :
#         return jsonify(tasks)
#     else:
#         task_id = request.args['id']
#         task = filter(lambda t: t['id'] == int(task_id), tasks)
#         return jsonify(task) if task else jsonify({'result':"not found"})


def dispath_main(environment_id=None, environment_type=None):
    environment_obj = None
    try:
        environment_obj = tasks_run[environment_id][environment_type]
    except:
        pass
    if (not environment_obj) or (not environment_id) or (not environment_type):
        return

    service_fun = services_map[environment_type]
    thread_name = environment_id + service_fun
    while True:
        environment_progress = environment_obj.get("environment_progress", 0.0)
        if environment_progress == 100.0:
            return

        if True:  # task_uuid not in tasks_time:
            if (thread_name not in global_params.thread_list) and (environment_progress == 0.0):
                try:

                    addtosubthread(thread_name, eval("api_service.task.%s" % service_fun), environment_obj,
                                   environment_id, environment_type)
                except:
                    environment_obj["environment_desc"] = "task tread error"
                    environment_obj["environment_progress"] = 100.0
                    environment_obj["environment_result"] = False
                    environment_obj["environment_status"] = "stoped"
                    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if environment_id == 1:
                        sqlite.insert(environment_obj, environment_id)
                    return
            else:  ###更新进度,这里不知道具体的执行线程执行进度
                if environment_obj["environment_status"] == "running":
                    environment_obj["environment_progress"] = environment_progress + (
                            100.0 - environment_progress) / 100.0
                    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            if tasks_time[environment_id] <= 0.0:
                ####查询过后 1min  删除task的信息
                del tasks_time[environment_id]
                del tasks_run[environment_id]
            else:
                tasks_time[environment_id] = tasks_time[environment_id] - 2
        time.sleep(2)


def abort_if_no_task(environment_id):
    if environment_id not in tasks_run:
        abort(404, messsage="environment {} doesn't exist".format(environment_id))


def abort_if_onsupport_task(environment_type):
    service_id = None
    try:
        service_id = int(environment_type)
    except:
        pass
    # print service_id
    if service_id and (not services_map.has_key(service_id)):
        abort(404, messsage="service doesn't support this action:{}".format(service_id))
    return service_id


# parser = reqparse.RequestParser()
# parser.add_argument("task")

class post_tasks(Resource):
    def __init__(self):
        self.message_object = Task_Message()

    # def get(self, task_uuid):
    #     abort_if_no_task(task_uuid)
    #     if tasks_run[task_uuid].get("task_progress",0.0) ==100.0 and tasks_run[task_uuid].get("task_status") != "running":
    #         tasks_time[task_uuid] = del_task_timeout   ###  初始化定时器
    #     return tasks_run[task_uuid]
    #
    # def delete(self,task_uuid):
    #     abort_if_no_task(task_uuid)
    #     del tasks_run[task_uuid]
    #     return '', 204

    def post(self, environment_id):
        task_param_err = ''
        # args = parser.parse_args()
        # Task_info = args.get('task')

        environment_info = request.json
        environment_param_err = ''
        try:
            self.message_object.decode(environment_info)
        except InvalidMessage:
            environment_param_err = 'environment info is Invalid'
        else:
            environment_type = self.message_object.environment_type
            abort_if_onsupport_task(environment_type)
            if (environment_id in tasks_run) and (environment_type in tasks_run[environment_id]) and (
                    tasks_run[environment_id][environment_type].get("environment_progress", 0.0) < 100.0):
                environment_param_err = 'environment is already running'

        if environment_param_err:
            return (
                           '''{"environment_name": "%s", "environment_result":"False", "environment_desc":"environment_params_err:%s"}''' % (
                       self.message_object.environment_type, environment_param_err)), 201

        message_dict = self.message_object.obj_2_json()
        if (environment_id in tasks_run):  ### 集群已存在
            if (environment_type in tasks_run[environment_id]):  ### 对集群的操作过（新建或添加或节点）再次运行该 任务
                for (task_pa, task_val) in message_dict.items():
                    if task_val:
                        tasks_run[environment_id][environment_type][task_pa] = task_val
                        tasks_run[environment_id][environment_type]["environment_progress"] = 0.0
                        tasks_run[environment_id][environment_type]["environment_result"] = None
                        tasks_run[environment_id][environment_type]["environment_status"] = "running"
                        tasks_run[environment_id][environment_type][
                            "environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:  ### 对集群  新的操作（新加节点？）
                tasks_run[environment_id][environment_type] = message_dict
        else:  ### 集群不存在
            tasks_run[environment_id] = {}
            if environment_type == 1:  ##新建集群才会写入数据库
                sqlite.insert(self.message_object, environment_id)
            tasks_run[environment_id][environment_type] = message_dict

        # if ("dispath_main" not in global_params.thread_list):
        #    addtosubthread("dispath_main", dispath_main, 5)
        addtosubthread("dispath_main_%s_%d" % (environment_id, environment_type), dispath_main, environment_id,
                       environment_type)
        return self.message_object.obj_2_json(), 201


class get_tasks(Resource):
    def __init__(self):
        self.message_object = Task_Message()

    def get(self, environment_id, environment_type):
        abort_if_no_task(environment_id)
        environment_type_int = abort_if_onsupport_task(environment_type)
        environment_type = int(environment_type)
        if tasks_run[environment_id].get("environment_progress", 0.0) == 100.0 and tasks_run[environment_id].get(
                "environment_status") != "running":
            tasks_time[environment_id] = del_task_timeout  ###  初始化定时器
        services_fun = services_map[int(environment_type)]
        if "get" in services_fun:
            return eval("api_service.task.%s" % services_fun)(tasks_run[environment_id][1])

        return tasks_run[environment_id][environment_type_int]  ###此处任务是前面post过来的任务，对这些任务的状态本身查询


class get_alltasks(Resource):
    def __init__(self):
        pass

    def get(self):
        return tasks_run  ###此处任务是前面post过来的任务，对这些任务的本身查询


api.add_resource(get_alltasks, '/environments')
api.add_resource(post_tasks, '/environments/<environment_id>')
api.add_resource(get_tasks, '/environments/<environment_id>/<environment_type>')


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # Perform first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    # os.chdir("/usr/vmd")
    os.umask(0)
    os.setsid()
    # Perform second fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %sn" % (e.errno, e.strerror))
        sys.exit(1)

    # e.g for /sbin/cryptsetup
    # The process is now daemonized, redirect standard file descriptors.
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


if __name__ == '__main__':
    logger.info("start onekey_deploy service ....")
    no_fork = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-d":
            no_fork = True
    if not no_fork:
        daemonize()
    if sqlite:
        logger.info("init environment from splite3")
        environments = sqlite.select()
        for environment in environments:
            environment_id = environment[0]
            environment_type = environment[1]
            tasks_run[environment_id] = {}
            tasks_run[environment_id][1] = {}
            tasks_run[environment_id][1]["environment_type"] = environment[1]
            tasks_run[environment_id][1]["environment_params"] = eval(environment[2])
            tasks_run[environment_id][1]["environment_progress"] = 100.0
            tasks_run[environment_id][1]["environment_status"] = "finished"
            tasks_run[environment_id][1]["environment_result"] = True
            tasks_run[environment_id][1]["environment_desc"] = environment[6]
            tasks_run[environment_id][1]["environment_time"] = environment[7]
            tasks_run[environment_id][1]["environment_err"] = environment[8]

    pid_file = "/var/run/onekey_deploy.pid"
    file(pid_file, "w").write(str(os.getpid()))

    global_params.init_threadlock()
    app.run(host='0.0.0.0', port=8383, debug=False)
