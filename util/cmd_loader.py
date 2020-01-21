# -*- coding: UTF-8 -*-
import importlib
import os

from command import Cmd
from util import CmdLoader


def py_file_to_class_name(py_file):
    """
    将py文件名按照首字母大写驼峰式转换成类名。忽略文件名中的"_"并截断"."

    :param py_file: py文件名，非路径
    :return: 首字母大写驼峰式类名
    """
    class_name = []
    idx = 0
    next_upper = False
    for c in py_file:
        idx += 1
        if c == '.':
            break
        if c == '_':
            next_upper = True
            continue
        if idx == 1:
            class_name.append(c.upper())
            continue
        if next_upper and c != '_':
            class_name.append(c.upper())
            next_upper = False
            continue
        class_name.append(c)
    return ''.join(class_name)


class ModuleFileCmdLoader(CmdLoader):
    """
    基于python模块文件动态加载的CmdLoader实现。
    指定加载目录、文件后缀过滤、加载模块实现动态加载，动态加载要求每个py文件中仅一个Cmd实现类，实现类的类名必须与文件名一至并遵循首字母大写驼峰式。
    注意，该实现的加载目录必须是当前项目中的python包，不支持任意目录的加载
    """

    def __init__(self):
        self.__cmd_list = []
        self.__cmd_dir = ''
        self.__module_name = 'command'
        self.__file_suffix = '_cmd.py'

    def __find_cmd_py(self):
        """
        扫描并返回目录中的py文件

        :return: 目录中的py文件，非None
        """
        files = []
        for path in os.listdir(self.__cmd_dir):
            full_path = os.path.join(self.__cmd_dir, path)
            if path.endswith(self.__file_suffix) and os.path.isfile(full_path):
                files.append(path)
        return files

    def __load_module(self, py_file):
        """
        加载模块

        :param py_file: py文件名
        :return: 加载的模块对象
        """
        if py_file.endswith('.py'):
            py_file = py_file[:len(py_file) - 3]
        return importlib.import_module('.' + py_file, self.__module_name)

    def __new_cmd_instance(self, py_file):
        """
        加载py文件中的类并创建实例。

        :return: 实例
        """
        module = self.__load_module(py_file)
        if not module:
            return None
        class_name = py_file_to_class_name(py_file)
        clazz = getattr(module, class_name)
        if clazz:
            return clazz()
        return None

    def set_cmd_dir(self, cmd_dir):
        """
        设置加载的目录的绝对路径，扫描该路径下的所有py文件，注意，动态加载并不会加载此处目录的子目录

        :param cmd_dir:  加载目录的绝对路径
        :return: 当前对象，允许链式调用
        """
        if cmd_dir and isinstance(cmd_dir, str):
            self.__cmd_dir = cmd_dir
        return self

    def set_module_name(self, module_name):
        """
        设置模块名，扫描路径所对应的模块。默认为 command

        :param module_name: 模块名，子模块时以"."分隔
        :return: 当前对象，允许链式调用
        """
        if module_name and isinstance(module_name, str):
            self.__module_name = module_name
        return self

    def set_file_suffix(self, file_suffix):
        """
        设置文件后缀，程序按照此设置的后缀过滤，排除非此后缀的文件。默认为 _cmd.py

        :param file_suffix: 保留文件的后缀
        :return: 当前对象，允许链式调用
        """
        if file_suffix and isinstance(file_suffix, str):
            self.__file_suffix = file_suffix
        return self

    def load(self):
        """
        加载命令实现类。若设置的路径未能扫描到实现类文件，该方法会提前结束但是不会抛出异常。
        但是若扫描到文件却未能成功加载实现类，该方法中断并抛出异常

        :return: 当前对象，允许链式调用
        """
        files = self.__find_cmd_py()
        if not files or len(files) == 0:
            return
        for f in files:
            cmd_inst = self.__new_cmd_instance(f)
            if cmd_inst:
                self.__cmd_list.append(cmd_inst)
        return self

    def cmd_instances(self):
        """
        获取所有加载的Cmd实例

        :return: 实例列表，加载失败为空列表
        """
        return self.__cmd_list


class SimpleCmdLoader(CmdLoader):
    """
    简单的CmdLoader实现。通过调用add方法添加Cmd实现类的实例对象
    """

    def __init__(self):
        self.__cmd_list = []

    def add(self, cmd: Cmd):
        """
        添加Cmd实现类的实例对象

        :param cmd: Cmd实现类的实例对象，注意，同一个实现类对象不要多次添加
        :return: 当前对象，允许链式调用
        """
        self.__cmd_list.append(cmd)
        return self

    def load(self):
        """
        空实现

        :return: 当前对象，允许链式调用
        """
        return self

    def cmd_instances(self):
        """
        获取所有添加的Cmd实例对象

        :return: 实例列表，若未调用add则返回空列表
        """
        return self.__cmd_list
