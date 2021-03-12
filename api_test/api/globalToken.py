import logging
from crontab import CronTab
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from threading import Thread
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from api_test.common.getTokenAuthor import *
from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic
from api_test.models import *
from api_test.serializers import *
import traceback
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class AddToken(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    def post(self, request):
        # post请求的数据
        data = JSONParser().parse(request)
        project_id = data['project']
        key = data['key']
        value = data['value']
        # print('84848146516514')
        # print(name)
        try:
            GlobalToken.objects.filter(project=project_id).update(key=key, value=value)
            GlobalToken.objects.get(project=project_id)

            return JsonResponse(code="999997", msg="更新成功")
        except:
            print(traceback.print_exc())
            bs = GlobalTokenSerializer(data=data)
            if bs.is_valid():
                bs.save()  # create方法
                return JsonResponse(code="999999", msg="新增成功！")
            else:
                print(bs.errors)
                return JsonResponse(code="999996", msg="失败！")
class AddLoginToken(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    def post(self, request):
        """
        获取项目详情
        :param username:
        :param password:
        :param url:
        :return:
        """
        data = JSONParser().parse(request)
        project_id = data['project']
        username = data['username']
        password = data['password']
        url = data['url']
        try:
            GlobalToken.objects.filter(project=project_id).update(username=username, password=password,
                                                                  url=url)
            GlobalToken.objects.get(project=project_id)
            return JsonResponse(code="999999", msg="更新成功")
        except:
            print(99898)
            print(data)
            bs = GlobalTokenSerializer(data=data)
            if bs.is_valid():
                bs.save()  # create方法
                return JsonResponse(code="999999", msg="新增成功！")
            else:
                print(bs.errors)
                return JsonResponse(code="999996", msg="失败！")
class TokenList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取token列表
        :param request:
        :return:
        """
        project_id=request.GET.get("project_id")
        project_id=int(project_id)
        obm=GlobalToken.objects.filter(project_id=project_id)
        serialize = GlobalTokenSerializer(obm, many=True)
        return JsonResponse(data= serialize.data, code="999999", msg="成功")
