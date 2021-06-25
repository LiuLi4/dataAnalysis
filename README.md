## uwsgi
```uwsgi
检查是否安装成功
    sudo pip3 freeze | grep -i 'uwsgi'
    
启动命令    
    cd 到uwsgi.ini所在目录
    uwsgi --ini uwsgi.ini
    
停止uwsgi
    cd 到uwsgi.ini所在目录
    uwsgi --stop uwsgi.pid
```

```nginx
Nginx安装命令
    sudo yum install nginx
    
查看安装版本
    nginx -v
    

```