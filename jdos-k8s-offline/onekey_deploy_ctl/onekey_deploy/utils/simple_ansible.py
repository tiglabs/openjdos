# -*- coding: utf-8 -*-
# !/usr/bin/env python

import json
import sys
import shutil
from collections import namedtuple

ansible_version = 0.0
try:
    from ansible.parsing.dataloader import DataLoader
    from ansible.vars.manager import VariableManager
    from ansible.inventory.manager import InventoryManager
    from ansible.playbook.play import Play
    from ansible.executor.task_queue_manager import TaskQueueManager
    from ansible.plugins.callback import CallbackBase

    ansible_version = 2.0
except:
    # https://www.cnblogs.com/PythonOrg/p/6030415.html
    import ansible.runner

    ansible_version = 1.0

import ansible.constants as C
import utils

try:
    class ResultCallback(CallbackBase):
        """A sample callback plugin used for performing an action as results come in

        If you want to collect all results into a single object for processing at
        the end of the execution, look into utilizing the ``json`` callback plugin
        or writing your own custom callback plugin
        """

        def __init__(self):
            self.runjson = {}

        def v2_runner_on_ok(self, result, **kwargs):
            """Print a json representation of the result

            This method could store the result in an instance attribute for retrieval later
            """
            host = result._host
            # abc = {host.name: result._result}
            # print json.dumps(abc).decode('unicode-escape')
            self.runjson = utils.merge_dicts(self.runjson, {host.name: result._result.get("stdout_lines", "")})
            # print json.dumps({host.name: result._result}, indent=4)
except:
    pass


class simple_ansible():
    def __init__(self, name, hosts, gather_facts, module, args, private_key_file=None, ansible_ssh_user='root',
                 ansible_sudo_pass=None, need_sudo=True):
        self.module = module
        if ansible_version == 2.0:
            # import pdb;pdb.set_trace()
            # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
            Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'sudo', 'become', 'become_method',
                                             'become_user', 'check', 'diff'])
            if need_sudo:
                become_method = 'sudo'
                sudo = 'yes'
            else:
                become_method = None
                sudo = 'no'
            self.options = Options(connection='smart', module_path=['/to/mymodules'], forks=10, sudo=sudo,
                                   become=need_sudo, become_method=become_method, become_user='root', check=False,
                                   diff=False)

            # initialize needed objects
            self.loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
            self.passwords = dict(vault_pass='secret')

            # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
            self.results_callback = ResultCallback()

            # create inventory, use path to host config file as source or hosts in a comma separated string
            self.inventory = InventoryManager(loader=self.loader, sources=hosts)

            # variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
            self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
            self.variable_manager.extra_vars = {"ansible_ssh_private_key_file": private_key_file,
                                                "ansible_ssh_user": ansible_ssh_user,
                                                "ansible_sudo_pass": ansible_sudo_pass}

            # create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.
            self.play_source = dict(
                name=name,
                hosts=hosts,
                gather_facts=gather_facts,
                tasks=[
                    dict(action=dict(module=module, args=args), register='shell_out')  # ,
                    # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
                ]
            )
        elif ansible_version == 1.0:
            self.runner = ansible.runner.Runner(
                host_list=hosts,
                pattern="all", forks=10,
                module_name=module, module_args=args,
                private_key_file=private_key_file,
                remote_user=ansible_ssh_user,
                become=need_sudo,
                become_pass=ansible_sudo_pass
            )
            ###extra_vars={"ansible_ssh_user":"root","ansible_ssh_pass":"xx"},

    def run(self):
        if ansible_version == 2.0:
            # Create play object, playbook objects use .load instead of init or new methods,
            # this will also automatically create the task objects from the info provided in play_source
            self.play = Play().load(self.play_source, variable_manager=self.variable_manager, loader=self.loader)
            # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
            tqm = None
            try:
                tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
                    stdout_callback=self.results_callback,
                    # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                )
                result = tqm.run(
                    self.play)  # most interesting data for a play is actually sent to the callback's methods
                return self.results_callback.runjson
            finally:
                # we always need to cleanup child procs and the structres we use to communicate with them
                if tqm is not None:
                    tqm.cleanup()

                # Remove ansible tmpdir
                shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
        elif ansible_version == 1.0:
            runjson = {}
            results = self.runner.run()
            if results is None:
                print "No hosts found"
                sys.exit(1)

            for (hostname, result) in results['contacted'].items():
                if self.module == 'shell':
                    try:
                        if not 'failed' in result:
                            runjson[hostname] = [result['stdout']]
                    except:
                        continue
                elif self.module == 'yum':
                    try:
                        if not 'failed' in result:
                            runjson[hostname] = ''
                    except:
                        continue
            return runjson

            # if __name__ == "__main__":
#    simple_ansible = simple_ansible('Ansible Play', 'localhost', 'no', 'shell', 'hostname')
#    simple_ansible.run()
