# -*- coding: UTF-8 -*-
import getopt
import re
import sys

from command import Cmd
from util import CommandNotFoundError, CmdHelper
from util.cmd_loader import CmdLoader

USAGE_HEAD = 'Run command.\ncmd.py <sub-command> <argv>'
USAGE_SUBCMD_FMT = "\n{0}:"
USAGE_ARG_FMT = "\n{0:>4}, {1:<12}{2}"


class DefaultCmdHelper(CmdHelper):
    """
    CmdHelper的实现，组装子命令的帮助以及根据命令行参数运行子命令
    """

    def __init__(self):
        self.__usage_head = USAGE_HEAD # 帮助的顶部信息
        self.__usage = ''   # 完整的帮助
        self.__subcmd = {}  # 子命令实例，key为子命令名，value为实例
        self.__subcmd_short_opts = {}   # 子命令短参名，key为子命令名，value为短参名
        self.__subcmd_long_opts = {}    # 子命令长参名，key为子命令名，value为长参名
        self.__subcmd_usage = {}       # 子命令帮助，key为子命令名，value为帮助信息
        self.__cmd_loader = None    # 命令加载器

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
        """
        设置帮助中的顶部信息，默认为USAGE_HEAD中的信息

        :param usage_head: 帮助的顶部信息
        :return: 当前对象，允许链式调用
        """
        if isinstance(usage_head, str):
            self.__usage_head = usage_head
        return self

    def set_cmd_loader(self, cmd_loader: CmdLoader):
        """
        设置命令实现的加载器，加载器必须是一个CmdLoader的实现，提供了两种默认的加载器实现ModuleFileCmdLoader, SimpleCmdLoader

        :param cmd_loader: 命令加载器
        :return: 当前对象，允许链式调用
        """
        self.__cmd_loader = cmd_loader
        return self

    def usage(self, subcmd=''):
        """
        获取帮助信息，用于在命令行中打印帮助。

        :param subcmd: 子命令的名称
        :return: 若参数subcmd为空，则返回完整的帮助，否则只返回subcmd指定的子命令帮助
        """
        if subcmd and self.__subcmd_usage[subcmd]:
            print(self.__usage_head + self.__subcmd_usage[subcmd])
            return
        print(self.__usage)

    def short_opts(self, subcmd):
        """
        获取子命令中的短参数名

        :param subcmd: 子命令的名称
        :return: 短参数名，若子命令不存在则返回空
        """
        return self.__subcmd_short_opts[subcmd]

    def long_opts(self, subcmd):
        """
        获取子命令中的长参数名

        :param subcmd: 子命令的名称
        :return: 长参数名，若子命令不存在则返回空
        """
        return self.__subcmd_long_opts[subcmd]

    def assemble(self):
        """
        加载指令类，并组装帮助信息
        """
        self.__cmd_loader.load()
        for cmd in self.__cmd_loader.cmd_instances():
            sub_cmd_name = cmd.name()
            self.__assemble_cmd(sub_cmd_name, cmd)
            args = cmd.args()
            if not isinstance(args, tuple):
                return
            self.__assemble_help_cmd(sub_cmd_name)
            for arg in args:
                self.__assemble_help_arg(sub_cmd_name, arg.short_name, arg.long_name, arg.description)
                self.__assemble_subcmd_opts(sub_cmd_name, arg.short_name, arg.long_name, arg.need_value)

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
    """
    解析命令行参数，并根据参数执行对应的子命令

    :param argv: 命令行参数 sys.argv
    :param loader: 子命令加载器，提供两种默认实现ModuleFileCmdLoader, SimpleCmdLoader，可按需传入
    :param helper: 用户生成
    """
    if helper is None:
        helper = DefaultCmdHelper()
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
