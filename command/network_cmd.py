# -*- coding: UTF-8 -*-
import os

from command import Cmd, CmdArg


class NetworkCmd(Cmd):

    start_flag = 'start'
    stop_flag = 'stop'
    restart_flag = 'restart'

    def __init__(self):
        super().__init__()
        self.add_arg(NetworkCmd.start_flag, CmdArg('-s', '--start', False, 'Run service network-manager start.'))
        self.add_arg(NetworkCmd.stop_flag, CmdArg('-t', '--stop', False, 'Run service network-manager stop.'))
        self.add_arg(NetworkCmd.restart_flag, CmdArg('-r', '--restart', False, 'Run service network-manager restart.'))

    def name(self):
        return 'network'

    def exec(self, short_arg, long_arg, value):
        if short_arg == self.short_name(NetworkCmd.start_flag) \
                or long_arg == self.long_name(NetworkCmd.start_flag):
            os.system('sudo service network-manager start')
        elif short_arg == self.short_name(NetworkCmd.stop_flag) \
                or long_arg == self.long_name(NetworkCmd.stop_flag):
            os.system('sudo service network-manager stop')
        elif short_arg == self.short_name(NetworkCmd.restart_flag) \
                or long_arg == self.long_name(NetworkCmd.restart_flag):
            os.system('sudo service network-manager restart')
