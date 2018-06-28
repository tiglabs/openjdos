# -*- coding:utf-8 -*-
try:
    import json
except ImportError:
    import simplejson as json
import traceback
import datetime


def _dict_to_message(dictory):
    message = json.JSONEncoder(ensure_ascii=False).encode(dictory)
    if type(message) is unicode:
        message = message.encode("utf-8")
    return message


class InvalidMessage(Exception):
    """Logged invalid message."""

    def __init__(self, message):
        """Logged invalid message"""

        # super(InvalidMessage, self).__init__()
        error_message = "Message Type error, message: %s" % message
        # support.message.global_object.MSG_LOG_OBJECT.error(error_message)
        # support.log.log.Log(error_message).error()
        # syslog.syslog(syslog.LOG_ERR, "%s" % error_message)


class Task_Message(object):
    def __init__(self):
        self.environment_type = None
        self.environment_params = None
        self.environment_progress = 0.0
        self.environment_status = None
        self.environment_result = None
        self.environment_desc = None
        self.environment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.environment_err = 0

    def decode(self, message):
        """Decode the mission message object.
        Raise InvalidMessage."""
        if type(message) != dict:
            try:
                # import pdb;pdb.set_trace()
                # message = '''"'''.join(message.split("'"))
                Task_directory = json.JSONDecoder().decode(message)
            except:
                # logger.error('msg err ' + str(traceback.format_exc()))
                raise InvalidMessage(message)
        else:
            Task_directory = message
        if Task_directory.has_key("environment_type") and Task_directory["environment_type"]:
            self.environment_type = Task_directory["environment_type"]

        if Task_directory.has_key("environment_params") and Task_directory["environment_params"]:
            self.environment_params = Task_directory["environment_params"]

        if Task_directory.has_key("environment_progress") and Task_directory["environment_progress"]:
            self.environment_progress = Task_directory["environment_progress"]
        else:
            self.environment_progress = 0.0

        if Task_directory.has_key("environment_status") and Task_directory["environment_status"]:
            self.environment_status = Task_directory["environment_status"]

        if Task_directory.has_key("environment_result"):
            self.environment_result = Task_directory["environment_result"]

        if Task_directory.has_key("environment_desc") and Task_directory["environment_desc"]:
            self.environment_desc = Task_directory["environment_desc"]
        else:
            self.environment_desc = ""

        if Task_directory.has_key("environment_time") and Task_directory["environment_time"]:
            self.environment_time = Task_directory["environment_time"]
        else:
            self.environment_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if Task_directory.has_key("environment_err"):
            self.environment_err = Task_directory["environment_err"]

    def encode(self):
        Task_directory = {}
        Task_directory["environment_type"] = self.environment_type
        Task_directory["environment_params"] = self.environment_params
        Task_directory["environment_progress"] = self.environment_progress
        Task_directory["environment_status"] = self.environment_status
        Task_directory["environment_result"] = self.environment_result
        Task_directory["environment_desc"] = self.environment_desc
        Task_directory["environment_time"] = self.environment_time
        Task_directory["environment_err"] = self.environment_err

        return _dict_to_message(Task_directory)

    def obj_2_json(self):
        return {
            "environment_type": self.environment_type,
            "environment_params": self.environment_params,
            "environment_progress": self.environment_progress,
            "environment_status": self.environment_status,
            "environment_result": self.environment_result,
            "environment_desc": self.environment_desc,
            "environment_time": self.environment_time,
            "environment_err": self.environment_err,
        }
