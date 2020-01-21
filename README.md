# cmd

本系统用于封装系统命令。可以单独作为命令行工具运行，也可以作为一个库使用。

代码中提供了封装的示例：command.network_cmd，该示例封装了ubuntu下的service network-manager命令
> $> cmd.py network -r    # 重启网络服务

# 介绍

本系统分为两部分，子命令的加载和帮助的组装。

## 子命令加载

提供了两种实现来加载子命令：
1. ModuleFileCmdLoader - 基于python模块文件动态加载
2. SimpleCmdLoader - 通过调用add方法添加子命令实例

### ModuleFileCmdLoader

默认的行为是根据指定的目录，获取以_cmd.py结尾的文件，每一个_cmd.py文件便是一个子命令的实现，再将文件名安装首字母大写的驼峰式转换成类名，以此类名来创建实例。

例如，network_cmd.py中的类名必须是首字母大写的驼峰式，即NetworkCmd，并且继承command.Cmd

由于此加载器基于importlib模块，所以加载的_cmd.py必须放置在自己的项目的包中，并调用此加载器中的set_module_name方法来设置包名。

### SimpleCmdLoader

该类的实现非常简单，提供了add方法用于逐个添加子命令的实例。

## 组装帮助

在 CmdLoader 加载完子命令后，会提取子命令中的参数定义和描述信息，生成帮助信息。

DefaultCmdHelper 类是默认的实现，其中的 usage 方法提供获取全部命令帮助和指定命令帮助两种。

另外，util.cmd_helper 模块提供了 run_cmd 函数，用于解析命令行参数并执行子命令
