import time
import paramiko

# 本地文件路径
local_file_path = "/Users/zhanglei/code/company/saas/saas-admin-api-integration/target/saas-admin-api-integration-1.0-SNAPSHOT.war"
# 服务器的路径
remote_dir_path = "/home/source/saas-admin-api-integration-1.0-SNAPSHOT.war"

# 服务器ip
ip = "10.10.100.8"
# 端口号
port = 22
# 用户名
username = "root"
# 密码
password = "Dw@0904"

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

def start (ssh):
    command = "nohup java -jar  /home/source/saas-admin-api-integration-1.0-SNAPSHOT.war --spring.profiles.active=DEV --server.port=10453 > /dev/null 2>&1 &"
    chan = ssh.invoke_shell()
    chan.send(command+"\n")
    time.sleep(3)


pid_command = "netstat -anp|grep 10453|awk '{print $7}'|cut -d/ -f1"
stdin, stdout, stderr  = ssh.exec_command(pid_command)
stdout.channel.recv_exit_status()
lines = stdout.readlines()

if lines:
    pid = lines[0]
    ssh.exec_command("kill -9 "+pid)
    start(ssh)
else:
    print(lines)
    start(ssh)

stdin, stdout, stderr = ssh.exec_command('tail /opt/logs/10453/applog/saas-admin-api_all_log.log')
while True:
    line = stdout.readline()
    if not line:
        break
    print(line, end="")

    if "JVM running for" in line:
        print("........发布成功........")
        break

ssh.close()



