import json

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from api_test.common.auto_test import *

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
from api_test.common.handleMysql import *
import traceback
from api_test.common.api_response import JsonResponse


class Timimg_list(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取定时任务的信息
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("pagesize"))
            page = int(request.GET.get("page", 1))
        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")
        name = request.GET.get("name")
        if name:
            sql = f'select a.id,a.name,Host_id,project_id,frequency,next_run_time,a.type FROM api_test_automationtesttask a   \
            INNER JOIN django_apscheduler_djangojob  b ON a.id=b.name where a.name like "%{name}%" '
        else:
            sql = f'select a.id,a.name,Host_id,project_id,frequency,next_run_time,a.type FROM api_test_automationtesttask a   \
                INNER JOIN django_apscheduler_djangojob  b ON a.id=b.name '
            print(sql)
        resultpage = select_sql(sql)
        paginator = Paginator(resultpage, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数
        startRow = (page - 1) * page_size
        if name:
            sql = f'select a.id,a.name,Host_id,project_id,frequency,next_run_time,a.type FROM api_test_automationtesttask a  INNER JOIN django_apscheduler_djangojob  b  \
            ON a.project_id=b.name where a.name like "%{name}%" limit {startRow},{page_size}'
        else:
            sql = f'''select a.id,a.name,Host_id,a.project_id,frequency,next_run_time,a.type,c.name as project_name,d.name as host_name FROM api_test_automationtesttask a  INNER JOIN django_apscheduler_djangojob  b ON a.project_id=b.name 
INNER JOIN api_test_project c on a.project_id=c.id 
INNER JOIN api_test_globalhost d on a.Host_id=d.id limit {startRow},{page_size}'''
        print(sql)
        result = select_sql(sql)
        print(result)
        list = []
        for row in result:
            dict = {}
            dict['id'] = row[0]
            dict['name'] = row[1]
            dict['Host_id'] = row[2]
            dict['project_id'] = row[3]
            dict['frequency'] = row[4]
            dict['next_run_time'] = str(row[5])[0:19]
            dict['type'] = str(row[6])
            dict['project_name'] = row[7]
            dict['host_name'] = row[8]
            # jsonArr = json.dumps(dict, ensure_ascii=False)
            list.append(dict)
        print(list)
        return JsonResponse(data={"data": list,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功")
