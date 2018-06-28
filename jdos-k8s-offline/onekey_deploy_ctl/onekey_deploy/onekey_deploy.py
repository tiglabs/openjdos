# -*- coding: utf-8 -*-
import os
import re
from utils.ssh_key_copy import ssh_key_copy
from install_rpm.install_rpm import install_rpm
from utils.simple_ansible import simple_ansible
from etcd_cluster.ectd_cluster import etcd_cluster
from conf.configure import configure
from k8s_cluster.k8s_cluster import docker, k8s_cluster_master, k8s_cluster_node
from command.clt import Ctl
from command.commands import *


def config_main(file_path="/etc/onekey_deploy/conf.ini", install_confpath="/etc/onekey_deploy/install.ini"):
    run_mode = 'normal'
    if len(sys.argv) > 2:
        if sys.argv[1] == "-d":
            run_mode = 'debug'

    if (not os.access(file_path, os.F_OK)) or (not os.access(install_confpath, os.F_OK)):
        print 'cofig file not exits'
        sys.exit(0)

    ansible_hosts = '/etc/ansible/hosts'
    conf = configure(file_path)

    (flag, err_str) = conf.check_configure()
    if not flag:
        print err_str
        sys.exit(0)
    # all_host_list={}

    # etcd_ansible = '[etcd_cluster]'
    # for (etcd_host_ip, etcd_host_passwd) in conf.etcd_cluster_list.items():
    #    etcd_ansible = etcd_ansible + '\n' + etcd_host_ip + ' ansible_ssh_user=root ansible_ssh_pass=\'' + etcd_host_passwd + '\''

    # k8s_ansible = '[k8s_cluster]'
    # for (k8s_host_ip, k8s_host_paswd) in conf.k8s__cluster_list.items():
    #    k8s_ansible = k8s_ansible + '\n' + k8s_host_ip + ' ansible_ssh_user=root ansible_ssh_pass=\'' + k8s_host_paswd + '\''
    ##print etcd_ansible k8s_ansible

    ## merge etcd node list and k8s node list
    ##all_host_list = utils.utils.merge_dicts(conf.etcd_list, conf.k8s_list)
    # print all_host_list
    print '--------开始配置ssh 互信--------'
    (flag, err) = ssh_key_copy(conf.all_host_list)
    if not flag:
        try:
            for err_host in err:
                print err_host + "->" + err[err_host]
                del conf.all_host_list[err_host]

                if conf.etcd_cluster.has_key(err_host):
                    del conf.etcd_cluster[err_host]

                if conf.k8s_cluster.has_key(err_host):
                    del conf.k8s_cluster[err_host]
        except:
            pass
    else:
        print "-->ssh-copy-id all right"
    print '------结束配置ssh 互信--------\n'

    # print conf.etcd_list
    # print conf.k8s_list
    # print all_host_list
    hosts_ip = ""
    for host in conf.all_host_list:
        if hosts_ip:
            hosts_ip = hosts_ip + ',' + host
        else:
            hosts_ip = host
    hosts_ip = hosts_ip + ','
    # print hosts

    print '--------开始获取结点主机名--------'
    ###获取所有节点到主机名
    simple_ansible_hostname = simple_ansible('get remote hostname', hosts_ip, 'no', 'shell', 'hostname')
    hosts_info_tmp = simple_ansible_hostname.run()
    # print hosts_info_tmp
    print '--------结束获取结点主机名--------\n'

    ###返回的host 信息是一个list，稍做处理
    all_hosts_map = {}  ## {ip:hostname,....}
    etcd_hosts_map = {}
    k8s_master_hosts_map = {}
    k8s_node_hosts_map = {}
    for (hosts_info, hname) in hosts_info_tmp.items():

        all_hosts_map[hosts_info] = hname[0]

        if conf.etcd_cluster.has_key(hosts_info):
            etcd_hosts_map[hosts_info] = hname[0]

        if conf.k8s_master.has_key(hosts_info):
            k8s_master_hosts_map[hosts_info] = hname[0]

        if conf.k8s_cluster.has_key(hosts_info):
            k8s_node_hosts_map[hosts_info] = hname[0]
    # print hosts_map

    print '--------开始安装集群节点所需要的rpm---------'
    ### 拷贝etcd rpm 到其他主机节点
    host_install_rpm = install_rpm(conf, install_confpath)
    host_install_rpm.copy_and_install()
    print '--------结束安装集群节点所需要的rpm---------\n'

    print '--------开始启动etcd_cluster结点---------'
    for (host_ip, host_hostname) in all_hosts_map.items():
        ## 生成etcd配置文件   /tmp/hostname.conf
        print 'start etcd node:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
        etcd_cluster_node = etcd_cluster(host_ip, host_hostname, "jd_etcd_cluster", all_hosts_map, "normal")
        etcd_cluster_node.update_configfile()
        etcd_cluster_node.copy_configfile_to_host()
        etcd_cluster_node.start_etcd_node()
        print 'start etcd node complete:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
    print '--------完成启动etcd_cluster结点---------'

    ### 后面增加 etcd cluster  状态检出

    print '--------启动k8s_cluster master 结点--------'
    for (host_ip, host_hostname) in k8s_master_hosts_map.items():
        ## 生成etcd配置文件   /tmp/hostname.conf
        print 'start k8s master node:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
        ### docker
        ks8m_docker = docker(host_ip, host_hostname)
        ks8m_docker.update_configfile()
        ks8m_docker.copy_configfile_to_host()
        ks8m_docker.start_docker_node()

        ### k8s master
        ks8m_node = k8s_cluster_master(host_ip, host_hostname, k8s_master_hosts_map)
        ks8m_node.update_configfile()
        ks8m_node.copy_configfile_to_host()
        ks8m_node.start_k8sm_node()
        print 'start k8s master node complete:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
    print '--------启动k8s_cluster master 结点 完成--------'

    print '--------启动k8s_cluster node 结点--------'
    for (host_ip, host_hostname) in k8s_node_hosts_map.items():
        ## 生成etcd配置文件   /tmp/hostname.conf
        print 'start k8s  node:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
        ### docker
        ks8_docker = docker(host_ip, host_hostname)
        ks8_docker.update_configfile()
        ks8_docker.copy_configfile_to_host()
        ks8_docker.start_docker_node()

        ### k8s master
        ks8_node = k8s_cluster_node(host_ip, host_hostname, k8s_master_hosts_map)
        ks8_node.update_configfile()
        ks8_node.copy_configfile_to_host()
        ks8_node.start_k8s_node()
        print 'start k8s  node complete:{hostname:%s, ip:%s}' % (host_hostname, host_ip)
    print '--------启动k8s_cluster node 结点完成--------'
    ### 拷贝自己工程文件到其他主机结点
    # simple_ansible_copy_etcd = simple_ansible('copy python file ', hosts, 'no', 'copy', 'src=/usr/autodeploy/ dest=/usr/autodeploy/ owner=root group=root mode=0777')
    # abc=simple_ansible_copy_etcd.run()

    ## install docker in k8s cluster nodes

    # for host_info in hosts_info:


ctl = Ctl()


def main():
    if "run_config" in sys.argv:
        conf_file_patter = r"^(fc=)"
        install_file_patter = r"^(fi=)"
        conf_file = ""
        install_file = ""
        for arg in sys.argv:
            if re.match(conf_file_patter, arg):
                conf_file = arg.split("=")[-1]
            if re.match(install_file_patter, arg):
                install_file = arg.split("=")[-1]
        if conf_file:
            if install_file:
                config_main(file_path=conf_file, install_confpath=install_file)  ### run with configfile
            else:
                config_main(file_path=conf_file)  ### run with configfile
        else:
            if install_file:
                config_main(install_confpath=install_file)  ### run with configfile
            else:
                config_main()

    else:
        Create_etcd_cluster(ctl)
        Create_k8s_cluster(ctl)
        ctl.run()


if __name__ == '__main__':
    main()
