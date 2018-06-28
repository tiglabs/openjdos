# -*- coding: utf-8 -*-

import re


def checkIP(ip):
    if not ip:
        return (False, "不能为空")
    ipv4Pattern = r"^(25[0-5]|2[0-4][0-9]|[1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[1]?[0-9][0-9]?)$"
    if not re.match(ipv4Pattern, ip):
        return (False, "格式错误")
    return (True, "")


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def split_str(in_str):
    if ('{' not in in_str) and ('(' not in in_str) and ('[' not in in_str):
        return in_str.split()
    str_list = []
    start_index = 0
    complete_str = 0
    spit_str = False
    for index, char_i in enumerate(in_str):
        if char_i == '{':
            complete_str = complete_str + 1
        if char_i == '}':
            complete_str = complete_str - 1
            if complete_str == 0:
                spit_str = True
        if in_str[start_index] == ' ':
            start_index = start_index + 1
            continue
        if char_i != ' ':
            if index == len(in_str) - 1:
                str_list.append(in_str[start_index:index + 1])
            continue
        if complete_str == 0:
            str_list.append(in_str[start_index:index])
            if spit_str:
                start_index = index + 1
            else:
                start_index = index
            spit_str = False
    return str_list


def list_str_2dict(input_str):
    # input  str  or list
    '''str split with '\n' '''
    '''
    NAME      STATUS    AGE
    k8s0      Ready     1h
    k8s1      Ready     1h
    k8s2      Ready     1h
    '''
    # output
    '''
    {
       "k8s0":{
           "STATUS":"Ready" ,
           "AGE":"1h"
        },
        "k8s1":{
           "STATUS":"Ready" ,
           "AGE":"1h"
        },
        "k8s2":{
           "STATUS":"Ready" ,
           "AGE":"1h"
        },
    }
    '''
    out_dict = {}
    if type(input_str) == str:
        input_list = input_str.split('\n')
    else:
        input_list = input_str

    # for input_line in input_list:
    input_params_name = []
    for index, input_line in enumerate(input_list):
        if not input_line:
            continue

        if index == 0:
            input_params_name = split_str(input_line)  # input_line.split()
            continue
        else:
            input_params = split_str(input_line)  # input_line.split()

        tmp_dick = {}
        for index_tmp, parma in enumerate(input_params):
            if index_tmp == 0:
                continue
            if index_tmp >= len(input_params_name):
                continue
            tmp_dick[input_params_name[index_tmp]] = parma
        out_dict[input_params[0]] = tmp_dick
    return out_dict


def spilt_host_passwd(node_list_info):
    node_list = {}
    for host in node_list_info:
        try:
            if not re.match(self.list_Pattern, host):
                return False, (host + "->arg fromat error!")

            host_ip = host.split("@")[-1]
            host_passwd = host.split("@")[0].split(":")[-1]
            flag, _ = checkIP(host_ip)
            if not flag:
                return False, (host + "->ip error!")
            if not host_passwd:
                return False, (host + "->password is none!")

            if not node_list.has_key(host_ip):
                node_list[host_ip] = host_passwd
            else:  ##
                if node_list[host_ip] != host_passwd:
                    return False, (host + "-> password is diff:" + node_list[host_ip] + '=?' + host_passwd)
        except:
            return False
    return True, node_list
