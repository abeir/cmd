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


class CommandException(Exception):
    pass


class CommandNotFoundError(CommandException):
    """
    异常：命令找不到
    """
    pass


class InvalidParameterError(CommandException):
    """
    异常：无效的参数
    """
    pass


class InsufficientParametersError(CommandException):
    """
    异常：无效的参数
    """
    pass

