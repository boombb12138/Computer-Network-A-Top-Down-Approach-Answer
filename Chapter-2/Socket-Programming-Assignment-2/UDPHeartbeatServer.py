from socket import *
import time
import threading

def check_clients():
    """定期检查客户端状态的线程函数"""
    while True:
        try:
            current_time = time.time()
            # 检查所有客户端状态
            for client_address, last_seen in list(client_last_seen.items()):
                if current_time - last_seen > 30:  # 如果超过30秒没收到心跳
                    print(f"客户端 {client_address} maybe已断开")
                    del client_last_seen[client_address]
            time.sleep(1)  # 每秒检查一次
        except:
            break

# 创建服务器socket
serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

client_last_seen = {}  # 记录每个客户端最后一次心跳的时间
print(f"服务器启动，监听端口 {serverPort}...")

# 启动检查线程
check_thread = threading.Thread(target=check_clients)
check_thread.daemon = True  # 设置为守护线程，这样主程序退出时线程也会退出
check_thread.start()

while True:
    try:
        message, address = serverSocket.recvfrom(1024)
        current_time = time.time()
        message = message.decode()
        
        # 解析消息
        _, sequence_number, send_time = message.split()
        send_time = float(send_time)
        
        # 计算延迟时间
        delay = current_time - send_time
        
        # 更新客户端最后一次心跳时间
        client_last_seen[address] = current_time
        
        print(f"收到来自 {address} 的心跳包 #{sequence_number}, 延迟: {delay:.3f}秒")
                
    except KeyboardInterrupt:
        print("\n服务器停止运行")
        serverSocket.close()
        break
    except Exception as e:
        print(f"发生错误: {e}")