#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys

from util.cmd_helper import run_cmd
from util.cmd_loader import ModuleFileCmdLoader

if __name__ == '__main__':
    current_path = os.path.abspath(os.path.dirname(__file__))

    cmd_loader = ModuleFileCmdLoader()
    cmd_loader.set_module_name('command').set_cmd_dir(os.path.join(current_path, 'command'))

    run_cmd(sys.argv, cmd_loader)
    pass
