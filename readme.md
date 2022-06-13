# 0. 更新
### (2022.6.13)
- 适配新的5s确认框
- 报错时生成日志文件
### (2022.6.6)
- 出入校填报改为【园区往返】新格式
- Win10上使用Edge浏览器时会自动下载对应版本Webdriver，无需手动下载

### （2022.5.4）
**【过时】**：出入校填报更新为审批制，需要上传核酸、健康宝、行程卡截图，特别是对校外同学必须上传健康宝截图，在情况发生改变之前本程序暂时作废

### (2022.3.19)

现在优化了程序，不再需要手动改json了，而是直接命令行输入后编码存储。

输入密码也不再明文显示了

尝试用pyinstaller编译为exe，可能也不再需要装python了

### (2021.11.23)
适应了现今的出入校填报系统，用历史填报功能

对edge增加headless功能，可以不弹窗执行了（终于不会被说像按键精灵了……虽然其实是一样的）

学校现在忘填两次就会被禁止出入校orz（因为出入各算一次所以其实只要忘了一天就gg）


# 1. 目的

自动填报上一次出入校记录的小工具。

自动化拯救人类:)

# 2. 安装

本工具依赖python3的selenium库。安装可以参考这个[知乎专栏](https://zhuanlan.zhihu.com/p/111859925)，也可以参考[官方文档](https://selenium-python.readthedocs.io/installation.html)。简单说明要点：

selenium是一款用于自动化调试网页的工具，可以用脚本模拟用户键盘、鼠标等输入，可以看作一个机器人控制的浏览器。

安装方法：`pip install selenium`

selenium需要依赖一个浏览器内核才可以运行。可以下载Edge的内核，[官方链接](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)。也可以在上面的知乎链接里用其他浏览器，但是没有经过测试不保证能用。

# 3. 初始化

### 3.1 用户基本信息输入

本工具使用`conf.json`文件来输入用户的信息（如学号，密码等）和一些其他选项。项目中附带的`conf-template.json`文件是这一文件的模板，第一次使用时需要自行定制。各项含义说明如下：

1. stuid：学号
2. passwd: 密码
3. webdriver_path: 内核的路径
4. driver_name: 内核的名称，默认Edge，也可以用Chrome, Firefox, Safari等等。和3的内核文件必须一致。

各项按需求修改完毕后，将文件名修改为`conf.json`即可结束。

### 3.2 第一次使用

本工具会使用“自动填报上一次信息”的功能，确保你确实是要这么做！

要出入多个校区的同学抱歉啦，实现起来会有点麻烦，暂时还没做。

# 4. 使用

Win10下确保Python、Selenium正确安装，conf.json正确配置后，双击run.bat即可。

其它系统的用户不能使用bat文件，但可以在命令行里用`python main.py`的方式运行。

# 5. 我能否让本程序每天固定时间执行？

在Win10系统下，可以。同时我也相信在其他系统下也可以。这里简单提供win10系统下的操作方法：

1. 右击**【此电脑】-【管理】-【任务计划程序】**，单击右侧【创建任务】
2. 在【常规】下，名称描述自选，**勾选【不管是否要登录都要执行】，不选【不存储密码】**，这是为了在锁屏状态下也能执行。
3. 在【触发器】下点【新建】，设置开始日期，间隔，结束日期等等。
4. 在【操作】下点【新建】，操作：启动程序，【程序或脚本】选择run.bat，**【起始于】填写所在的文件夹**。
5. 在【条件】下，视需求勾选只有插入电源时运行，勾选只在有网络时运行（不然跑个寂寞= =）
6. 确定即可，注意电脑不要关机，睡眠即可（一般笔记本合盖就是睡眠）

其它系统请自行查找相关教程。

