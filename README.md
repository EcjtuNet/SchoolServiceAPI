# 校园服务接口

## 实现功能：

* cas跳转登录智慧交大和教务系统

* 用户模型

* 获取所有15级及以后班级成员名单

* 用户姓名返回和验证接口

* 用户密码验证接口

* 用户信息接口

* 15级成绩,课表，考试安排查询接口

* 14级成绩查询接口

## TODO

* 14级课表, 考试安排接口

* 查饭卡，图书馆接口

* 查询信息缓存

## 部署方法
``请注意系统权限``

``` 
 > python版本
 
    python -V
 
    python 2.7
 
 > pip install virtualenv
 
 > virtualenv env
 
 > source env/bin/activate
 
 > pip install -r requirements.txt
 
 > 安装node服务 :
   
    node -v
 
    v7.1.0
    

> cp config.py.example config.py

> vim config.py

> cd node_server;node app.js &

> cd ..;python deploy.py

> gunicorn -c gunicorn.conf app:app &

```

```option: 使用supervisor```

```

> echo_supervisord_conf

> echo_supervisord_conf > /etc/supervisord.conf

> cd /etc;mkdir supervisor.d

> echo "files = /etc/supervisor.d/*.conf" >> supervisord.conf

> cd -;mv ss_supervisor.conf /etc/supervisor.d

> 修改ss_supervisor.conf配置

> supervisord -c /etc/supervisord.conf

> supervisorctl start ss_ecjtu_tech

```

``option: 开机自动启动 Supervisord``

> centos7.2
```
echo "/usr/bin/supervisord -c /etc/supervisord.conf" /etc/rc.d/rc.local

```
