import socket
from sys import argv
import gevent
from gevent import monkey
import time
import random
import re
import hashlib,pickle

cache = {}
timec = {}

def pID2Url(pid):
    tc=0
    try:
        tc=timec[pid]
    except:
        pass
    t = time.time()
    if ((t-tc) > 5):
        import getmigu as gm
        curl=gm.getMiguContId(pid)
        furl=gm.pushUrl(gm.ddCalcu(curl))
        cache[pid]=furl
        timec[pid]=int(t)
    else:
        furl=cache[pid]
    return furl

def mID2Url(mID,idx):
    tc=0
    inr = "%s-%s" % (mID,idx)
    try:
        tc=timec[inr]
    except:
        pass
    t = time.time()
    if ((t-tc) > 5):
        try:
            import listmigu as lm
            import getmigu as gm
            pid=lm.getDbID(mID)[int(idx)]["pID"]
            curl=gm.getMiguContId(pid)
            furl=gm.pushUrl(gm.ddCalcu(curl))
        except:
            furl=''
        cache[inr]=furl
        timec[inr]=int(t)
    else:
        furl=cache[inr]
    return furl

# 服务器类
class WISG(object):
    def __init__(self, port):
        self.port = port
        # 创建主套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 允许端口重用
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 主套接字绑定端口
        self.server_socket.bind(("", self.port))
        # 主套接字转为被动模式
        self.server_socket.listen(128)
        pass

    # 启动服务器对象的入口函数
    def run_forever(self):
        self.create_new_socket()
        pass
    
    # 创建新的套接字,使用gevent,使新的套接字以消耗少量资源的协程方式运行
    def create_new_socket(self):
        while True:
            new_client_socket, new_client_socket_addr = self.server_socket.accept()
            gevent.spawn(self.deal_accept_data, new_client_socket)

    # 处理接收到的数据
    def deal_accept_data(self, new_client_socket):
        recv_data = new_client_socket.recv(1024)
        # 接收到的请求为utf-8格式,解析数据
        recv_data = recv_data.decode("utf-8")
        # 如果收到客户端发送的空字符,则关闭连接
        if not recv_data:
            return
        # 将接收到的数据转换为列表
        recv_data_list = recv_data.splitlines()

        # 获取请求头信息
        the_request_header = recv_data_list[0]
        
        file_name = self.get_file_name(the_request_header)
        if file_name.startswith("/live"):
            import getmigu as gm
            arr=file_name.split("/")
            if(len(arr)>2):
                try:
                        pid=arr[2]
               	        pidu=pID2Url(pid)
                        self.send_m3u8(pidu, new_client_socket)
                except:
                        self.send_empty(new_client_socket)
                new_client_socket.close()
                return

        if file_name.startswith("/room"):
            import getmigu as gm
            arr=file_name.split("/")
            if(len(arr)>2):
                mId=arr[2]
                if(len(arr)>3):
                    Idx=str(int(arr[3])-1)
                else:
                    Idx='0'
                try:
                        pidu=mID2Url(mId,Idx)
                        self.send_m3u8(pidu, new_client_socket)
                except:
                        self.send_empty(new_client_socket)
                new_client_socket.close()
                return

        self.send_empty(new_client_socket)
        new_client_socket.close()

    # 根据请求头信息,获得本地对应以.html或.py尾缀的文件名
    def get_file_name(self, the_request_header):
        """GET /index.html HTTP/1.1"""
        file_name = re.match(r"[^/]+([^ ]+).*", the_request_header).group(1)
        if file_name == "/":
            file_name = "/index.html"
        return file_name
        pass      

    def send_empty(self, new_client_socket):
        respond_body = ""
        respond_header = "HTTP/1.1 404 Not Found \r\n"
        respond_header = respond_header + "\r\n"
        # 发送回应
        new_client_socket.send(respond_header.encode("utf-8"))
        pass

    def send_m3u8(self, url, new_client_socket):
        #content = "#EXTM3U\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2084544\n"+url+"\n"
        if url=='':
            self.send_empty(new_client_socket)
            return
        content = ""
        respond_body = content.encode("utf-8")
        #respond_header = "HTTP/1.1 200 OK \r\n"
        respond_header = "HTTP/1.1 301 Moved Permanently"
        respond_header += "Content-Type: Application/vnd.apple.mpegurl\r\n"
        respond_header += "Location: %s\r\n" % url
        respond_header = respond_header + "\r\n"
        
        # 发送回应
        new_client_socket.send(respond_header.encode("utf-8"))
        new_client_socket.send(respond_body)
        print("内容发送成功!")
        pass

    def send_html(self, file_name, new_client_socket):
        try:
            f = open(self.root_dir+file_name, "rb")
        except Exception as res:
            print(res)
            print("无法找到网页404")
        else:
            content = f.read()

        respond_body = content
        respond_header = "HTTP/1.1 200 OK \r\n"
        respond_header += "Content-Type: text/html; charset=utf-8\r\n"
        respond_header = respond_header + "\r\n"
        
        # 发送回应
        new_client_socket.send(respond_header.encode("utf-8"))
        new_client_socket.send(respond_body)
        print("内容发送成功!")
        pass


    # 发送静态文件的html到客户端
    def send_html(self, file_name, new_client_socket):
        try:
            f = open(self.root_dir+file_name, "rb")
        except Exception as res:
            print(res)
            print("无法找到网页404")
        else:
            content = f.read()

        respond_body = content
        respond_header = "HTTP/1.1 200 OK \r\n"
        respond_header += "Content-Type: text/html; charset=utf-8\r\n"
        respond_header = respond_header + "\r\n"
        
        # 发送回应
        new_client_socket.send(respond_header.encode("utf-8"))
        new_client_socket.send(respond_body)
        print("内容发送成功!")
        pass

    def set_response_header(self, status, headers):


        #将从web框架收到的状态码,和返回的头信息存储到一个列表里面
        self.dynamic_respond_header = [status, headers]
        # 组建返回头信息
        dynamic_respond_header = "HTTP/1.1 %s \r\n"
        dynamic_respond_header += "%s:%s\r\n"%(headers[0][0], headers[0][1])
        dynamic_respond_header += "\r\n"
        # 将列表中的数据进行整理,转为可直接使用的"返回头"信息,然后存到类变量dynamic_response_headers_info
        self.dynamic_response_headers_info =  dynamic_respond_header.encode("utf-8")
        pass


def main():
    monkey.patch_all()
    # 创建web服务器
    if len(argv) == 2:
        port = int(argv[1])

    # 传入端口号,和来自web框架的函数app
    web_server = WISG(port)
    print("端口号为%s"%(port))
    print("请在地址栏访问 127.0.0.1:%d"%(port))

    # 启动web服务器
    web_server.run_forever()
    pass

if __name__ == "__main__":
    main()
