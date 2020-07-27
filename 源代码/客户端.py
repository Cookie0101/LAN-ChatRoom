import tkinter  # 窗口
import tkinter.messagebox  # 提示框
import os
import sys
import socket
import threading
import time

def get_resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# LOGO_PATH = 'resources' + os.sep + '聊天室图标.ico'  # 图标路径
# IMAGES_PATH = 'resources' + os.sep + '连接按钮.png'
LOGO_PATH = get_resource_path(os.path.join('resources', '聊天室图标.ico'))
IMAGES_PATH = get_resource_path(os.path.join('resources', '连接按钮.png'))
bufsize = 1024   # 接收消息的缓冲区大小
server_port = 56415  # 服务端的端口号
send_str = ' '


def test_main(self):
    main()


def main():
    global server_port
    name = name_in.get()
    server_ip = server_IP_in.get()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 使用TCP协议进行通信
    if server_port_in.get() != '':  # 端口号设置 如果没输入则为默认值
        server_port = int(server_port_in.get())

    def test_send_job(sock):
        send_job(sock)

    def delete_job():  # 避免遗留换行问题
        time.sleep(0.01)
        TextIn.delete('0.0', 'end')

    def send_job(sock):
        global send_str
        # while True:
        try:
            send_str = TextIn.get('0.0', 'end-1c')
            send_str = name + ':' + send_str  # 消息打包
            Onetext.configure(state='normal')
            Onetext.insert(tkinter.END, send_str, 'text_blue')
            Onetext.insert(tkinter.END, '\n')
            Onetext.see(tkinter.END)
            Onetext.configure(state='disabled')
            sock.send(send_str.encode('UTF-8'))  # 消息进行UTF-8编码
            delete_thread = threading.Thread(target=delete_job)  # 清空输入框
            delete_thread.start()  # 执行线程
        except:
            return

    def recv_job(sock):
        global send_str
        while True:
            try:
                recv_str = sock.recv(bufsize)
                recv_str = recv_str.decode('UTF-8')
                if recv_str != send_str:
                    Onetext.configure(state='normal')
                    Onetext.insert(tkinter.END, recv_str)
                    Onetext.insert(tkinter.END, '\n')
                    Onetext.see(tkinter.END)
                    Onetext.configure(state='disabled')
            except:
                tkinter.messagebox.showerror(title="小小咸鱼提醒您", message="与服务器的连接断开！程序已停止运行！")
                sock.close()
                exit()

    LogOn.destroy()  # 关闭登录窗口
    room = tkinter.Tk()
    room.title('小小咸鱼聊天室')  # 标题
    room.iconbitmap(LOGO_PATH)  # 图标路径
    room.geometry('500x600')  # 初始尺寸
    room.maxsize(500, 600)  # 最大大小
    room['background'] = "Silver"  # 设置背景色为银灰色

    Onetext = tkinter.Text(room, bg='white', relief=tkinter.SUNKEN)
    Onetext.place(x=5, y=5, width=490, height=400)

    Onetext.tag_config('text_green', foreground='green')
    Onetext.tag_config('text_blue', foreground='blue')
    Onetext.tag_config('text_red', foreground='red')

    TextIn = tkinter.Text(room, bg='white')
    TextIn.place(x=5, y=410, width=490, height=150)

# Onetext需要在右侧添加一个滚动条

    try:   # 与服务端建立连接并发送自己的名字及异常处理
        Onetext.insert(tkinter.END, '连接到服务端中，请稍后...\n', 'text_red')
        sock.connect((server_ip, server_port))
        sock.send(name.encode('UTF-8'))
        Onetext.insert(tkinter.END, '连接成功！欢迎来到小小咸鱼聊天室！\n', 'text_greed')
        Onetext.configure(state='disabled')
    except:
        tkinter.messagebox.showerror(title="小小咸鱼提醒您", message="连接失败！服务端未开启或IP地址有误！")
        sock.close()
        exit()

    TextIn.bind('<Return>', lambda tmp1: test_send_job(sock))

    TextIn.bind('<Control-Return>', lambda tmp2: TextIn.insert(tkinter.END, ''))

    SendButton = tkinter.Button(room, text='发送(ENTER)', command=lambda: send_job(sock))
    SendButton.place(x=410, y=565)

    tkinter.Label(room, text="Enter键发送消息，如果想要换行请使用Ctrl+Enter键。", bg='Silver', font=("楷体", 12)).place(x=9, y=567)

    recv_thread = threading.Thread(target=recv_job, args=(sock,))  # 创建接受消息线程
    recv_thread.setDaemon(True)
    recv_thread.start()  # 执行线程

    room.mainloop()
    sock.close()
    exit()


LogOn = tkinter.Tk()
LogOn.title("客户端登录")
LogOn.iconbitmap(LOGO_PATH)
LogOn.geometry('370x235')
LogOn.maxsize(370, 235)
LogOn.minsize(370, 235)

# 输入提示信息
tkinter.Label(LogOn, text="用户名:", font=("楷体", 15)).place(x=90, y=25)
tkinter.Label(LogOn, text="服务端IP:", font=("楷体", 15)).place(x=70, y=60)
tkinter.Label(LogOn, text="服务端端口号：", font=("楷体", 15)).place(x=30, y=95)
tkinter.Label(LogOn, text="请与服务端保持一致\n不填默认为56415", font=("新宋体", 9), fg="grey").place(x=170, y=120)

# 用户名的输入框
name_in = tkinter.StringVar()
name_acq = tkinter.Entry(LogOn, textvariable=name_in)
name_acq.place(x=170, y=27)
# 服务端IP的输入框
server_IP_in = tkinter.StringVar()
server_IP_acq = tkinter.Entry(LogOn, textvariable=server_IP_in)
server_IP_acq.place(x=170, y=62)
# 端口的输入框
server_port_in = tkinter.StringVar()
server_port_acq = tkinter.Entry(LogOn, textvariable=server_port_in)
server_port_acq.place(x=170, y=97)

# 登录按键
photo = tkinter.PhotoImage(file=IMAGES_PATH)
LogOnButton = tkinter.Button(LogOn, image=photo, bd=0, command=main)
LogOnButton.place(x=115, y=160)
LogOn.bind("<Return>", test_main)   # 回车实现与按钮相同功能

LogOn.mainloop()
