# 基于socket的小型局域网聊天室
本程序是基于TCP协议的简单局域网聊天室，在代码中的主要部位有相应注释进行说明。


使用方法：
1.先在局域网内的服务器上运行服务端；
2.在客户机上运行客户端。

注意事项：
1.在使用客户端进行连接之前请先确保在该局域网内有服务端在运行；
2.请使客户端要连接的端口与服务端自身设置的端口保持一致；
3.在使用客户端时，请不要在文本框内输入过多的文本，本软件仅为实现局域网内的简单交流。并不适用于长文本交流；
3.如果想在同一主机同时打开多个服务端，请不要使用与已打开的服务端共同的端口，同时请尽量避免使用已注册端口；
4.同一机器同时运行多个客户端是允许的，同时运行客户端和服务端也是允许的；
5.如果不知道本机的IP地址，可通过在控制台使用ipconfig命令查看。
