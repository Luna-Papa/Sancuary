import datetime


def get_metric_date(period):
    """根据当前日期计算统计周期需要的日期值"""
    current_period = ''  # 统计周期
    if period == 'day':
        current_period = \
            (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # 获取昨天日期
    elif period == 'month':
        current_period = \
            (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m')  # 获取上个月月份
    elif period == 'year':
        current_period = (datetime.datetime.today().replace(month=1).replace(day=1) -
                          datetime.timedelta(days=1)).strftime('%Y')  # 获取去年年份
    end_date = datetime.datetime.today().replace(day=1).strftime('%Y-%m-%d')
    begin_date = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)) \
        .replace(day=1).strftime('%Y-%m-%d')
    return current_period, begin_date, end_date
