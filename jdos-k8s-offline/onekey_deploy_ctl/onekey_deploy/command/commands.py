# -*- coding:utf-8 -*-
import re, time
from clt import *
from utils.utils import *
from utils.ssh_key_copy import *
from utils.simple_ansible import *
from etcd_cluster.ectd_cluster import *
from install_rpm.install_rpm import *
from install_rpm.yum_install import *
from k8s_cluster.k8s_cluster import *
from k8s_cluster.calico import *
from global_params import logger


class Command(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.hide = False
        self.cleanup_routines = []
        self.quiet = False

    def install_argparse_arguments(self, parser):
        pass

    def install_cleanup_routine(self, func):
        self.cleanup_routines.append(func)

    def __call__(self, *args, **kwargs):
        try:
            if not self.quiet:
                logger.info('Start running command [ onekey_deploy_ctl %s ]' % args)
            self.run(*args)
        finally:
            for c in self.cleanup_routines:
                c()

    def run(self, args):
        raise CtlError('the command is not implemented')


class Create_etcd_cluster(Command):
    def __init__(self, Clt):
        super(Create_etcd_cluster, self).__init__()
        self.name = 'create_etcd_cluster'
        self.description = 'Ceate etcd cluster from nodes list'
        self.clt = Clt
        self.host_list_Pattern = '.*:.*@.*'
        Clt.register_command(self)

    def install_argparse_arguments(self, parser):
        parser.add_argument('--host-list', '--hosts', nargs='+',
                            help="All hosts connect info follow below format, example: 'onekey_deploy create_etcd_cluster --hosts root:passwd1@host1_ip root:passwd2@host2_ip ...' ",
                            required=True)
        # parser.add_argument('--force-reinstall', '-f', action="store_true", default=False)
        parser.add_argument('--force-reinstall', '-f', nargs='+',
                            help="All hosts will install rpm, include -f, example:' /home/etcd-3.2.18-1.el7.x86_64.rpm:.....' ")

        parser.add_argument('--ssh-key', nargs='?',
                            help="the path of private key for SSH login $host; if provided, Ansible will use the "
                                 "specified key as private key to SSH login the $host, default will use root private key",
                            default=None)
        ### ssh 登陆用户名
        parser.add_argument('--ssh-user', nargs='?',
                            help="ansible use this user ssh login ",
                            default=None)
        ### ansibel sudo 密码
        parser.add_argument('--ssh-sudo-pw', nargs='?',
                            help="ansible sudo passwd",
                            default=None)

    def run(self, args):
        etcd_hosts_list = {}
        # print args.force_reinstall
        if not args.ssh_key:
            logger.info(
                '''The ssh_key not provided,next ssh login use password,first checkout node_parms is it correct ? eg."root:pw@ip" ''')
            for host in args.host_list:
                try:
                    if not re.match(self.host_list_Pattern, host):
                        logger.error(host + "->arg fromat error!")
                        return False

                    host_ip = host.split("@")[-1]
                    host_passwd = host.split("@")[0].split(":")[-1]
                    flag, _ = checkIP(host_ip)
                    if not flag:
                        logger.error(host + "->ip error!")
                        return False
                    if not host_passwd:
                        logger.error(host + "->password is none!")
                        return False

                    if not etcd_hosts_list.has_key(host_ip):
                        etcd_hosts_list[host_ip] = host_passwd
                    else:  ##
                        if etcd_hosts_list[host_ip] != host_passwd:
                            logger.error(host + "-> password is diff:" + etcd_hosts_list[host_ip] + '=?' + host_passwd)
                            return False
                        else:
                            logger.info(host + "->have same node")
                except:
                    return False

            if len(etcd_hosts_list) < 2:
                ogger.error("etcd cluster at least 2 nodes:%s" % etcd_hosts_list)
                return False

            (flag, err) = ssh_key_copy(etcd_hosts_list)
            if not flag:
                try:
                    for err_host in err:
                        logger.error("copy ssh key to " + err_host + "error:%s" % err[err_host])
                        del etcd_hosts_list[err_host]
                except:
                    pass
                if len(etcd_hosts_list) < 2:
                    logger.error("etcd cluster at least 2 nodes, beacuse some node copy ssh key error")
                    return False
            else:
                logger.info("copy ssh key ok!")
        else:
            for host in args.host_list:
                etcd_hosts_list[host] = ""
            logger.info(
                '''use specified key:%s as private key to SSH login the host,and first check The key''' % args.ssh_key)
            ssh_login(etcd_hosts_list, args.ssh_key)

        logger.info("start create etcd cluster:%s" % etcd_hosts_list)

        hosts_ip = ""
        for host in etcd_hosts_list:
            if hosts_ip:
                hosts_ip = hosts_ip + ',' + host
            else:
                hosts_ip = host
        hosts_ip = hosts_ip + ','

        simple_ansible_hostname = simple_ansible('get remote hostname', hosts_ip, 'no', 'shell', 'hostname',
                                                 private_key_file=args.ssh_key, ansible_ssh_user=args.ssh_user,
                                                 ansible_sudo_pass=args.ssh_sudo_pw)
        hosts_info_tmp = simple_ansible_hostname.run()

        for (hosts_info, hname) in hosts_info_tmp.items():
            etcd_hosts_list[hosts_info] = hname[0]

        if args.force_reinstall:
            logger.info("install etcd rpm from rpm package")
            hosts_rpms = {}
            for host in etcd_hosts_list:
                hosts_rpms[host] = args.force_reinstall
            logger.info("will force install rpm in etcd cluster nodes")
            host_install_rpm = install_rpm(rpm_list=hosts_rpms, private_key_file=args.ssh_key,
                                           ansible_ssh_user=args.ssh_user, ansible_sudo_pass=args.ssh_sudo_pw)
            (flag, str_err) = host_install_rpm.copy_and_install()
            if not flag:
                self.clt.logger.info(str_err)
                return False
        else:  ###yum (yum install etcd)
            logger.info("install etcd rpm from yum")
            yum_etcd = yum_install(hosts_ip, "etcd", private_key_file=args.ssh_key, ansible_ssh_user=args.ssh_user,
                                   ansible_sudo_pass=args.ssh_sudo_pw)
            return_list = yum_etcd.install()
            for failed_host in return_list.get("failed"):
                logger.error("yum install etcd failed:%s" % failed_host)
                if failed_host in etcd_hosts_list:
                    del etcd_hosts_list[failed_host]

        logger.info("start create etcd cluster:%s" % etcd_hosts_list)
        for (host_ip, host_hostname) in etcd_hosts_list.items():
            ## 生成etcd配置文件   /tmp/hostname.conf
            logger.info('start etcd node:{hostname:%s, ip:%s}' % (host_hostname, host_ip))
            etcd_cluster_node = etcd_cluster(host_ip, host_hostname, "jd_etcd_cluster", etcd_hosts_list, "normal",
                                             private_key_file=args.ssh_key, ansible_ssh_user=args.ssh_user,
                                             ansible_sudo_pass=args.ssh_sudo_pw)
            etcd_cluster_node.update_configfile()
            etcd_cluster_node.copy_configfile_to_host()
            etcd_cluster_node.start_etcd_node()
            logger.info('start etcd node complete:{hostname:%s, ip:%s}' % (host_hostname, host_ip))
        logger.info("end create etcd cluster:%s" % etcd_hosts_list)


class Create_k8s_cluster(Command):
    def __init__(self, Clt):
        super(Create_k8s_cluster, self).__init__()
        self.name = 'create_k8s_cluster'
        self.description = 'Ceate k8s cluster from nodes list,include master list and node list'
        self.clt = Clt
        self.list_Pattern = '.*:.*@.*'
        self.need_restart = False  ## 最后是否要重启docker 以及 k8s
        '''matser and node list parttern'''
        Clt.register_command(self)

    def install_argparse_arguments(self, parser):
        ### 创建集群时参数，或者增减节点时 原有集群参数
        parser.add_argument('--master-host-list', '--master-hosts', nargs='+',
                            help="All master hosts connect info follow below format, example: 'onekey_deploy create_ks8_cluster --hosts root:passwd1@host1_ip root:passwd2@host2_ip ...' ",
                            required=True)
        parser.add_argument('--node-host-list', '--node-hosts', nargs='+',
                            help="All master hosts connect info follow below format, example: 'onekey_deploy create_ks8_cluster --hosts root:passwd1@host1_ip root:passwd2@host2_ip ...' ",
                            required=True)
        #### etcd 集群节点
        parser.add_argument('--etcd-node-list', '-enl', nargs='+',
                            help="etcd cluster node list.....' ")
        ### 增加节点
        parser.add_argument('--add-master-host-list', '--add-master-hosts', nargs='+',
                            help="add cluster master node list.....' ")
        parser.add_argument('--add-node-host-list', '--add-node-hosts', nargs='+',
                            help="add cluster node list.....' ")
        ### 删除节点
        parser.add_argument('--del-master-host-list', '--del-master-hosts', nargs='+',
                            help="del cluster master node list.....' ")
        parser.add_argument('--del-node-host-list', '--del-node-hosts', nargs='+',
                            help="del cluster node list.....' ")
        ###  安装本地rpm到目标节点
        parser.add_argument('--force-reinstall-master', '-fm', nargs='+',
                            help="All hosts will install rpm, include -fm, example:' /home/etcd-3.2.18-1.el7.x86_64.rpm:.....' ")
        parser.add_argument('--force-reinstall-node', '-fn', nargs='+',
                            help="All hosts will install rpm, include -fn, example:' /home/etcd-3.2.18-1.el7.x86_64.rpm:.....' ")
        ### 网络模块
        parser.add_argument('--k8s-cni-module', '-cni', nargs='?',
                            help="which cni module select.....' ")
        #### 集群操作，创建、增加节点、删除节点
        parser.add_argument('--cluster-oper', '-cp', nargs='?',
                            help="what oper? create cluser、add node or del node.....' ")
        ### ansible 操作证书
        parser.add_argument('--ssh-key', nargs='?',
                            help="the path of private key for SSH login $host; if provided, Ansible will use the "
                                 "specified key as private key to SSH login the $host, default will use root private key",
                            default=None)

        ### ssh 登陆用户名
        parser.add_argument('--ssh-user', nargs='?',
                            help="ansible use this user ssh login ",
                            default=None)
        ### ansibel sudo 密码
        parser.add_argument('--ssh-sudo-pw', nargs='?',
                            help="ansible sudo passwd",
                            default=None)

    def start_k8s_node(self, host_ip, host_hostname, master_list, etcd_node_list, cni, node_type, ssh_key=None,
                       ansible_ssh_user=None, ansible_sudo_pass=None):
        ## 生成etcd配置文件   /tmp/hostname.conf
        ### docker
        ks8_docker = docker(host_ip, host_hostname, private_key_file=ssh_key)
        ks8_docker.update_configfile()
        ks8_docker.copy_configfile_to_host()
        ks8_docker.start_docker_node()
        if cni == "flannel":
            ks8_flannel = flannel(host_ip, host_hostname, private_key_file=ssh_key, etcd_node_list=etcd_node_list)
            ks8_flannel.update_configfile()
            ks8_flannel.copy_configfile_to_host()
            ks8_flannel.start_flannel_node()
            oper_etcd_node = ''
            try:
                oper_etcd_node = etcd_node_list[0]
            except:
                pass
            if not self.need_restart and oper_etcd_node:
                logger.info(
                    '''etcdctl set /atomic.io/network/config by %s user:%s''' % (oper_etcd_node, ansible_ssh_user))
                flag_set_flannel_ansible = simple_ansible('flag_set_flannel_ansible', '%s,' % oper_etcd_node, 'no',
                                                          'shell',
                                                          '''etcdctl set /atomic.io/network/config '{ "Network": "10.0.0.0/16" }' ''',
                                                          private_key_file=ssh_key, ansible_ssh_user=ansible_ssh_user,
                                                          ansible_sudo_pass=ansible_sudo_pass)
                fannel_result = flag_set_flannel_ansible.run()
                re_str = None
                try:
                    re_str = fannel_result.get(host_ip)[0]
                except:
                    pass
                if (re_str == '''{ "Network": "10.0.0.0/16" }''') or ((re_str) == ''):
                    self.need_restart = True
                    logger.info('''etcdctl set /atomic.io/network/config '{ "Network": "10.0.0.0/16" }'  success''')
                else:
                    logger.error('''etcdctl set /atomic.io/network/config '{ "Network": "10.0.0.0/16" }' error''')
        elif cni == "calico":
            ks8_calico = calico(host_ip, host_hostname, private_key_file=ssh_key, etcd_node_list=etcd_node_list,
                                k8sm_node_list=master_list, ansible_ssh_user=ansible_ssh_user,
                                ansible_sudo_pass=ansible_sudo_pass)
            logger.info("install calico by bin :{hostname:%s, ip:%s}" % (host_hostname, host_ip))
            ks8_calico.install_calico()
            ks8_calico.update_configfile()
            ks8_calico.copy_configfile_to_host()
            logger.info("start calico service :{hostname:%s, ip:%s}" % (host_hostname, host_ip))
            ks8_calico.start_calico_node()

        ### k8s master
        if node_type == 'master':
            ks8m_node = k8s_cluster_master(host_ip, host_hostname, master_list, private_key_file=ssh_key,
                                           etcd_node_list=etcd_node_list, ansible_ssh_user=ansible_ssh_user,
                                           ansible_sudo_pass=ansible_sudo_pass)
            ks8m_node.update_configfile()
            ks8m_node.copy_configfile_to_host()
            ks8m_node.start_k8sm_node()
        else:
            ks8_node = k8s_cluster_node(host_ip, host_hostname, master_list, private_key_file=ssh_key, cni=cni,
                                        ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            ks8_node.update_configfile()
            ks8_node.copy_configfile_to_host()
            ks8_node.start_k8s_node()

    def create_k8s_node(self, k8s_node_list, k8sm_node_list, force_reinstall, node_type='master', ssh_key=None,
                        k8s_cni=None, etcd_node_list=None, ansible_ssh_user=None, ansible_sudo_pass=None):
        node_list = {}
        master_list = {}
        if not k8s_cni:
            cni = "flannel"
        else:
            cni = k8s_cni

        if node_type == 'master':
            log_str = 'k8s cluster master'
        else:
            log_str = 'k8s cluster nodes'

        if not ssh_key:
            ### 使用用户名、密码
            logger.info(
                '''The ssh_key not provided,next ssh login use password,first checkout node_parms is it correct ? eg."root:pw@ip" ''')
            (flag, node_list) = spilt_host_passwd(k8s_node_list)
            if node_type == 'master':
                master_list = node_list
            else:
                (flag, node_list) = spilt_host_passwd(k8sm_node_list)

            (flag, err) = ssh_key_copy(node_list)
            if not flag:
                try:
                    for err_host in err:
                        logger.error("copy ssh key to " + err_host + "error:%s" % err[err_host])
                        del node_list[err_host]
                except:
                    pass

            else:
                logger.info("copy ssh key ok!")
        else:
            logger.info(
                '''use specified key:%s as private key to SSH login the host,and first check The key''' % ssh_key)
            for host in k8s_node_list:
                node_list[host] = ""
            if node_type == 'master':
                master_list = node_list
            else:
                for host in k8sm_node_list:
                    master_list[host] = ""

        logger.info("start %s:%s" % (log_str, node_list))

        ### 1. get hostname from ansible
        hosts_ip = ""
        for host in node_list:
            if hosts_ip:
                hosts_ip = hosts_ip + ',' + host
            else:
                hosts_ip = host
        hosts_ip = hosts_ip + ','
        simple_ansible_hostname = simple_ansible('get remote hostname', hosts_ip, 'no', 'shell', 'hostname',
                                                 private_key_file=ssh_key, ansible_ssh_user=ansible_ssh_user,
                                                 ansible_sudo_pass=ansible_sudo_pass)
        hosts_info_tmp = simple_ansible_hostname.run()
        for (hosts_info, hname) in hosts_info_tmp.items():
            node_list[hosts_info] = hname[0]

        ####2. install rpm package from ansible
        if force_reinstall:  ### copy and rpm *.rpm --force  from ansible
            hosts_rpms = {}
            for host in node_list:
                hosts_rpms[host] = force_reinstall
            logger.info("will force install rpm in " + log_str)
            host_install_rpm = install_rpm(rpm_list=hosts_rpms, private_key_file=ssh_key,
                                           ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            (flag, str_err) = host_install_rpm.copy_and_install()
            if not flag:
                logger.info(str_err)
                return False
        else:  ###yum install from ansible
            ## install docker、kubernet
            logger.info("install kubernetes rpm from yum")
            if cni == "flannel":
                yum_kubernetes = yum_install(hosts_ip, "docker,kubernetes,flannel", private_key_file=ssh_key,
                                             ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            else:
                yum_kubernetes = yum_install(hosts_ip, "docker,kubernetes", private_key_file=ssh_key,
                                             ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            return_list = yum_kubernetes.install()
            for failed_host in return_list.get("failed"):
                logger.error("yum install yum_kubernetes failed :%s" % failed_host)
                if failed_host in node_list:
                    del node_list[failed_host]

        ### 3. create k8s nodes configfile ,and start related service
        logger.info("start create %s:%s" % (log_str, node_list))
        for (host_ip, host_hostname) in node_list.items():
            logger.info('start %s:{hostname:%s, ip:%s}' % (log_str, host_hostname, host_ip))
            self.start_k8s_node(host_ip, host_hostname, master_list, etcd_node_list, cni, node_type, ssh_key,
                                ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            logger.info('start %s complete:{hostname:%s, ip:%s}' % (log_str, host_hostname, host_ip))
        logger.info("end create %s :%s" % (log_str, node_list))

        ####4. need restart some serivces, eg. cni=='flannel'
        if self.need_restart:  ##重启服务
            time.sleep(10)
            for (host_ip, host_hostname) in node_list.items():
                ks8_docker = docker(host_ip, host_hostname, private_key_file=ssh_key, ansible_ssh_user=ansible_ssh_user,
                                    ansible_sudo_pass=ansible_sudo_pass)
                logger.info('restart node:%s docker' % (host_ip))
                ks8_docker.restart_docker_node()
                if node_type == 'master':
                    logger.info('restart k8s master node:%s docker' % (host_ip))
                    ks8m_node = k8s_cluster_master(host_ip, host_hostname, master_list, private_key_file=ssh_key,
                                                   ansible_ssh_user=ansible_ssh_user,
                                                   ansible_sudo_pass=ansible_sudo_pass)
                    ks8m_node.restart_k8sm_node()
                else:
                    logger.info('restart k8s  node:%s docker' % (host_ip))
                    ks8_node = k8s_cluster_node(host_ip, host_hostname, master_list, private_key_file=ssh_key,
                                                ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
                    ks8_node.restart_k8s_node()

    def add_k8s_masters(self, k8s_node_list, k8sm_node_list, force_reinstall, node_type='master', ssh_key=None,
                        k8s_cni=None, etcd_node_list=None, add_master_list=None):
        pass

    def del_k8s_masters(self, k8s_node_list, k8sm_node_list, force_reinstall, node_type='master', ssh_key=None,
                        k8s_cni=None, etcd_node_list=None, del_master_list=None):

        pass

    def add_k8s_nodes(self, add_k8s_node_list, k8sm_node_list, force_reinstall, ssh_key=None,
                      k8s_cni=None, etcd_node_list=None, ansible_ssh_user=None, ansible_sudo_pass=None):
        node_list = {}
        hosts_ip = ""
        if not k8s_cni:
            cni = "flannel"
        else:
            cni = k8s_cni
        for host in add_k8s_node_list:
            if hosts_ip:
                hosts_ip = hosts_ip + ',' + host
            else:
                hosts_ip = host
        hosts_ip = hosts_ip + ','

        simple_ansible_hostname = simple_ansible('get remote hostname', hosts_ip, 'no', 'shell', 'hostname',
                                                 private_key_file=ssh_key, ansible_ssh_user=ansible_ssh_user,
                                                 ansible_sudo_pass=ansible_sudo_pass)
        hosts_info_tmp = simple_ansible_hostname.run()
        for (hosts_info, hname) in hosts_info_tmp.items():
            node_list[hosts_info] = hname[0]

        if force_reinstall:
            hosts_rpms = {}
            for host in node_list:
                hosts_rpms[host] = force_reinstall
            logger.info("will force install rpm in " + log_str)
            host_install_rpm = install_rpm(rpm_list=hosts_rpms, private_key_file=ssh_key,
                                           ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            (flag, str_err) = host_install_rpm.copy_and_install()
            if not flag:
                logger.info(str_err)
                return False
        else:  ###yum (yum install docker)
            ## install docker、kubernet
            logger.info("install kubernetes rpm from yum")
            if cni == "flannel":
                yum_kubernetes = yum_install(hosts_ip, "docker,kubernetes,flannel", private_key_file=ssh_key,
                                             ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            else:
                yum_kubernetes = yum_install(hosts_ip, "docker,kubernetes", private_key_file=ssh_key,
                                             ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            return_list = yum_kubernetes.install()
            for failed_host in return_list.get("failed"):
                logger.error("yum install yum_kubernetes failed :%s" % failed_host)
                if failed_host in node_list:
                    del node_list[failed_host]

        logger.info("start add node %s" % (node_list))
        ### 3. create k8s nodes configfile ,and start related service
        logger.info("start add  node to cluster %s" % (node_list))
        for (host_ip, host_hostname) in node_list.items():
            logger.info('start :{hostname:%s, ip:%s}' % (host_hostname, host_ip))
            self.start_k8s_node(host_ip, host_hostname, k8sm_node_list, etcd_node_list, cni, 'node', ssh_key,
                                ansible_ssh_user=ansible_ssh_user, ansible_sudo_pass=ansible_sudo_pass)
            logger.info('start  complete:{hostname:%s, ip:%s}' % (host_hostname, host_ip))
        logger.info("end  add  node to cluster %s" % (node_list))

    def del_k8s_nodes(self, del_k8s_node_list, k8sm_node_list, ssh_key=None, ansible_ssh_user=None,
                      ansible_sudo_pass=None):
        logger.info("start del  node to cluster %s" % (del_k8s_node_list))
        if not k8sm_node_list:
            return
        else:
            k8sm = k8sm_node_list[0]
        for node in del_k8s_node_list:
            # print "kubectl -s http://%s:8088 delete node %s " % ( k8sm, node)
            node_status = os.popen("kubectl -s http://%s:8088 delete node %s " % (k8sm, node)).read()
        logger.info("end del  node to cluster %s" % (del_k8s_node_list))

    def run(self, args):
        cluster_oper = args.cluster_oper

        if (not cluster_oper) or ('create' == cluster_oper):  ##默认创建集群
            ###应先创建master
            self.create_k8s_node(args.master_host_list, args.master_host_list, args.force_reinstall_master, 'master',
                                 ssh_key=args.ssh_key, k8s_cni=args.k8s_cni_module, etcd_node_list=args.etcd_node_list,
                                 ansible_ssh_user=args.ssh_user, ansible_sudo_pass=args.ssh_sudo_pw)
            self.create_k8s_node(args.node_host_list, args.master_host_list, args.force_reinstall_node, 'node',
                                 ssh_key=args.ssh_key, k8s_cni=args.k8s_cni_module, etcd_node_list=args.etcd_node_list,
                                 ansible_ssh_user=args.ssh_user, ansible_sudo_pass=args.ssh_sudo_pw)
            logger.info('create k8s cluster success')
        elif 'add_nodes' == cluster_oper:
            self.add_k8s_nodes(args.add_node_host_list, args.master_host_list, args.force_reinstall_node,
                               ssh_key=args.ssh_key, k8s_cni=args.k8s_cni_module, etcd_node_list=args.etcd_node_list,
                               ansible_ssh_user=args.ssh_user, ansible_sudo_pass=args.ssh_sudo_pw)
            logger.info('add nodes  k8s cluster success')

        elif 'del_nodes' == cluster_oper:
            self.del_k8s_nodes(args.del_node_host_list, args.master_host_list, ssh_key=args.ssh_key,
                               ansible_ssh_user=args.ssh_user, ansible_sudo_pass=args.ssh_sudo_pw)
            logger.info('del nodes  k8s cluster success')

        # import pdb;pdb.set_trace()
        # print args.force_reinstall
