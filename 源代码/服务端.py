import tkinter  # 窗口
import os
import socket
import threading
import sys


def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


LOGO_PATH = get_resource_path(os.path.join('resources', '聊天室图标.ico'))
IMAGES_PATH = get_resource_path(os.path.join('resources', '登录按钮.png'))
Port = 56415  # 端口号
bufsize = 1024  # 缓冲区大小
online_num = 0  # 在线人数
message = ' '  # 收发消息的文本


def test_main(self):
    main()


def main():
    global Port

    def main_job(server):
        global message
        global online_num
        conlock = threading.Condition()  # 创建条件锁对象

        def send_job(name, connect):
            global online_num
            global message

            while True:
                conlock.acquire()
                conlock.wait()
                try:
                    connect.send(message)
                    conlock.release()
                except:
                    conlock.release()
                    break

        def recv_job(name, connect, IP):
            global online_num
            global message
            global UserMessage
            while True:
                try:
                    tmp = connect.recv(bufsize)
                    conlock.acquire()
                    message = tmp
                    conlock.notifyAll()
                    conlock.release()
                except:
                    conlock.acquire()
                    message = name + '退出了房间。'
                    message = message.encode('UTF-8')
                    conlock.notifyAll()
                    conlock.release()
                    connect.close()
                    UserMessage = ' 地址为 ' + IP + ' 的 ' + name + ' 用户关闭了连接。' + '\n'
                    notice.configure(state='normal')
                    notice.insert(tkinter.END, UserMessage, 'text_coral')
                    notice.see(tkinter.END)
                    notice.configure(state='disabled')
                    online_num -= 1
                    break

        while True:
            connect, address = server.accept()  # 接受连接 并存储来源相关的地址信息

            name = connect.recv(bufsize).decode('UTF-8')  # 记录用户的名字
            UserMessage = ' 已接受来自地址为 ' + address[0] + ' 的连接，用户名为：' + name + '\n'
            notice.configure(state='normal')
            notice.insert(tkinter.END, UserMessage)
            notice.see(tkinter.END)
            notice.configure(state='disabled')

            online_num += 1  # 在线人数+1
            message = '当前房间内在线人数为：' + str(online_num)
            connect.send(message.encode('UTF-8'))

            conlock.acquire()
            message = '欢迎' + name + '进入聊天室！'
            message = message.encode('UTF-8')
            conlock.notifyAll()
            conlock.release()

            # 每建立一个连接就为这个连接创建接受和发送线程
            send_thread = threading.Thread(target=send_job, args=(name, connect))
            send_thread.setDaemon(True)
            send_thread.start()
            recv_thread = threading.Thread(target=recv_job, args=(name, connect, address[0]))
            recv_thread.setDaemon(True)
            recv_thread.start()

    HostIP = HostIP_In.get()  # 获取IP地址
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp监听端口
    if Port_In.get() != '':  # 端口号设置 如果没输入则为默认值
        Port = int(Port_In.get())
    server.bind((HostIP, Port))  # 绑定端口和IP
    LogOn.destroy()  # 关闭登录窗口

    room = tkinter.Tk()
    room.title('小小咸鱼聊天室 [服务端]')  # 标题
    room.iconbitmap(LOGO_PATH)  # 图标路径
    room.geometry('500x600')  # 初始尺寸
    room.maxsize(500, 600)  # 最大大小
    # 设置一个文本区域
    notice = tkinter.Text(room, bg='white')
    notice.place(x=5, y=5, width=490, height=590)

    notice.tag_config('text_green', foreground='green')
    notice.tag_config('text_coral', foreground='coral')

    UserMessage = ' 本机IP地址：'+HostIP+'    服务端使用的接口：'+str(Port)+'\n\n'
    notice.insert(tkinter.END, UserMessage)
    UserMessage = ' 端口已绑定，开始等待客户端的连接...' + '\n'
    notice.insert(tkinter.END, UserMessage, 'text_green')
    notice.configure(state='disabled')  # 设置为只读

    server.listen(5)  # 设置最大连接数 等待连接

    main_thread = threading.Thread(target=main_job, args=(server,))
    main_thread.setDaemon(True)
    main_thread.start()
    room.mainloop()
    exit()


# 登陆界面主体
LogOn = tkinter.Tk()
LogOn.title("服务端登录")
LogOn.iconbitmap(LOGO_PATH)
LogOn.geometry('300x200')
LogOn.maxsize(300, 200)
LogOn.minsize(300, 200)

# 输入提示信息
tkinter.Label(LogOn, text="本机IP：", font=("楷体", 15)).place(x=30, y=30)
tkinter.Label(LogOn, text="端口号：", font=("楷体", 15)).place(x=30, y=70)
tkinter.Label(LogOn, text="不填默认为56415", font=("新宋体", 10), fg="grey").place(x=110, y=95)

# IP地址的输入框
HostIP_In = tkinter.StringVar()
IPacq = tkinter.Entry(LogOn, textvariable=HostIP_In)
IPacq.place(x=110, y=32)
# 端口的输入框
Port_In = tkinter.StringVar()
PortAcq = tkinter.Entry(LogOn, textvariable=Port_In)
PortAcq.place(x=110, y=72)
# 登录按键
photo = tkinter.PhotoImage(file=IMAGES_PATH)
LogOnButton = tkinter.Button(LogOn, image=photo, bd=0, command=main)
LogOnButton.place(x=80, y=125)
LogOn.bind("<Return>", test_main)   # 回车实现与按钮相同功能

LogOn.mainloop()