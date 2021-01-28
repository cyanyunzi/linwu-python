import time
import paramiko

# 本地文件路径
local_file_path = "/Users/zhanglei/code/company/saas/saas-tenant-ws/saas-tenant-ws-service/target/saas-tenant-ws-service-1.0-SNAPSHOT.war"

# 服务器的路径
remote_dir_path = "/home/source/saas-tenant-ws-service-1.0-SNAPSHOT.war"

# 服务器ip
ip = "172.16.220.152"
# 端口号
port = 22
# 用户名
username = "root"
# 密码
password = "Homedo@yw110901"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, port, username, password)


try:
    sftp = ssh.open_sftp()
    sftp.put(local_file_path, remote_dir_path)
except FileNotFoundError as e:
    print(e)
    print("系统找不到指定文件" + local_file_path)
else:
    print("........文件上传成功.........")

def start ():
    command = "nohup java -jar  /home/source/saas-tenant-ws-service-1.0-SNAPSHOT.war --spring.profiles.active=DEV --server.port=10433 > /dev/null 2>&1 &"
    chan = ssh.invoke_shell()
    chan.send(command+"\n")
    time.sleep(3)


pid_command = "netstat -anp|grep 10433|awk '{print $7}'|cut -d/ -f1"
stdin, stdout, stderr  = ssh.exec_command(pid_command)
stdout.channel.recv_exit_status()
lines = stdout.readlines()
if lines:
    pid = lines[0]
    ssh.exec_command("kill -9 "+pid)
    start()
else:
    print(lines)
    start()

stdin, stdout, stderr = ssh.exec_command('tail -f /opt/logs/10433/applog/saas-tenant-ws_all_log.log')
while True:
    line = stdout.readline()
    if not line:
        break
    print(line, end="")

    if "JVM running for" in line:
        print("........发布成功........")
        break

ssh.close()



