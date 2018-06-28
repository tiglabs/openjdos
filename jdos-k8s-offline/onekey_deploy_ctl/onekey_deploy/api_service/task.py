# -*- coding:utf-8 -*-
import time, os

from task_message import Task_Message, InvalidMessage
from command.clt import Ctl
from command.commands import *
from utils.utils import checkIP, list_str_2dict
from global_params import sqlite, tasks_run, logger
from k8s_nodes.EC2 import *
import datetime


def create_k8s_cluster(environment_obj, environment_id=None, environment_type=None):
    environment_obj["environment_progress"] = 0.1
    environment_obj["environment_status"] = "running"

    params = environment_obj.get("environment_params")
    # print params
    # time.sleep(25)
    ###ge params
    etcd_install_rpm = params.get("etcd_install_rpm")
    etcd_host_list = params.get("etcd-host-list")
    etcd_cmd = ["create_etcd_cluster", "--host-list"] + etcd_host_list
    if etcd_install_rpm:
        etcd_cmd = etcd_cmd + ["-f"] + etcd_install_rpm

    master_install_rpm = params.get("master_install_rpm")
    node_install_rpm = params.get("node_install_rpm")
    certificate_path = params.get("certificate_path")
    ssh_user = params.get("ssh-user")
    ssh_sudo_pw = params.get("ssh-sudo-pw")

    k8s_cni = params.get("k8s-cni-module", "flannel")
    master_host_list = params.get("master-host-list")
    node_host_list = params.get("node-host-list")
    k8s_cmd = ["create_k8s_cluster", "--master-host-list"] + master_host_list
    if master_install_rpm:
        k8s_cmd = k8s_cmd + ["-fm"] + master_install_rpm

    k8s_cmd = k8s_cmd + ["--node-host-list"] + node_host_list
    if node_install_rpm:
        k8s_cmd = k8s_cmd + ["-fn"] + node_install_rpm

    if certificate_path:
        etcd_cmd = etcd_cmd + ["--ssh-key", certificate_path]
        k8s_cmd = k8s_cmd + ["--ssh-key", certificate_path]
    if ssh_user:
        etcd_cmd = etcd_cmd + ["--ssh-user", ssh_user]
        k8s_cmd = k8s_cmd + ["--ssh-user", ssh_user]
    if ssh_sudo_pw:
        etcd_cmd = etcd_cmd + ["--ssh-sudo-pw", ssh_sudo_pw]
        k8s_cmd = k8s_cmd + ["--ssh-sudo-pw", ssh_sudo_pw]

    k8s_cmd = k8s_cmd + ["--etcd-node-list"] + etcd_host_list
    k8s_cmd = k8s_cmd + ["--k8s-cni-module", k8s_cni]
    environment_obj["environment_progress"] = environment_obj["environment_progress"] + 2
    environment_obj["environment_desc"] = 'start create etcd cluster'
    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ctl = Ctl(etcd_cmd)
    Create_etcd_cluster(ctl)
    ctl.run()
    environment_obj["environment_progress"] = environment_obj["environment_progress"] + 30
    environment_obj["environment_desc"] = "create etcd cluster end, and start create k8s cluster"
    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ctl = Ctl(k8s_cmd)
    Create_k8s_cluster(ctl)
    ctl.run()
    environment_obj["environment_progress"] = 100.0
    environment_obj["environment_desc"] = 'create etcd and k8s cluster complete'
    environment_obj["environment_status"] = "finished"
    environment_obj["environment_result"] = True
    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if environment_id:
        sqlite.update(environment_obj, environment_id)


def get_k8s_status(environment_obj, environment_id=None):
    ip_port = ""
    try:
        # print environment_obj
        master_ip_port = environment_obj.get("environment_params", None)
        if master_ip_port:
            ip_port = master_ip_port.get("master-host-list")[0]
    except:
        pass
    if ip_port:
        try:
            if "@" in ip_port:
                ip = ip_port.split("@")[-1]
            else:
                ip = ip_port
            # (flag, _) = checkIP(ip)
            # if not flag:
            #    return {}
        except:
            return {}
    else:
        ip_port = "127.0.0.1"
    return_dict = {}
    print "1111111111"
    print ip_port
    node_status = os.popen("kubectl -s http://%s:8088 get node" % ip_port).read()
    componentstatus_status = os.popen("kubectl -s http://%s:8088 get componentstatus" % ip_port).read()
    node_status_dict = list_str_2dict(node_status)
    componentstatus_status_dict = list_str_2dict(componentstatus_status)

    # return_str = node_status + componentstatus_status
    return_dict["nodestatus"] = node_status_dict
    return_dict["componentstatus"] = componentstatus_status_dict
    return {
        "environment_type": 3,
        "environment_params": "",
        "environment_progress": 100.0,
        "environment_status": "finished",
        "environment_result": True,
        "environment_desc": return_dict,
        "environment_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "environment_err": 0
    }


def k8s_add_node(environment_obj, environment_id=None, environment_type=None):
    ##environment_obj本次post操作的状态
    environment_obj["environment_progress"] = 0.1
    environment_obj["environment_status"] = "running"

    if environment_id not in tasks_run:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster id:%s not exist" % environment_id
        return

    ###获得创建集群时的参数
    cluster_obj = None
    try:
        cluster_obj = tasks_run[environment_id][1]
    except:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster 111111 not exist"
        environment_obj["environment_err"] = 1
        return

    params = cluster_obj.get("environment_params")
    # time.sleep(25)
    ###ge params
    etcd_install_rpm = params.get("etcd_install_rpm")
    etcd_host_list = params.get("etcd-host-list")
    etcd_cmd = ["create_etcd_cluster", "--host-list"] + etcd_host_list
    if etcd_install_rpm:
        etcd_cmd = etcd_cmd + ["-f"] + etcd_install_rpm
    master_install_rpm = params.get("master_install_rpm")
    node_install_rpm = params.get("node_install_rpm")
    certificate_path = params.get("certificate_path")
    k8s_cni = params.get("k8s-cni-module", "flannel")
    master_host_list = params.get("master-host-list")
    node_host_list = params.get("node-host-list")
    k8s_cmd = ["create_k8s_cluster", "--master-host-list"] + master_host_list
    if master_install_rpm:
        k8s_cmd = k8s_cmd + ["-fm"] + master_install_rpm
    k8s_cmd = k8s_cmd + ["--node-host-list"] + node_host_list
    if node_install_rpm:
        k8s_cmd = k8s_cmd + ["-fn"] + node_install_rpm

    k8s_cmd = k8s_cmd + ["--etcd-node-list"] + etcd_host_list
    k8s_cmd = k8s_cmd + ["--k8s-cni-module", k8s_cni]

    ### 增加节点的参数
    add_params = environment_obj.get("environment_params")
    # print params
    # time.sleep(25)
    ###ge params
    add_etcd_cmd = []
    add_k8s_cmd = []

    add_certificate_path = add_params.get("certificate_path")

    ##  add etcd node 参数
    add_etcd_host_list = add_params.get("etcd-host-list")
    if add_etcd_host_list:
        add_etcd_cmd = ["create_etcd_cluster", "--add-host-list"] + add_etcd_host_list
        if add_certificate_path:
            add_etcd_cmd = add_etcd_cmd + ["--ssh-key", add_certificate_path]
        elif certificate_path:
            add_etcd_cmd = add_etcd_cmd + ["--ssh-key", certificate_path]  ## 使用创建集群时的证书
        add_etcd_cmd = add_etcd_cmd + ["--cluster-oper", "add_nodes"]

    ### add k8s node 参数

    add_master_host_list = add_params.get("master-host-list")
    add_node_host_list = add_params.get("node-host-list")

    if add_master_host_list:
        add_k8s_cmd = ["create_k8s_cluster", "--add-master-host-list"] + add_master_host_list
    if add_node_host_list:
        add_k8s_cmd = add_k8s_cmd + ["--add-node-host-list"] + add_node_host_list

    if add_certificate_path:
        add_k8s_cmd = add_k8s_cmd + ["--ssh-key", add_certificate_path]
    elif certificate_path:
        add_k8s_cmd = add_k8s_cmd + ["--ssh-key", certificate_path]

    if add_etcd_host_list:
        add_k8s_cmd = add_k8s_cmd + ["--etcd-node-list"] + add_etcd_host_list

    add_k8s_cmd = add_k8s_cmd + ["--cluster-oper", "add_nodes"]

    add_k8s_cmd = k8s_cmd + add_k8s_cmd

    ctl = Ctl(add_k8s_cmd)
    Create_k8s_cluster(ctl)
    ctl.run()
    environment_obj["environment_progress"] = 100.0
    environment_obj["environment_desc"] = 'add node to cluster complete'
    environment_obj["environment_status"] = "finished"
    environment_obj["environment_result"] = True
    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    environment_obj["environment_err"] = 0
    # print etcd_cmd
    # print k8s_cmd
    try:
        if add_master_host_list:
            tasks_run[environment_id][1]["environment_params"]["master-host-list"] = list(
                set(tasks_run[environment_id][1]["environment_params"]["master-host-list"] + add_master_host_list))
        if add_node_host_list:
            tasks_run[environment_id][1]["environment_params"]["node-host-list"] = list(
                set(tasks_run[environment_id][1]["environment_params"]["node-host-list"] + add_node_host_list))
        if add_etcd_host_list:
            tasks_run[environment_id][1]["environment_params"]["etcd-host-list"] = list(
                set(tasks_run[environment_id][1]["environment_params"]["etcd-host-list"] + add_etcd_host_list))

        if environment_id:
            sqlite.update(tasks_run[environment_id][1], environment_id)
    except:
        pass


def k8s_del_node(environment_obj, environment_id=None, environment_type=None):
    ##environment_obj本次post操作的状态
    environment_obj["environment_progress"] = 0.1
    environment_obj["environment_status"] = "running"

    if environment_id not in tasks_run:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster id:%s not exist" % environment_id
        environment_obj["environment_err"] = 1
        return

    ###获得创建集群时的参数
    cluster_obj = None
    try:
        cluster_obj = tasks_run[environment_id][1]
    except:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster 111111 not exist"
        environment_obj["environment_err"] = 2
        return

    params = cluster_obj.get("environment_params")
    # time.sleep(25)
    ###ge params
    etcd_install_rpm = params.get("etcd_install_rpm")
    etcd_host_list = params.get("etcd-host-list")
    etcd_cmd = ["create_etcd_cluster", "--host-list"] + etcd_host_list
    if etcd_install_rpm:
        etcd_cmd = etcd_cmd + ["-f"] + etcd_install_rpm
    master_install_rpm = params.get("master_install_rpm")
    node_install_rpm = params.get("node_install_rpm")
    certificate_path = params.get("certificate_path")
    k8s_cni = params.get("k8s-cni-module", "flannel")
    master_host_list = params.get("master-host-list")
    node_host_list = params.get("node-host-list")
    k8s_cmd = ["create_k8s_cluster", "--master-host-list"] + master_host_list
    if master_install_rpm:
        k8s_cmd = k8s_cmd + ["-fm"] + master_install_rpm
    k8s_cmd = k8s_cmd + ["--node-host-list"] + node_host_list
    if node_install_rpm:
        k8s_cmd = k8s_cmd + ["-fn"] + node_install_rpm

    k8s_cmd = k8s_cmd + ["--etcd-node-list"] + etcd_host_list
    k8s_cmd = k8s_cmd + ["--k8s-cni-module", k8s_cni]

    ### 删除节点的参数
    del_params = environment_obj.get("environment_params")
    # print params
    # time.sleep(25)
    ###ge params
    del_etcd_cmd = []
    del_k8s_cmd = []

    del_certificate_path = del_params.get("certificate_path")

    ##  del etcd node 参数
    del_etcd_host_list = del_params.get("etcd-host-list")
    if del_etcd_host_list:
        del_etcd_cmd = ["create_etcd_cluster", "--del-host-list"] + del_etcd_host_list
        if del_certificate_path:
            del_tcd_cmd = del_etcd_cmd + ["--ssh-key", del_certificate_path]
        elif certificate_path:
            del_etcd_cmd = del_etcd_cmd + ["--ssh-key", certificate_path]  ## 使用创建集群时的证书
        del_etcd_cmd = del_etcd_cmd + ["--cluster-oper", "del_nodes"]

    ### add k8s node 参数

    del_master_host_list = del_params.get("master-host-list")
    del_node_host_list = del_params.get("node-host-list")

    if del_master_host_list:
        del_k8s_cmd = ["create_k8s_cluster", "--del-master-host-list"] + del_master_host_list
    if del_node_host_list:
        del_k8s_cmd = del_k8s_cmd + ["--del-node-host-list"] + del_node_host_list

    if del_certificate_path:
        del_k8s_cmd = del_k8s_cmd + ["--ssh-key", del_certificate_path]
    elif certificate_path:
        del_k8s_cmd = del_k8s_cmd + ["--ssh-key", certificate_path]

    if del_etcd_host_list:
        del_k8s_cmd = del_k8s_cmd + ["--etcd-node-list"] + del_etcd_host_list

    del_k8s_cmd = del_k8s_cmd + ["--cluster-oper", "del_nodes"]

    del_k8s_cmd = k8s_cmd + del_k8s_cmd

    print del_k8s_cmd

    ctl = Ctl(del_k8s_cmd)
    Create_k8s_cluster(ctl)
    ctl.run()
    environment_obj["environment_progress"] = 100.0
    environment_obj["environment_desc"] = 'add node to cluster complete'
    environment_obj["environment_status"] = "finished"
    environment_obj["environment_result"] = True
    environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    environment_obj["environment_err"] = 0
    # print etcd_cmd
    # print k8s_cmd
    try:
        if del_master_host_list:
            tasks_run[environment_id][1]["environment_params"]["master-host-list"] = \
                list(set(tasks_run[environment_id][1]["environment_params"]["master-host-list"]) - set(
                    del_master_host_list))
        if del_node_host_list:
            tasks_run[environment_id][1]["environment_params"]["node-host-list"] = \
                list(
                    set(tasks_run[environment_id][1]["environment_params"]["node-host-list"]) - set(del_node_host_list))
        if del_etcd_host_list:
            tasks_run[environment_id][1]["environment_params"]["etcd-host-list"] = \
                list(
                    set(tasks_run[environment_id][1]["environment_params"]["etcd-host-list"]) - set(del_etcd_host_list))

        if environment_id:
            sqlite.update(tasks_run[environment_id][1], environment_id)
    except:
        pass


def create_nodes(environment_obj, environment_id=None, environment_type=None):
    # ec2instances = ec2_instances.create(ImageId='ami-02de0cb5595f2050d', MinCount=1, MaxCount=1, InstanceType='t2.micro',KeyName='My_key', SecurityGroups=['default', ], BlockDeviceMappings=[{'DeviceName': '/dev/sda1','Ebs':{'VolumeType':'standard'}}])
    environment_obj["environment_progress"] = 0.1
    environment_obj["environment_status"] = "running"

    if environment_id not in tasks_run:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster id:%s not exist" % environment_id
        environment_obj["environment_err"] = 1
        return

    params = environment_obj.get("environment_params")
    print params
    node_type = environment_obj.get("node_type", 'EC2')
    if node_type == 'EC2':
        ImageId = params.get("ImageId")  ## aws 模版镜像编号，可从
        MinCount = params.get("MinCount", 1)  ##创建虚拟机的最小个数
        MaxCount = params.get("MaxCount", 1)  ##创建虚拟机的最大个数
        InstanceType = params.get("InstanceType", "t2.micro")  ## 虚拟机类型
        KeyName = params.get("certificate_Name")  ## 创建虚拟机时，用于ssh登陆的 证书（可以自己生成密钥对，上传其中的公钥，aws 创建虚拟机时自动把公钥写入虚拟机的ssh配置中）
        SecurityGroups = [params.get("SecurityGroups", 'default'), ]
        DeviceName = params.get("DeviceName", '/dev/sda1')
        VolumeType = params.get("VolumeType", 'standard')
        BlockDeviceMappings = [{'DeviceName': DeviceName, 'Ebs': {'VolumeType': VolumeType}}]
        environment_obj["environment_progress"] = 10
        environment_obj["environment_status"] = "running"
        try:
            ec2_instances = EC2()
            (new_instances, _) = ec2_instances.create(ImageId=ImageId, MinCount=MinCount, MaxCount=MaxCount,
                                                      InstanceType=InstanceType, KeyName=KeyName,
                                                      SecurityGroups=SecurityGroups,
                                                      BlockDeviceMappings=BlockDeviceMappings)
        except Create_err as e:
            logger.error(e.err_msg)
            environment_obj["environment_progress"] = 100.0
            environment_obj["environment_status"] = "stopped"
            environment_obj["environment_result"] = False
            environment_obj["environment_desc"] = e.err_msg
            environment_obj["environment_err"] = 2
            return
        instances_info = {}
        logger.info("create aws ec2 success,wait The instances running")
        environment_obj["environment_desc"] = "create aws ec2 success,wait The instances running"
        environment_obj["environment_progress"] = 20.0
        for instance in new_instances:
            vm_status = instance.state.get("Name")
            if vm_status == 'pending' or vm_status == 'running':
                instances_info[instance.instance_id] = {}
                instances_info[instance.instance_id]["public_dns_name"] = instance.public_dns_name
                instances_info[instance.instance_id]["public_ip_address"] = instance.public_ip_address
                instances_info[instance.instance_id]["private_dns_name"] = instance.private_dns_name
                instances_info[instance.instance_id]["private_ip_address"] = instance.private_ip_address

                if vm_status == 'pending':  ##                   running->stopping->stopped->pending->running
                    logger.info("waitting %s running" % instance.private_dns_name)
                    environment_obj["environment_desc"] = "waitting %s running" % instance.private_dns_name
                    instance.wait_until_running()  # terminated     虚拟机已经被删除
                    instance.reload()
                    logger.info("%s running,get public dns:%s<=>public ip:%s" % (
                    instance.private_dns_name, instance.public_dns_name, instance.public_ip_address))
                    instances_info[instance.instance_id]["public_dns_name"] = instance.public_dns_name
                    instances_info[instance.instance_id]["public_ip_address"] = instance.public_ip_address

        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_desc"] = instances_info
        environment_obj["environment_status"] = "finished"
        environment_obj["environment_result"] = True
        environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        environment_obj["environment_err"] = 0
    else:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_desc"] = 'node type cannt support'
        environment_obj["environment_status"] = "finished"
        environment_obj["environment_result"] = False
        environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        environment_obj["environment_err"] = 3


def get_nodes_info(environment_obj, environment_id=None):
    environment_obj["environment_progress"] = 0.1
    environment_obj["environment_status"] = "running"

    if environment_id not in tasks_run:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_status"] = "stopped"
        environment_obj["environment_result"] = False
        environment_obj["environment_desc"] = "cluster id:%s not exist" % environment_id
        return

    params = environment_obj.get("environment_params")
    print params
    node_type = environment_obj.get("node_type", 'EC2')
    if node_type == 'EC2':
        InstanceType = params.get("InstanceID")  ## 虚拟机类型
        ec2_instances = EC2()
    else:
        environment_obj["environment_progress"] = 100.0
        environment_obj["environment_desc"] = 'node type cannt support'
        environment_obj["environment_status"] = "finished"
        environment_obj["environment_result"] = False
        environment_obj["environment_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
