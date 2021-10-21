import time
import ibm_db
from celery import shared_task
from .models import TaskList, StatusTypes


@shared_task(name='sjxf.data_push', queue='sjxf')
def data_push(ds_id, org_no, tb_name, table_id, task_id):
    from sjxf.utils.db2 import get_ssh_conn
    ssh = get_ssh_conn('ETL-Database')
    command = ''
    print("####提交远程脚本执行####")
    stdin, stdout, stderr = ssh.exec_command(command)
    ssh.close()
    print('####开始循环检测任务状态####')
    while True:
        print('####等待300s####')
        time.sleep(300)
        task_status = TaskList.objects.get(task_id=task_id).status
        if task_status not in [StatusTypes.status_success, StatusTypes.status_failed]:
            print('####任务未完成，继续等待####')
            continue
        else:
            print(f'####{task_id}下发任务已结束，状态为{task_status}。####')
            break
    print('####作业完成！####')
    return True


@shared_task()
def check_task_result():
    """检查数据下发任务状态"""
    # 只检查状态为已开始和等待中的任务
    tasks = TaskList.objects.filter(status__in=[StatusTypes.status_submit, StatusTypes.status_execute])
    conn = ibm_db.connect("hisdata", "db2inst", "db2inst")
    for task in tasks:
        sql = "SELECT STATUS FROM ARES.TASK_RESULT WHERE TASK_ID = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, task.task_id)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_tuple(stmt)
        try:
            if task.status != row[0]:
                # 更新本地库任务状态
                task.status = row[0]
                task.save()
            else:
                print("####任务状态未改变...####")
                continue
        except Exception as e:
            print(e)
