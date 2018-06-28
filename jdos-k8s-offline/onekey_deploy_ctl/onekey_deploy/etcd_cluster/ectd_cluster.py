# -*- coding:utf-8 -*-

import os
from utils.simple_ansible import simple_ansible

'''create etcd cluster
'''


class etcd_cluster():

    def __init__(self, etcd_node_ip, etcd_node_name, etcd_cluster_name, etcd_cluster_nodes, etcd_cluster_type,
                 etcd_conf_path='/etc/etcd/etcd.conf', private_key_file=None, ansible_ssh_user=None,
                 ansible_sudo_pass=None):
        '''
        etcd_cluster_nodes node dict eg: {ip1:hostnme1, ip2:hostname2....}
        etcd_cluster_type type of ectd_cluster ha or ....
        '''
        self.ETCD_INITIAL_CLUSTER_TOKEN = etcd_cluster_name
        self.cluster_nodes = etcd_cluster_nodes
        self.cluster_type = etcd_cluster_type
        self.etcd_node_name = etcd_node_name
        self.etcd_node_ip = etcd_node_ip
        self.conf_path = etcd_conf_path
        self.private_key_file = private_key_file
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_sudo_pass = ansible_sudo_pass
        self.ETCD_INITIAL_CLUSTER = ''
        for (node_ip, node_hostname) in etcd_cluster_nodes.items():
            if self.ETCD_INITIAL_CLUSTER:
                self.ETCD_INITIAL_CLUSTER = self.ETCD_INITIAL_CLUSTER + ''',%s=http://%s:2380''' % (
                node_hostname, node_ip)
            else:
                self.ETCD_INITIAL_CLUSTER = '''%s=http://%s:2380''' % (node_hostname, node_ip)

    def update_configfile(self):
        if not os.access(self.conf_path, os.F_OK):
            ###从目标结点考一份
            copy_cfg_ansible_from_oper_node = simple_ansible('synchronize etcd configure file from remote_node ',
                                                             '%s,' % self.etcd_node_ip, 'no',
                                                             'synchronize',
                                                             'dest=/tmp/etcd.conf src=/etc/etcd/etcd.conf mode=pull compress=yes',
                                                             private_key_file=self.private_key_file,
                                                             ansible_ssh_user=self.ansible_ssh_user,
                                                             ansible_sudo_pass=self.ansible_sudo_pass)
            copy_cfg_ansible_from_oper_node.run()
            self.conf_path = "/tmp/etcd.conf"
            # return False, 'The etcd.conf not exits..'

        cfg_str = ''
        with open(self.conf_path) as confd:
            for line in confd.readlines():
                if 'ETCD_LISTEN_PEER_URLS=' in line:
                    cfg_str = cfg_str + '''ETCD_LISTEN_PEER_URLS="http://0.0.0.0:2380"\n'''
                elif 'ETCD_LISTEN_CLIENT_URLS=' in line:
                    cfg_str = cfg_str + '''ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379,http://0.0.0.0:4001"\n'''
                elif 'ETCD_INITIAL_ADVERTISE_PEER_URLS=' in line:
                    cfg_str = cfg_str + '''ETCD_INITIAL_ADVERTISE_PEER_URLS="http://%s:2380"\n''' % self.etcd_node_ip
                elif 'ETCD_NAME=' in line:
                    cfg_str = cfg_str + '''ETCD_NAME="%s"\n''' % self.etcd_node_name
                elif 'ETCD_ADVERTISE_CLIENT_URLS=' in line:
                    cfg_str = cfg_str + '''ETCD_ADVERTISE_CLIENT_URLS="http://localhost:2379,http://localhost:4001"\n'''
                elif 'ETCD_INITIAL_CLUSTER=' in line:
                    cfg_str = cfg_str + '''ETCD_INITIAL_CLUSTER="%s"\n''' % self.ETCD_INITIAL_CLUSTER
                elif 'ETCD_INITIAL_CLUSTER_TOKEN=' in line:
                    cfg_str = cfg_str + '''ETCD_INITIAL_CLUSTER_TOKEN="%s"\n''' % self.ETCD_INITIAL_CLUSTER_TOKEN
                elif 'ETCD_INITIAL_CLUSTER_STATE=' in line:
                    cfg_str = cfg_str + '''ETCD_INITIAL_CLUSTER_STATE="new"\n'''
                else:
                    cfg_str = cfg_str + line

        # print cfg_str
        with open("/tmp/%s.conf" % self.etcd_node_name, 'w') as nodefd:
            nodefd.write(cfg_str)

    def copy_configfile_to_host(self):

        copy_cfg_ansible = simple_ansible('copy etcd configure file ', '%s,' % self.etcd_node_ip, 'no', 'copy',
                                          'src=/tmp/%s.conf dest=/etc/etcd/etcd.conf owner=root group=root mode=0777' %
                                          (self.etcd_node_name), private_key_file=self.private_key_file,
                                          ansible_ssh_user=self.ansible_ssh_user,
                                          ansible_sudo_pass=self.ansible_sudo_pass)
        copy_cfg_ansible.run()

    def start_etcd_node(self):
        start_node_ansible = simple_ansible('start etcd node ', '%s,' % self.etcd_node_ip, 'no', 'shell',
                                            'systemctl enable etcd && systemctl restart etcd',
                                            private_key_file=self.private_key_file,
                                            ansible_ssh_user=self.ansible_ssh_user,
                                            ansible_sudo_pass=self.ansible_sudo_pass)
        start_node_ansible.run()

    def check_etcd_cluster_health(self):
        pass
