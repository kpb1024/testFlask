# Git协同开发
## 1. 获取项目文件
`git clone git@github.com:kpb1024/testFlask.git`

## 2. 在自己的分支上开发功能
创建自己的分支: `git branch $你的分支名字` 
切换到自己的分支: `git checkout $你的分支名字`

## 3. 提交更新到远程仓库自己的分支
![git原理](http://blog.kangpb.cn/2019/03/27/gitskill/gitadd.jpg)
提交到版本库的指令如下:
```git
git add --all
git commit -m "$Description"
```
在完成了某块功能时可以推送到远程仓库下自己的分支`git commit -m "关于改动的描述"`


## 4. 获取远程仓库主分支的更新
`git pull origin master` 会将主分支的更新拉(pull)到本地，`git checkout master`可以回到主分支查看更新
在自己的分支下，首先`git add --all & git commit -m "$Description"`把自己的所有更新提交到版本库，然后通过`git merge master`将版本库中的主分支的内容与自己的进行合并(merge)。合并完后需要在提示了发生改变的文件中查看更改，"======"分割线会划出不同的部分。


# 运行应用

运行 Flask 应用需要在Python环境下 `pip install -r requirements.txt` 安装requirements.txt文件里项目相关 python 包。

Linux 环境下运行 Flask APP 可以在/testFlask/下执行`sh run.sh`，代码如下：
```python
export FLASK_APP=ssms
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
```
-h 参数为0.0.0.0时能够从外部网络访问该应用，-p 参数指定端口

> 安装virtualenv
运行命令：pip intall virtualenv 直接安装
运行创建虚拟环境命令:virtualenv venv ，在当前目录下会成功生产一个venv文件夹。
开启虚拟环境：先cd venv，进入venv目录，输入Scripts\activate运行，开启成功。
关闭虚拟环境：输入deactivate回车成功关闭。

无论在什么环境下都要注意系统变量 FLASK_APP 和 FLASK_ENV 的设置，Windows 平台下通过`set FLASK_APP=ssms`设置系统变量。

# testFlask目录下的各文件
```
testFlask
|-- instance	//已弃用，旧版本所使用的数据库的本地文件
|   `-- ssms.sqlite
|-- notes.md
|-- README.md
|-- requirements.txt
|-- run.sh
|-- ssms
|   |-- auth.py	//登录、注册、强制要求登录等功能
|   |-- db.py	//数据库相关功能
|   |-- guanghong_info.py
|   |-- info.py	//主页、录入成绩等功能
|   |-- __init__.py	//ssms模块声明
|   |-- mysql.py	//被我魔改过的flask_ext.mysql模块
|   |-- reference.sql	//已弃用，依据需求报告写的建表语句
|   |-- schema.sql	//灵活、可随时修改的建表语句
|   |-- static	//静态文件如css、js
|   `-- templates	//前端网页模板
|       |-- auth
|       |-- base.html	//所有网页都继承的基础网页
|       `-- info
`-- ToDo.md	
```
