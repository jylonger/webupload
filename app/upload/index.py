#coding:utf-8
import os

class Upload():
    def __init__(self):
        pass

    #合并文件
    def mergefiles(self,rndstr,filename,filenum):
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        with open('{}\\files\\{}\\{}'.format(path,rndstr,filename), 'wb') as file:  # 创建新文件
            for i in range(filenum):
                try:
                    filename = '{}\\files\\{}\\data\\{}'.format(path,rndstr,i)
                    source_file = open(filename, 'rb')  # 按序打开每个分片
                    file.write(source_file.read())  # 读取分片内容写入新文件
                    source_file.close()
                except IOError:
                    break
                #删除已合并的分片
                #os.remove(filename)

if __name__=='__main__':
    u=Upload()
    u.mergefiles("j5pBzn3Ni6AYpFh6","图标文件.zip",2)