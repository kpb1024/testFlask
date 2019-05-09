# Git
## 获取项目文件
`git clone git@github.com:kpb1024/testFlask.git`
## 更新到远程服务器上
```git
git add --all
git commit -m "blablalbla"
git push -u origin master
```

# 环境部署
安装虚拟环境 __virtualenv__
`pip install virtualenv`

# 运行应用
在`testFlask`文件夹下，生成虚拟环境`virtualenv venv`，此时会生成文件夹`/venv`
启动虚拟环境`source /venv/bin/acitvate`
运行 Flask APP :
```python
export FLASK_APP=ssms
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
```
-h 参数为0.0.0.0时能够从外部网络访问该应用，-p 参数指定端口

# 其他
分布式版本控制系统 Git 和 Python 虚拟环境工具 virtualenv 在 Linux 和 Windows 系统上都可以使用。
如果用成都IP的服务器的话，我已经配置好了公钥，可以直接 push 到远程仓库。
