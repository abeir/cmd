# -*- coding: UTF-8 -*-
import os

from command import Cmd


class NetworkCmd(Cmd):

    def __init__(self):
        self.__arg_start = ('-s', '--start', 'Run service network-manager start.', False)
        self.__arg_stop = ('-t', '--stop', 'Run service network-manager stop.', False)
        self.__arg_restart = ('-r', '--restart', 'Run service network-manager restart.', False)

    def cmd_name(self):
        return 'network'

    def arg_names(self):
        return self.__arg_start, self.__arg_stop, self.__arg_restart

    def exec(self, short_arg, long_arg, value):
        if short_arg == self.__arg_start[0] or long_arg == self.__arg_start[1]:
            os.system('sudo service network-manager start')
        elif short_arg == self.__arg_stop[0] or long_arg == self.__arg_stop[1]:
            os.system('sudo service network-manager stop')
        elif short_arg == self.__arg_restart[0] or long_arg == self.__arg_restart[1]:
            os.system('sudo service network-manager restart')
