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

```
 pip install -r requirements.txt

 安装node

 cp config.py.example config.py

 修改config.py配置

 cd node_server;node app.js &

 cd ..;python deploy.py

 python app.py
```