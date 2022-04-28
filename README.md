# kash_visualize

流调可视化

## 前端

### 依赖

- node
- yarn (ubuntu安装参考https://linuxize.com/post/how-to-install-yarn-on-ubuntu-18-04/)
- ant design
- echart
- redux

### HOW TO BUILD

```
cd fe
yarn (自动安装依赖)
yarn next build (编译)
yarn next start (启动前端，-p可以指定端口，默认3000)
```

可能碰到的问题

> ./node_modules/@antv/g6-pc/es/graph/controller/layout.js
> Attempted import error: 'LayoutWorker' is not exported from '../../layout/worker/layout.worker'.

解决方案：删除 fe/node_modules/@antv/g6-pc/es/graph/controller/layout.js:6 `import { LayoutWorker }` 的大括号删掉

## 后端

### 依赖

- python
- django
- mongoDB
- neo4j

### HOW TO RUN

```
cd server
pip3 install -r requirement.txt
python3 manage.py runserver <ip>:<port>
```

### mongoDB创建用户

```
# ~ mongodb
// 进入mongodb的shell里面
> db.createUser({user: "admin",pwd: "123456",roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]})
```


### 后端单元测试方法

**如何添加**单元测试

进入tests目录下，创建一个名为`test_<case_name>.py`的文件，仿照其他文件即可


**测试方法**

```
cd server/
python3 manage.py runserver test
```
