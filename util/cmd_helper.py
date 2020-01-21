# -*- coding: UTF-8 -*-
import getopt
import re
import sys

from command import Cmd
from util import CommandNotFoundError
from util.cmd_loader import CmdLoader

USAGE_HEAD = 'Run command.\ncmd.py <sub-command> <argv>'
USAGE_SUBCMD_FMT = "\n{0}:"
USAGE_ARG_FMT = "\n{0:>4}, {1:<12}{2}"


class CmdHelper(object):

    def __init__(self):
        self.__cmd_list = []
        self.__usage_head = USAGE_HEAD
        self.__usage = ''
        self.__subcmd = {}
        self.__subcmd_short_opts = {}
        self.__subcmd_long_opts = {}
        self.__subcmd_usage = {}
        self.__cmd_loader = None

    def __assemble_help_cmd(self, subcmd_name):
        if subcmd_name in self.__subcmd_usage:
            return
        self.__usage = self.__usage_head + USAGE_SUBCMD_FMT.format(subcmd_name)
        self.__subcmd_usage[subcmd_name] = USAGE_SUBCMD_FMT.format(subcmd_name)

    def __assemble_help_arg(self, subcmd_name, short_arg, long_arg, desc):
        if subcmd_name not in self.__subcmd_usage:
            return
        self.__usage += USAGE_ARG_FMT.format(short_arg, long_arg, desc)
        self.__subcmd_usage[subcmd_name] += USAGE_ARG_FMT.format(short_arg, long_arg, desc)

    def __assemble_subcmd_opts(self, subcmd_name, short_arg, long_arg, need_val):
        if subcmd_name not in self.__subcmd_short_opts:
            self.__subcmd_short_opts[subcmd_name] = 'h'
        if subcmd_name not in self.__subcmd_long_opts:
            self.__subcmd_long_opts[subcmd_name] = ['help']

        if need_val:
            self.__subcmd_short_opts[subcmd_name] += short_arg[1:] + ':'
            self.__subcmd_long_opts[subcmd_name].append(long_arg[2:] + '=')
        else:
            self.__subcmd_short_opts[subcmd_name] += short_arg[1:]
            self.__subcmd_long_opts[subcmd_name].append(long_arg[2:])

    def __assemble_cmd(self, subcmd, cmd: Cmd):
        if not subcmd:
            return
        self.__subcmd[subcmd] = cmd

    def set_usage_head(self, usage_head):
        if isinstance(usage_head, str):
            self.__usage_head = usage_head
        return self

    def set_cmd_loader(self, cmd_loader: CmdLoader):
        self.__cmd_loader = cmd_loader
        return self

    def usage(self, subcmd=''):
        if subcmd and self.__subcmd_usage[subcmd]:
            print(self.__subcmd_usage[subcmd])
            return
        print(self.__usage)

    def short_opts(self, subcmd):
        return self.__subcmd_short_opts[subcmd]

    def long_opts(self, subcmd):
        return self.__subcmd_long_opts[subcmd]

    def assemble(self):
        self.__cmd_loader.load()
        for cmd in self.__cmd_loader.cmd_instances():
            sub_cmd_name = cmd.cmd_name()
            self.__assemble_cmd(sub_cmd_name, cmd)
            args = cmd.arg_names()
            if not isinstance(args, tuple):
                return
            self.__assemble_help_cmd(sub_cmd_name)
            for short_arg, long_arg, desc, need_val in args:
                self.__assemble_help_arg(sub_cmd_name, short_arg, long_arg, desc)
                self.__assemble_subcmd_opts(sub_cmd_name, short_arg, long_arg, need_val)

    def __find_subcmd(self, sub_cmd):
        if not sub_cmd:
            return None
        if sub_cmd in self.__subcmd:
            return self.__subcmd[sub_cmd]
        return None

    def run(self, sub_cmd, opt, value):
        cmd = self.__find_subcmd(sub_cmd)
        if not cmd:
            raise (CommandNotFoundError, "Can not found command: %s" % sub_cmd)
        if opt:
            if re.match(r'-\w+', opt):
                cmd.exec(opt, None, value)
                return True
            elif re.match(r'--\w+', opt):
                cmd.exec(None, opt, value)
                return True
        return False


def run_cmd(argv, loader: CmdLoader, helper: CmdHelper = None):
    if helper is None:
        helper = CmdHelper()
    helper.set_cmd_loader(loader)
    helper.assemble()

    if len(argv) < 2 or not argv[1] or argv[1] == '-h':
        helper.usage()
        return

    sub_cmd = argv[1]
    try:
        opts, args = getopt.getopt(argv[2:], helper.short_opts(sub_cmd), helper.long_opts(sub_cmd))
    except getopt.GetoptError:
        helper.usage()
        sys.exit(2)

    for opt, val in opts:
        if opt == "-h":
            helper.usage(sub_cmd)
            return
        if helper.run(sub_cmd, opt, val):
            return
        helper.usage(sub_cmd)
