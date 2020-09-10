# 1. 目的

本工具的目的是尽可能简化贵校常态化的疫情防控填报流程，以将现有的云战役填报和出入校申报简化为一条命令即可完成为目标。我们开发自动化工具并不是不重视防控工作，而是为了让绝大多数健康状况良好的同学们更轻松地完成任务，降低填错、漏填的概率。在这个过程中，人的参与是必要的，人的主观意愿不能代替机器；因此，我们不建议用户使用完全自动化的工具（如win10的计划任务）和本工具组合使用，同时建议用户在出现异常状况时立即停用本工具，并在网页端手动填报。

# 2. 安装

本工具依赖python3的selenium库。安装可以参考这个[知乎专栏](https://zhuanlan.zhihu.com/p/111859925)，也可以参考[官方文档](https://selenium-python.readthedocs.io/installation.html)。简单说明要点：

selenium是一款用于自动化调试网页的工具，可以用脚本模拟用户键盘、鼠标等输入，可以看作一个机器人控制的浏览器。

安装方法：`pip install selenium`

selenium需要依赖一个浏览器内核才可以运行。可以下载Edge的内核，[官方链接](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)。也可以在上面的知乎链接里用其他浏览器，但是没有经过测试不保证能用。

# 3. 初始化

本工具使用`conf.json`文件来输入用户的信息（如学号，密码等）和一些其他选项。项目中附带的`conf-template.json`文件是这一文件的模板，第一次使用时需要自行定制。各项含义说明如下：

1. stuid：学号
2. passwd: 密码
3. webdriver_path: 内核的路径
4. driver_name: 内核的名称，默认Edge，也可以用Chrome, Firefox, Safari等等。和3的内核文件必须一致。
5. input_temperature: true/false，是否需要手动输入体温。为false时，则直接使用默认值（36.5）。为true时，需要在python输入框里手动输入当前体温值。

各项按需求修改完毕后，将文件名修改为`conf.json`即可结束。

# 4. 使用

在`main.py`中，`epidemic`函数用于填报云战役，*`epidemic_access`用于填报出入校（还在开发中）*。

如果不需要某个功能可以注释掉相应代码。

运行程序：

Win10下确保Python、Selenium正确安装，conf.json正确配置后，双击run.bat即可。

其它系统的用户不能使用bat文件，但可以在命令行里用`python main.py`的方式运行。

# 5. 后续计划 & 可能的改进

- **添加出入校自动申报功能**：等我返校之后开始做，应该两三天就能做好。
- 手动输入体温可否改成弹窗：现在输入体温用的是input函数，是在python窗口里的，会被selenium的浏览器窗口挡住。更好的做法应该是用JS弹出一个prompt框来处理输入，但我不会JS。感兴趣的话请Pull Request。