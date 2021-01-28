import paramiko

# 本地文件路径
local_file_path = "/Users/zhanglei/code/company/crm/crm-tools-ws/crm-tools-ws-service/target/crm-tools-ws-service-1.0.0-SNAPSHOT.war"
# 服务器的路径
remote_dir_path = "/home/source/crm-tools-ws-service-1.0.0-SNAPSHOT.war"

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

ssh.close()