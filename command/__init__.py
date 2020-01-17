# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod


class Cmd(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cmd_name(self):
        """
        命令名

        :return: 命令名（字符串）
        """
        pass

    @abstractmethod
    def arg_names(self):
        """
        多组参数名，包含了短参名、长参名和描述信息：(('短参数名', '长参数名', '描述', 是否需要参数值),)
        例：(('-n', '--name', 'the name', True), ('-a', '--all', 'all actions', False))

        :return: 多组的参数名，[0]为短参名，[1]为长参名（元组）
        """
        pass

    @abstractmethod
    def exec(self, short_arg, long_arg, value):
        """
        执行指令

        :param short_arg: 指令中的短参数，若使用长参数此处可能为空
        :param long_arg: 指令中的长参数，若使用短参数此处可能为空
        :param value: 指令中的参数值
        """
        pass
