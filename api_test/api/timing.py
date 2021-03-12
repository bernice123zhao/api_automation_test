import json
from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from rest_framework.parsers import JSONParser
import os
import random
from api_test.common.auto_test import *
from api_test.models import *
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
import traceback


def add_timing_api(Host_id,project_id,type,parameters,name):
        """
        添加测试任务
        :param request:
        :return:
        """
        try:
            AutomationTestTask.objects.get(project_id=project_id)
            AutomationTestTask.objects.filter(project_id=project_id).update(project_id=project_id, Host_id=Host_id,
                                              type=type,frequency=parameters,name=name)  # update可多条
        except ObjectDoesNotExist:
            AutomationTestTask.objects.create(project_id=project_id, Host_id=Host_id,
                                              type=type,frequency=parameters,name=name)



def test_add_task(request):  # 添加定时任务
    data = json.loads(request.body.decode())
    project_id = data["project_id"]
    timingType = data["timingType"]
    parameters = data["parameters"]
    host_id = data["host_id"]
    name = data["name"]
    add_timing_api(Host_id=host_id,project_id=project_id,type=timingType,parameters=parameters,name=name)

    try:
        # 创建任务
        if timingType == 'timing':
            print(parameters)
            functionStr = f"scheduler.add_job(all_task_run, 'cron',{parameters},args=(project_id, host_id),  id=str(project_id))"
        else:
            functionStr = f"scheduler.add_job(all_task_run, 'interval',{parameters},args=(project_id, host_id),id=str(project_id))"
        print(eval(functionStr))
        #             scheduler.add_job(runtask, 'cron',hour=9, minute= 8, seconde=1, args=(taskid,task_type,reciveremail),id=str(taskid))
        # scheduler.add_job(runtask, "interval", seconds=3,args=[taskid,task_type])
        code = "999999"
        msg = "成功！"
    except Exception as e:
        print(traceback.format_exc())
        code = '999996'
        msg = traceback.format_exc()
    back = {
        'code': code,
        'message': msg
    }
    return JsonResponse(back)


def test(a):
    print('执行成功')
    print(a)
    pass




register_events(scheduler)
scheduler.start()
# 开启定时工作
# try:
#     # 实例化调度器
#     scheduler = BackgroundScheduler()
#     # 调度器使用DjangoJobStore()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     # 设置定时任务，选择方式为interval，时间间隔为10s
#     # 另一种方式为每天固定时间执行任务，对应代码为：
#     # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
#     @register_job(scheduler, "interval", seconds=10)
#     def my_job1():
#         # 这里写你要执行的任务
#         pass
#     register_events(scheduler)
#     scheduler.start()
#     print(scheduler.get_jobs())
# except Exception as e:
#     print(e)
#     # 有错误就停止定时器
#     scheduler.shutdown()
