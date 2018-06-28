# -*- coding: utf-8 -*-
# !/usr/bin/python


import pexpect
import utils
import os, getpass
from global_params import logger


# ip = sys.argv[1]
# password = sys.argv[2]

def ssh_key_copy(hosts_passwds):
    fail_host = {}
    if not hosts_passwds:
        return False, {'no host'}

    if type(hosts_passwds) != dict:
        return False, {'not support host type'}

    user_home = os.path.expanduser('~')
    ssh_key_list = ['(y/n)', 'id_rsa\):']
    if not os.access("%s/.ssh/id_rsa.pub" % user_home, os.F_OK):
        ssh_key = pexpect.spawn('''/usr/bin/ssh-keygen  -N '' ''')
        try:
            while True:
                idx = ssh_key.expect(ssh_key_list)
                if idx == 0:
                    ssh_key.sendline('y')
                elif idx == 1:
                    ssh_key.sendline('\n')

        except pexpect.EOF:
            if 'ERROR' in ssh_key.before:
                logger.error("ssh key create:%s" % ssh_key.before)
                for (ip, password) in hosts_passwds.items():
                    fail_host[ip] = "ssh key create error"
                return (False, fail_host)

    expect_list = ['(yes/no)', 'password:']
    flag = True

    for (ip, password) in hosts_passwds.items():
        if not utils.checkIP(ip):
            flag = False
            fail_host[ip] = 'check ip failed'
            continue

        p = pexpect.spawn('/usr/bin/ssh-copy-id  -i %s/.ssh/id_rsa.pub %s' % (user_home, ip))
        try:
            while True:
                idx = p.expect(expect_list)
                # print p.before + expect_list[idx],
                if idx == 0:
                    # print "yes"
                    p.sendline('yes')
                elif idx == 1:
                    # print password
                    p.sendline(password)
        # except pexpect.TIMEOUT:
        #    print >>sys.stderr, 'timeout'
        except pexpect.EOF:
            # print '------'
            # print ip
            # print p.before
            # print '------'
            if "ERROR" in p.before:
                logger.error("ssh key copy:%s" % p.before)
                flag = False
                # print type(p.before)
                # import pdb;pdb.set_trace()
                err_start = p.before.find("ERROR")
                fail_host[ip] = p.before[err_start:p.before.find('\n', err_start)]  # 'ssh-copy-id error'
            continue
            # print >>sys.stderr, '<the end>'
        except:
            flag = False
            fail_host[ip] = 'ssh-copy-id error'
            continue

    return (flag, fail_host)


###1：测试key 是否可用，主机网络是否可达等
###2：有些设置会在第一次ssh key登录时需要输入yes

def ssh_login(hosts, ssh_key):
    pass
