#coding:utf-8
import asyncio,uuid
from webupload.app import app
from sanic.response import json
from sanic_jinja2 import SanicJinja2
from webupload.app.upload.index import *

#把app传进去实例化jinja对象
jinja = SanicJinja2(app)
app.ws = {}

#首页
@app.route('/')
async def index(request):
    msg={"name":"李大厨","sex":"男","uid":uuid.uuid4()}
    return jinja.render('index.html',request, msg=msg)

#上传文件接口
@app.route('/upload',methods=["POST"])
async def upload(request):
    args = request.args if request.method == 'GET' else request.form
    filename = args.get('filename', '')    #文件名
    filenum = args.get('filenum', 0)       #文件分片总数
    rndstr = args.get('rndstr', '')        #随机字符串（唯一标识）
    zoneid = args.get('zoneid', 0)         #当前分片id
    file = request.files.get('file')       #文件流
    path = os.path.abspath(os.path.dirname(__file__))
    #基本文件夹路径
    basepath="{}\\files\\{}".format(path,rndstr)
    datapath="{}\\data".format(basepath)
    if not os.path.exists(datapath):
        os.makedirs(datapath)
    #保存文件分片
    with open("{}\\{}".format(datapath,zoneid), 'wb') as f:
         f.write(file.body)
    #记录当前完成的分片id
    with open("{}\\record.txt".format(basepath), 'w',encoding="utf-8") as f:
         txt="{}|{}".format(zoneid,rndstr)
         f.write(txt)
    #判断文件是否上传完毕
    if int(filenum)==int(zoneid)+1:
        u=Upload()
        u.mergefiles(rndstr,filename,int(filenum))
    msg={"code":200,"msg":"开始上传"}
    return json(msg)

#获取文件上传保存的进度
@app.route('/getrecord',methods=["POST"])
async def getrecord(request):
    args = request.args if request.method == 'GET' else request.form
    rndstr = args.get('rndstr', '')
    if rndstr!="":
        path = os.path.abspath(os.path.dirname(__file__))
        basepath = "{}\\files\\{}".format(path, rndstr)
        if os.path.exists("{}\\record.txt".format(basepath)):
            with open("{}\\record.txt".format(basepath), 'r') as f:
                result=f.read()
                print(result)
            if result!="":
                zoneid=int(result.split("|")[0])+1
                msg = {"code": 200, "msg": "请求成功", "zoneid": zoneid}
        else:
            msg = {"code": 203, "msg": "正在创建文件中"}
    else:
        msg = {"code": 204, "msg": "请求异常"}
    return json(msg)

#执行提取方法
async def extract_pdf(id,stream,foldername,matrix):
    print("已成功删除了websocket:",id)


#PDF执行进度websocket
@app.websocket('/extract/<id>')
async def extract(request, ws, id):
    app.ws[id] = ws
    while True:
        result=await ws.recv()
        print("result",result)

#app.add_websocket_route(extract, '/extract')
