#coding:utf-8
from sanic import Sanic
app = Sanic(__name__)
app.static('/static','app/static/')     #定义静态资源文件夹路径
app.static('/files','app/files/')         #提取pdf图片存放的文件夹路径
from webupload.app import main    #引入主文件