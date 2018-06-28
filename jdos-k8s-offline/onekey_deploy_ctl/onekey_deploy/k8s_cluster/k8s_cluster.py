# -*- coding: utf-8 -*-

import os
from utils.simple_ansible import simple_ansible


class flannel():

    def __init__(self, flannel_node_ip, flannel_node_name, conf_path='/etc/sysconfig/flanneld', private_key_file=None,
                 etcd_node_list=None, ansible_ssh_user=None, ansible_sudo_pass=None):

        self.flannel_node_ip = flannel_node_ip
        self.flannel_node_name = flannel_node_name
        self.conf_path = conf_path
        self.private_key_file = private_key_file
        self.etcd_node_list = etcd_node_list
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

    def update_configfile(self):
        if not os.access(self.conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_ansible_from_oper_node = simple_ansible('synchronize flannel configure file from remote_node ',
                                                             '%s,' % self.flannel_node_ip, 'no',
                                                             'synchronize',
                                                             'dest=/tmp/flanneld src=/etc/sysconfig/flanneld mode=pull compress=yes',
                                                             private_key_file=self.private_key_file,
                                                             ansible_ssh_user=self.ansible_ssh_user,
                                                             ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_ansible_from_oper_node.run()
            self.conf_path = "/tmp/flanneld"
            # return False, 'The docker conf file not exits..'

        cfg_str = ''

        etcd_servers = ""

        if self.etcd_node_list:
            for etcd_node in self.etcd_node_list:
                if etcd_servers:
                    etcd_servers = etcd_servers + ",http://%s:2379" % etcd_node
                else:
                    etcd_servers = "http://%s:2379" % etcd_node
        if not etcd_servers:
            etcd_servers = "http://127.0.0.1:2379"

        with open(self.conf_path) as confd:
            for line in confd.readlines():
                if 'FLANNEL_ETCD_ENDPOINTS=' in line:
                    cfg_str = cfg_str + '''FLANNEL_ETCD_ENDPOINTS="%s"\n''' % etcd_servers
                else:
                    cfg_str = cfg_str + line

        # print cfg_str
        with open("/tmp/%s.flannel.conf" % self.flannel_node_name, 'w') as nodefd:
            nodefd.write(cfg_str)

    def copy_configfile_to_host(self):

        copy_cfg_ansible = simple_ansible('copy flannel configure file ', '%s,' % self.flannel_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.flannel.conf dest=/etc/sysconfig/flanneld owner=root group=root mode=0777'
                                          % (self.flannel_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

    def start_flannel_node(self):
        start_node_ansible = simple_ansible('start flannel node ', '%s,' % self.flannel_node_ip, 'no', 'shell',
                                            'systemctl enable flanneld && systemctl start flanneld',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

    def restart_flannel_node(self):
        start_node_ansible = simple_ansible('restart flannel node ', '%s,' % self.flannel_node_ip, 'no', 'shell',
                                            'systemctl restart flanneld', private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()


class docker():

    def __init__(self, docker_node_ip, docker_node_name, conf_path='/etc/sysconfig/docker', options=None,
                 private_key_file=None, ansible_ssh_user=None, ansible_sudo_pass=None):
        self.options = options
        self.docker_node_ip = docker_node_ip
        self.conf_path = conf_path
        self.docker_node_name = docker_node_name
        self.private_key_file = private_key_file
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

    def update_configfile(self):
        if not os.access(self.conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_ansible_from_oper_node = simple_ansible('synchronize docker configure file from remote_node ',
                                                             '%s,' % self.docker_node_ip, 'no',
                                                             'synchronize',
                                                             'dest=/tmp/docker src=/etc/sysconfig/docker mode=pull compress=yes',
                                                             private_key_file=self.private_key_file,
                                                             ansible_ssh_user=self.ansible_ssh_user,
                                                             ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_ansible_from_oper_node.run()
            self.conf_path = "/tmp/docker"
            # return False, 'The docker conf file not exits..'

        cfg_str = ''
        with open(self.conf_path) as confd:
            for line in confd.readlines():
                if ('OPTIONS=' in line) and (self.options):
                    cfg_str = cfg_str + '''OPTIONS="%s"\n''' % self.options
                else:
                    cfg_str = cfg_str + line

        # print cfg_str
        with open("/tmp/%s.docker.conf" % self.docker_node_name, 'w') as nodefd:
            nodefd.write(cfg_str)

    def copy_configfile_to_host(self):

        copy_cfg_ansible = simple_ansible('copy docker configure file ', '%s,' % self.docker_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.docker.conf dest=/etc/sysconfig/docker owner=root group=root mode=0777'
                                          % (self.docker_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

    def start_docker_node(self):
        start_node_ansible = simple_ansible('start docker node ', '%s,' % self.docker_node_ip, 'no', 'shell',
                                            'systemctl enable docker && systemctl start docker',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

    def restart_docker_node(self):
        restart_node_ansible = simple_ansible('restart docker node ', '%s,' % self.docker_node_ip, 'no', 'shell',
                                              'systemctl restart docker', private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()


class k8s_cluster_master():

    def __init__(self, ks8m_node_ip, k8sm_node_name, k8sm_list, api_server_conf_path='/etc/kubernetes/apiserver',
                 k8s_conf_path='/etc/kubernetes/config', private_key_file=None, etcd_node_list=None, cni=None,
                 ansible_ssh_user=None, ansible_sudo_pass=None):

        self.ks8m_node_ip = ks8m_node_ip
        self.k8sm_node_name = k8sm_node_name
        self.api_server_conf_path = api_server_conf_path
        self.k8s_conf_path = k8s_conf_path
        self.k8s_master_list = k8sm_list
        self.private_key_file = private_key_file
        self.etcd_node_list = etcd_node_list
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

    def update_configfile(self):
        if not os.access(self.api_server_conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_from_oper_node = simple_ansible('synchronize apiserver configure file from remote_node ',
                                                     '%s,' % self.ks8m_node_ip, 'no',
                                                     'synchronize',
                                                     'dest=/tmp/apiserver src=/etc/kubernetes/apiserver mode=pull compress=yes',
                                                     private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_from_oper_node.run()
            self.api_server_conf_path = "/tmp/apiserver"
            # return False, 'The apiserver conf file not exits..'

        if not os.access(self.k8s_conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_from_oper_node = simple_ansible('synchronize config configure file from remote_node ',
                                                     '%s,' % self.ks8m_node_ip, 'no',
                                                     'synchronize',
                                                     'dest=/tmp/config src=/etc/kubernetes/config mode=pull compress=yes',
                                                     private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_from_oper_node.run()
            self.k8s_conf_path = "/tmp/config"
            # return False, 'The kubernetes conf file not exits..'

        cfg_str_apiserver = ''
        etcd_servers = ""

        if self.etcd_node_list:
            for etcd_node in self.etcd_node_list:
                if etcd_servers:
                    etcd_servers = etcd_servers + ",http://%s:2379" % etcd_node
                else:
                    etcd_servers = "http://%s:2379" % etcd_node
        if not etcd_servers:
            etcd_servers = "http://127.0.0.1:2379"
        with open(self.api_server_conf_path) as confd_apiserver:
            for line in confd_apiserver.readlines():
                if 'KUBE_API_ADDRESS=' in line:
                    cfg_str_apiserver = cfg_str_apiserver + '''KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"\n'''
                elif 'KUBE_API_PORT=' in line:
                    cfg_str_apiserver = cfg_str_apiserver + '''KUBE_API_PORT="--port=8088"\n'''
                elif 'KUBE_ETCD_SERVERS=' in line:
                    cfg_str_apiserver = cfg_str_apiserver + '''KUBE_ETCD_SERVERS="--etcd-servers=%s"\n''' % etcd_servers
                elif 'KUBE_ADMISSION_CONTROL=' in line:
                    cfg_str_apiserver = cfg_str_apiserver + '''UBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"\n'''
                else:
                    cfg_str_apiserver = cfg_str_apiserver + line

        cfg_k8s_conf_path = ''

        KUBE_MASTER_str = ''
        for k8sm in self.k8s_master_list:
            if KUBE_MASTER_str:
                KUBE_MASTER_str = KUBE_MASTER_str + ''',http://%s:8088''' % k8sm
            else:
                KUBE_MASTER_str = '''http://%s:8088''' % k8sm

        with open(self.k8s_conf_path) as confd_k8s_conf_path:
            for line in confd_k8s_conf_path.readlines():
                if 'KUBE_MASTER=' in line:
                    cfg_k8s_conf_path = cfg_k8s_conf_path + '''KUBE_MASTER="--master=''' + KUBE_MASTER_str + '''"\n'''
                else:
                    cfg_k8s_conf_path = cfg_k8s_conf_path + line

        # print cfg_str
        with open("/tmp/%s.api_server.conf" % self.k8sm_node_name, 'w') as node_spi_server_fd:
            node_spi_server_fd.write(cfg_str_apiserver)

        with open("/tmp/%s.k8s.conf" % self.k8sm_node_name, 'w') as node_k8s_fd:
            node_k8s_fd.write(cfg_k8s_conf_path)

    def copy_configfile_to_host(self):

        copy_cfg_ansible = simple_ansible('copy api-server configure file ', '%s,' % self.ks8m_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.api_server.conf dest=/etc/kubernetes/apiserver owner=root group=root mode=0777' %
                                          (self.k8sm_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

        copy_cfg_ansible = simple_ansible('copy k8s configure file ', '%s,' % self.ks8m_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.k8s.conf dest=/etc/kubernetes/config owner=root group=root mode=0777' % (
                                              self.k8sm_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

    def start_k8sm_node(self):
        start_node_ansible = simple_ansible('start api-server node ', '%s,' % self.ks8m_node_ip, 'no', 'shell',
                                            'systemctl enable kube-apiserver.service && systemctl start kube-apiserver.service',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

        start_node_ansible = simple_ansible('start kube-controller-manager node ', '%s,' % self.ks8m_node_ip, 'no',
                                            'shell',
                                            'systemctl enable kube-controller-manager && systemctl start kube-controller-manager',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

        start_node_ansible = simple_ansible('start kube-scheduler node ', '%s,' % self.ks8m_node_ip, 'no', 'shell',
                                            'systemctl enable kube-scheduler && systemctl start kube-scheduler',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

    def restart_k8sm_node(self):
        restart_node_ansible = simple_ansible('restart api-server node ', '%s,' % self.ks8m_node_ip, 'no', 'shell',
                                              'systemctl restart kube-apiserver.service',
                                              private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()

        restart_node_ansible = simple_ansible('restart kube-controller-manager node ', '%s,' % self.ks8m_node_ip, 'no',
                                              'shell',
                                              'systemctl restart kube-controller-manager',
                                              private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()

        restart_node_ansible = simple_ansible('restart kube-scheduler node ', '%s,' % self.ks8m_node_ip, 'no', 'shell',
                                              'systemctl restart kube-scheduler',
                                              private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()


class k8s_cluster_node():

    def __init__(self, ks8_node_ip, k8s_node_name, k8sm_list, kubelet_conf_path='/etc/kubernetes/kubelet',
                 k8s_conf_path='/etc/kubernetes/config', private_key_file=None, cni=None, ansible_ssh_user=None,
                 ansible_sudo_pass=None):

        self.ks8_node_ip = ks8_node_ip
        self.k8s_node_name = k8s_node_name
        self.kubelet_conf_path = kubelet_conf_path
        self.k8s_conf_path = k8s_conf_path
        self.k8s_master_list = k8sm_list
        self.private_key_file = private_key_file
        self.cni = cni
        self.k8s_proxy_conf_path = '/etc/kubernetes/proxy'
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass

    def update_configfile(self):
        if not os.access(self.kubelet_conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_from_oper_node = simple_ansible('synchronize kubelet configure file from remote_node ',
                                                     '%s,' % self.ks8_node_ip, 'no',
                                                     'synchronize',
                                                     'dest=/tmp/kubelet src=/etc/kubernetes/kubelet mode=pull compress=yes',
                                                     private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_from_oper_node.run()
            self.kubelet_conf_path = "/tmp/kubelet"
            # return False, 'The apiserver conf file not exits..'

        if not os.access(self.k8s_conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_from_oper_node = simple_ansible('synchronize config configure file from remote_node ',
                                                     '%s,' % self.ks8_node_ip, 'no',
                                                     'synchronize',
                                                     'dest=/tmp/config src=/etc/kubernetes/config mode=pull compress=yes',
                                                     private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_from_oper_node.run()
            self.k8s_conf_path = "/tmp/config"
            # return False, 'The kubernetes conf file not exits..'

        if not os.access(self.k8s_proxy_conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_from_oper_node = simple_ansible('synchronize proxy configure file from remote_node ',
                                                     '%s,' % self.ks8_node_ip, 'no',
                                                     'synchronize',
                                                     'dest=/tmp/proxy src=/etc/kubernetes/proxy mode=pull compress=yes',
                                                     private_key_file=self.private_key_file,
                                                     ansible_ssh_user=self.ansible_ssh_user,
                                                     ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_from_oper_node.run()
            self.k8s_proxy_conf_path = "/tmp/proxy"
            # return False, 'The kubernetes conf file not exits..'

        KUBE_MASTER_str = ''
        for k8sm in self.k8s_master_list:
            if KUBE_MASTER_str:
                KUBE_MASTER_str = KUBE_MASTER_str + ''',http://%s:8088''' % k8sm
            else:
                KUBE_MASTER_str = '''http://%s:8088''' % k8sm

        cfg_str_kubelet = ''
        with open(self.kubelet_conf_path) as confd_kubelet:
            for line in confd_kubelet.readlines():
                if 'KUBELET_ADDRESS=' in line:
                    cfg_str_kubelet = cfg_str_kubelet + '''KUBELET_ADDRESS="--address=0.0.0.0"\n'''
                elif 'KUBELET_HOSTNAME=' in line:
                    cfg_str_kubelet = cfg_str_kubelet + '''KUBELET_HOSTNAME="--hostname-override=%s"\n''' % self.ks8_node_ip
                elif 'KUBELET_API_SERVER=' in line:
                    cfg_str_kubelet = cfg_str_kubelet + '''KUBELET_API_SERVER="--api-servers=%s"\n''' % KUBE_MASTER_str
                elif 'KUBELET_ARGS=' in line:
                    if self.cni == "calico":
                        cfg_str_kubelet = cfg_str_kubelet + '''KUBELET_ARGS="--network-plugin=cni   --cni-conf-dir=/etc/cni/net.d   --cni-bin-dir=/opt/cni/bin"\n'''
                else:
                    cfg_str_kubelet = cfg_str_kubelet + line
        cfg_k8s_conf_path = ''

        with open(self.k8s_conf_path) as confd_k8s_conf_path:
            for line in confd_k8s_conf_path.readlines():
                if 'KUBE_MASTER=' in line:
                    cfg_k8s_conf_path = cfg_k8s_conf_path + '''KUBE_MASTER="--master=''' + KUBE_MASTER_str + '''"\n'''
                else:
                    cfg_k8s_conf_path = cfg_k8s_conf_path + line

        k8s_proxy_conf = ''
        if self.cni == "calico":
            with open(self.k8s_proxy_conf_path) as k8s_proxy_conf_path:
                for line in k8s_proxy_conf_path.readlines():
                    if 'KUBE_PROXY_ARGS=' in line:
                        k8s_proxy_conf = k8s_proxy_conf + '''KUBE_PROXY_ARGS="--proxy-mode=iptables"\n'''
                    else:
                        k8s_proxy_conf = k8s_proxy_conf + line

            with open("/tmp/%s.proxy" % self.k8s_node_name, 'w') as node_proxy_fd:
                node_proxy_fd.write(k8s_proxy_conf)

        # print cfg_str
        with open("/tmp/%s.kubelet.conf" % self.k8s_node_name, 'w') as node_kubelet_fd:
            node_kubelet_fd.write(cfg_str_kubelet)

        with open("/tmp/%s.k8s.conf" % self.k8s_node_name, 'w') as node_k8s_fd:
            node_k8s_fd.write(cfg_k8s_conf_path)

    def copy_configfile_to_host(self):

        copy_cfg_ansible = simple_ansible('copy kubelet configure file ', '%s,' % self.ks8_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.kubelet.conf dest=/etc/kubernetes/kubelet owner=root group=root mode=0777' %
                                          (self.k8s_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

        copy_cfg_ansible = simple_ansible('copy k8s configure file ', '%s,' % self.ks8_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.k8s.conf dest=/etc/kubernetes/config owner=root group=root mode=0777' % (
                                              self.k8s_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()
        if self.cni == "calico":
            copy_cfg_ansible = simple_ansible('copy k8s proxy file ', '%s,' % self.ks8_node_ip, 'no', 'copy',
                                              'src=/tmp/%s.proxy dest=/etc/kubernetes/proxy owner=root group=root mode=0777' % (
                                                  self.k8s_node_name), private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_ansible.run()

    def start_k8s_node(self):

        start_node_ansible = simple_ansible('start kubelet node ', '%s,' % self.ks8_node_ip, 'no', 'shell',
                                            'systemctl enable kubelet && systemctl start kubelet',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

        start_node_ansible = simple_ansible('start kube-proxy node ', '%s,' % self.ks8_node_ip, 'no', 'shell',
                                            'systemctl enable kube-proxy && systemctl start kube-proxy',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

    def restart_k8s_node(self):

        restart_node_ansible = simple_ansible('restart kubelet node ', '%s,' % self.ks8_node_ip, 'no', 'shell',
                                              'systemctl restart kubelet', private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()

        restart_node_ansible = simple_ansible('restart kube-proxy node ', '%s,' % self.ks8_node_ip, 'no', 'shell',
                                              'systemctl restart kube-proxy', private_key_file=self.private_key_file,
                                              ansible_ssh_user=self.ansible_ssh_user,
                                              ansible_sudo_pass=self.ansible_sudo_pass)
        restart_node_ansible.run()
