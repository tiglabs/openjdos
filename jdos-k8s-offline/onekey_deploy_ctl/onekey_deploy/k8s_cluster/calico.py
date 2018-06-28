# -*- coding: utf-8 -*-

import os
from utils.simple_ansible import simple_ansible


class calico():

    def __init__(self, calico_node_ip, calico_node_name, conf_path='/etc/sysconfig/calico-node', private_key_file=None,
                 etcd_node_list=None, k8sm_node_list=None, calico_ver='v2.5.1', ssh_user=None, sudo_passwd=None):

        self.calico_node_ip = calico_node_ip
        self.calico_node_name = calico_node_name
        self.conf_path = conf_path
        self.private_key_file = private_key_file
        self.etcd_node_list = etcd_node_list
        self.k8sm_node_list = k8sm_node_list
        self.calico_ver = calico_ver
        self.ssh_user = ssh_user
        self.sudo_passwd = sudo_passwd

        if not os.access("/tmp/%s" % calico_node_name, os.F_OK):
            os.system("mkdir -p /tmp/%s" % calico_node_name)

    def update_configfile(self):

        etcd_servers = ""
        if self.etcd_node_list:
            for etcd_node in self.etcd_node_list:
                if etcd_servers:
                    etcd_servers = etcd_servers + ",http://%s:2379" % etcd_node
                else:
                    etcd_servers = "http://%s:2379" % etcd_node
        if not etcd_servers:
            etcd_servers = "http://127.0.0.1:2379"

        ks8_apiservers = ""
        if self.k8sm_node_list:
            for k8sm_node in self.k8sm_node_list:
                if ks8_apiservers:
                    ks8_apiservers = ks8_apiservers + ",http://%s:8088" % k8sm_node
                else:
                    ks8_apiservers = "http://%s:8088" % k8sm_node
        if not ks8_apiservers:
            ks8_apiservers = "http://127.0.0.1:8088"

        ETCD_ENDPOINTS = '''ETCD_ENDPOINTS="%s"\n''' % etcd_servers
        ETCD_ENDPOINTS = ETCD_ENDPOINTS + '''CALICO_VER="%s"''' % self.calico_ver

        with open("/tmp/%s/calico-node" % self.calico_node_name, 'w') as nodefd:
            nodefd.write(ETCD_ENDPOINTS)

        calico_conf = '''
{
    "name": "calico-k8s-network",
    "cniVersion": "0.1.0",
    "type": "calico",
    "etcd_endpoints": "%s",
    "log_level": "info",
    "ipam": {
        "type": "calico-ipam"
    },
    "policy": {
        "type": "k8s"
    },
    "kubernetes": {
	"k8s_api_root": "%s"
    }
}
        ''' % (etcd_servers, ks8_apiservers)

        with open("/tmp/%s/10-calico.conf" % self.calico_node_name, 'w') as nodefd:
            nodefd.write(calico_conf)

    def install_calico(self):
        copy_cfg_ansible = simple_ansible('copy calico bin ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/opt/cni/bin/calico dest=/opt/cni/bin/ owner=root group=root mode=0777',
                                          private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                          ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()

        copy_cfg_ansible = simple_ansible('copy calico bin ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/opt/cni/bin/calico-ipam dest=/opt/cni/bin/ owner=root group=root mode=0777',
                                          private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                          ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()
        copy_cfg_ansible = simple_ansible('copy calico bin ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/usr/bin/calicoctl dest=/usr/bin/ owner=root group=root mode=0777',
                                          private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                          ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()
        copy_cfg_ansible = simple_ansible('copy calico bin ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/opt/cni/bin/loopback dest=/opt/cni/bin/ owner=root group=root mode=0777',
                                          private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                          ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()

        copy_cfg_ansible = simple_ansible('copy calico service ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/etc/onekey_deploy/calico-node.service dest=/usr/lib/systemd/system/ owner=root group=root mode=0777',
                                          private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                          ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()

    def copy_configfile_to_host(self):
        copy_cfg_ansible = simple_ansible('copy calico configure file ', '%s,' % self.calico_node_ip, 'no', 'copy',
                                          'src=/tmp/%s/calico-node dest=/etc/kubernetes/ owner=root group=root mode=0777'
                                          % (self.calico_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ssh_user, ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()
        copy_cfg_ansible = simple_ansible('copy 10-calico.conf configure file ', '%s,' % self.calico_node_ip, 'no',
                                          'copy',
                                          'src=/tmp/%s/10-calico.conf dest=/etc/cni/net.d/ owner=root group=root mode=0777' % (
                                              self.calico_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ssh_user, ansible_sudo_pass=self.sudo_passwd)
        copy_cfg_ansible.run()

    def start_calico_node(self):
        start_node_ansible = simple_ansible('start calico-node node ', '%s,' % self.calico_node_ip, 'no', 'shell',
                                            'systemctl enable calico-node && systemctl start calico-node',
                                            private_key_file=self.private_key_file, ansible_ssh_user=self.ssh_user,
                                            ansible_sudo_pass=self.sudo_passwd)
        start_node_ansible.run()

    def restart_calico_node(self):
        start_node_ansible = simple_ansible('restart calico-node node ', '%s,' % self.calico_node_ip, 'no', 'shell',
                                            'systemctl restart calico-node', private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ssh_user, ansible_sudo_pass=self.sudo_passwd)
        start_node_ansible.run()
