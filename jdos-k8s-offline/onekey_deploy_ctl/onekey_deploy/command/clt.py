import sys, os
import argparse
from datetime import datetime, timedelta
from termcolor import colored


class CtlParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error:%s\n' % message)
        self.print_help()
        sys.exit(1)


class CtlError(Exception):
    pass


class Ctl(object):

    def __init__(self, params=None):
        self.commands = {}
        self.command_list = []
        self.main_parser = CtlParser(prog='onekey_deploy_ctl', description="onekey_deploy management tool",
                                     formatter_class=argparse.RawTextHelpFormatter)
        self.main_parser.add_argument('-v', help="verbose, print execution details", dest="verbose",
                                      action="store_true", default=False)
        self.sunshine_home = None
        self.properties_file_path = None
        self.ui_properties_file_path = None
        self.verbose = False
        self.extra_arguments = None
        self.params = params

    def register_command(self, cmd):
        assert cmd.name, "command name cannot be None"
        assert cmd.description, "command description cannot be None"
        self.commands[cmd.name] = cmd
        self.command_list.append(cmd)

    def run(self):

        if os.getuid() != 0:
            raise CtlError('sunshine-ctl needs root privilege, please run with sudo')

        # import pdb;pdb.set_trace()
        metavar_list = []
        for n, cmd in enumerate(self.command_list):
            if cmd.hide is False:
                metavar_list.append(cmd.name)
            else:
                self.command_list[n].description = None

        metavar_string = '{' + ','.join(metavar_list) + '}'
        subparsers = self.main_parser.add_subparsers(help="All sub-commands", dest="sub_command_name",
                                                     metavar=metavar_string)
        for cmd in self.command_list:
            if cmd.description is not None:
                cmd.install_argparse_arguments(subparsers.add_parser(cmd.name, help=cmd.description + '\n\n'))
            else:
                cmd.install_argparse_arguments(subparsers.add_parser(cmd.name))

        if self.params:
            args, self.extra_arguments = self.main_parser.parse_known_args(self.params)
        else:
            args, self.extra_arguments = self.main_parser.parse_known_args(sys.argv[1:])

        self.verbose = args.verbose
        globals()['verbose'] = self.verbose

        cmd = self.commands[args.sub_command_name]

        cmd(args)
