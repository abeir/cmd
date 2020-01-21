# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class CmdArg(object):
    """
    参数对象，存储了短参名、长参名、是否需要参数值、参数描述
    """

    def __init__(self, short_name: str, long_name: str, need_value: bool, description: str):
        """
        创建参数对象，存储短参名、长参名、是否需要参数值、参数描述

        :param short_name: 短参名 (str)
        :param long_name: 长参名 (str)
        :param need_value: 是否需要参数值 (bool)
        :param description: 参数描述 (str)
        """
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.need_value = need_value


class Cmd(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__args = OrderedDict()

    def add_arg(self, arg_flag, arg: CmdArg):
        """
        添加一个参数，参数的详细信息由 CmdArg 定义

        :param arg_flag: 参数的标识符，根据该标识符存取参数对象。若命令提供多个参数，标识符不可重复
        :param arg: 参数对象 CmdArg
        """
        self.__args[arg_flag] = arg

    def get_arg(self, arg_flag):
        """
        通过参数标识符获取参数对象

        :param arg_flag: 参数的标识符
        :return: 参数对象 CmdArg，若标识符对应的参数不存在返回空
        """
        return self.__args[arg_flag]

    def short_name(self, arg_flag):
        """
        获取参数对象中的短参名

        :param arg_flag: 参数的标识符
        :return: 短参名，若标识符对应的参数不存在返回空字符串
        """
        cmd_arg = self.__args[arg_flag]
        if cmd_arg:
            return cmd_arg.short_name
        return ''

    def long_name(self, arg_flag):
        """
        获取参数对象中的长参名

        :param arg_flag: 参数的标识符
        :return: 长参名，若标识符对应的参数不存在返回空字符串
        """
        cmd_arg = self.__args[arg_flag]
        if cmd_arg:
            return cmd_arg.long_name
        return ''

    def description(self, arg_flag):
        """
        获取参数对象中的参数描述

        :param arg_flag: 参数的标识符
        :return: 参数描述，若标识符对应的参数不存在返回空字符串
        """
        cmd_arg = self.__args[arg_flag]
        if cmd_arg:
            return cmd_arg.description
        return ''

    def need_value(self, arg_flag):
        """
        获取参数对象中的是否需要参数值配置

        :param arg_flag: 参数的标识符
        :return: 是否需要参数值，若标识符对应的参数不存在返回 False
        """
        cmd_arg = self.__args[arg_flag]
        if cmd_arg:
            return cmd_arg.need_value
        return False

    def args(self):
        """
        多组参数对象CmdArg

        :return: 多组的参数（元组）
        """
        return tuple(self.__args.values())

    @abstractmethod
    def name(self):
        """
        命令名

        :return: 命令名（字符串）
        """
        return ''

    @abstractmethod
    def exec(self, short_arg, long_arg, value):
        """
        执行指令

        :param short_arg: 指令中的短参数，若使用长参数此处可能为空
        :param long_arg: 指令中的长参数，若使用短参数此处可能为空
        :param value: 指令中的参数值
        """
        pass

