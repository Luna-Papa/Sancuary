import configparser
import os
import pathlib
from Sanctuary.settings import BASE_DIR
import ibm_db_dbi
import paramiko


def get_db_conn(db):
    cf = configparser.ConfigParser()
    cf.read(BASE_DIR / 'sjxf' / 'utils' / 'dbconf.ini')
    host = cf.get(db, "host")
    database = cf.get(db, "db")
    port = cf.get(db, "port")
    user = cf.get(db, "user")
    password = cf.get(db, "password")
    # 生成数据库连接配置
    conn = ibm_db_dbi.connect(f"PORT={port};PROTOCOL=TCPIP;", host=f"{host}", user=f"{user}",
                              password=f"{password}", database=f"{database}")
    conn.set_autocommit(True)
    curr = conn.cursor()
    return curr  # 返回游标


def get_sql_stmt(table):
    cf = configparser.ConfigParser()
    cf.read(BASE_DIR / 'sjxf' / 'utils' / 'sql_stmt.ini')
    stmt = cf.get(table, "SQL")
    return stmt


def get_ssh_conn(db):
    cf = configparser.ConfigParser()
    cf.read(BASE_DIR / 'sjxf' / 'utils' / 'dbconf.ini')
    # secs = cf.sections()
    host = cf.get(db, "host")
    port = 22
    user = cf.get(db, "user")
    password = cf.get(db, "password")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=user, password=password)
    return ssh  # 返回SSH通道
