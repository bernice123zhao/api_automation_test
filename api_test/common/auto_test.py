import datetime
import django
import sys
import os
import pytz
import logging

from crontab import CronTab
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
import random
from django.http import JsonResponse
from api_test.common.common import record_dynamic
from api_test.models import *
from api_test.serializers import *
import traceback
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。
from api_test.common.getTokenAuthor import *

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_automation_test.settings")
django.setup()
from api_test.common.sendEmail import send_email
from api_test.common.auto_task_test import test_api
from api_test.models import AutomationCaseApi, AutomationTaskRunTime, AutomationTestCase, GlobalHost, Project

def all_task_run(project_id,host_id):
    # data = AutomationCaseApi.objects.filter(automationTestCase=sys.argv[1])
    tz = pytz.timezone('Asia/Shanghai')
    start_time = datetime.datetime.now(tz)
    format_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
    case = AutomationTestCase.objects.filter(project=project_id).order_by("id")
    host = GlobalHost.objects.get(id=host_id, project=project_id)
    _pass = 0
    fail = 0
    error = 0
    time_out = 0
    for j in case:
        data = AutomationCaseApi.objects.filter(automationTestCase=j.pk).order_by("exeSequence")
        print('i')
        for i in data:
            try:
                result = test_api(host=host, case_id=j.pk, _id=i.pk, time=format_start_time, project_id=project_id)
            except:
                result = 'timeout'
            if result == 'success':
                _pass = _pass + 1
            elif result == 'fail':
                fail = fail + 1
            elif result == 'ERROR':
                error = error + 1
            elif result == 'timeout':
                time_out = time_out + 1
    total = _pass + fail + error + time_out
    result_data = "Hi, all:\n    测试时间： %s\n" \
                  "    总执行测试接口数： %s:\n" \
                  "    成功： %s,  失败： %s, 执行错误： %s, 超时： %s\n" \
                  "    详情查看地址：http://website-test2.shenlanbao.com/#/projectReport/project=%s" % (start_time, total,
                                                                                            _pass, fail, error, time_out
                                                                                            , project_id)      # sys.argv[2] origin
    if total != _pass:
        if send_email(project_id, result_data):
            print("邮件发送成功")
        else:
            print("邮件发送失败")
    if total == _pass:      # debug 相等也发邮件
        if send_email(project_id, result_data):
            print("邮件发送成功")
        else:
            print("邮件发送失败")
    elapsed_time = (datetime.datetime.now(tz) - start_time).seconds
    AutomationTaskRunTime(project=Project.objects.get(id=project_id), startTime=format_start_time,
                          elapsedTime=elapsed_time, host=host.name).save()
    print('wanlewanle')
def automation_task(request):
    getTokenAuthor()
    project_id=request.GET.get("project_id")
    host_id = request.GET.get("host_id")
    print(project_id,host_id)
    all_task_run(project_id,host_id)
    return JsonResponse({"code": "999999", "msg": "执行成功"})


