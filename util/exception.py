# -*- coding: UTF-8 -*-


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