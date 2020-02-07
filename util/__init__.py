# -*- coding: UTF-8 -*-
from abc import ABCMeta, abstractmethod


class CmdLoader(object):
    """
    Cmd实现类加载器，需要实现如何加载并返回所有Cmd实现类
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def load(self):
        """
        执行Cmd实现类加载

        :return: 当前对象，允许链式调用
        """
        return self

    @abstractmethod
    def cmd_instances(self):
        """
        获取所有加载的Cmd实例

        :return: 实例列表，未加载或加载失败应该返回空列表
        """
        return []


class CmdHelper(object):
    """
    Cmd帮助工具，提供生成命令的帮助、运行命令等操作
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_cmd_loader(self, cmd_loader: CmdLoader):
        """
        设置命令实现的加载器，加载器必须是一个CmdLoader的实现，提供了两种默认的加载器实现ModuleFileCmdLoader, SimpleCmdLoader

        :param cmd_loader: 命令加载器
        :return: 当前对象，允许链式调用
        """
        return self

    @abstractmethod
    def short_opts(self, subcmd):
        """
        获取子命令中的短参数名

        :param subcmd: 子命令的名称
        :return: 短参数名，若子命令不存在则返回空
        """
        return self

    @abstractmethod
    def long_opts(self, subcmd):
        """
        获取子命令中的长参数名

        :param subcmd: 子命令的名称
        :return: 长参数名，若子命令不存在则返回空
        """
        return self

    @abstractmethod
    def assemble(self):
        """
        加载指令类，并组装帮助信息
        """
        pass

    @abstractmethod
    def usage(self, subcmd=''):
        """
        获取帮助信息，用于在命令行中打印帮助。

        :param subcmd: 子命令的名称
        :return: 若参数subcmd为空，则返回完整的帮助，否则只返回subcmd指定的子命令帮助
        """
        pass

    @abstractmethod
    def run(self, sub_cmd, opt, value):
        """
        运行子命令

        :param sub_cmd: 子命令名
        :param opt: 参数名，传入的可能是短参名也可能是长参名
        :param value: 参数值
        """
        pass


class Const(object):
    """
    常量类
    初始化该类后，直接为该类赋值属性即定义常量。常量只允许定义属性时赋值，否则跑出错误。注意定义常量时不要使用类中的内置属性
    """

    class ConsError(TypeError):
        pass

    class ConstCaseError(ConsError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConsError, "Can't change const.%s" % name)
        if not name.isupper():
            raise (self.ConstCaseError, "const name '%s' is not all uppercase" % name)
        self.__dict__[name] = value


