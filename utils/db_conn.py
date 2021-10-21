import ibm_db
import MySQLdb
import psycopg2


def execute_sql(db_type, user, passwd, db_name, sql, ip='', port='', *date):
    real_sql_stmt = ''  # 实际执行SQL
    if '{begin_date}' in sql:
        real_sql_stmt = sql.format(begin_date=date[0], end_date=date[1])
    if db_type == 'DB2':
        conn = ibm_db.connect(db_name, user, passwd)  # DB2数据库需要本地编目
        stmt = ibm_db.exec_immediate(conn, real_sql_stmt)
        results = ibm_db.fetch_tuple(stmt)
        return results
    elif db_type == 'MySql':
        print("暂不支持")
    elif db_type == 'PostgreSQL':
        conn = psycopg2.connect(database=db_name, user=user, password=passwd,
                                host=ip, port=port)
        cur = conn.cursor()
        cur.execute(real_sql_stmt)
        results = cur.fetchall()
        if len(results) > 1:
            return results
        else:
            return results[0]
    elif db_type == 'Oracle':
        print("暂不支持")
