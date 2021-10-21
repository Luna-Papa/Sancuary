import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='127.0.0.1', port=22, username='Athena', password='yygl@123')
stdin, stdout, stderr = client.exec_command('sh /home/db2inst1/sync.sh')
client.close()
