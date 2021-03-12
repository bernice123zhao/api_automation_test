import logging
import pymysql
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


class AddDataBase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    def post(self, request):
        # post请求的数据
        data = JSONParser().parse(request)
        name = data['name']
        print(99)
        print(data)
        try:
            obj = Project.objects.get(id=data["project_id"])
            DataBase.objects.get(name=name)
            return JsonResponse(code="999997", msg="名称重复")
        except:
            print(traceback.print_exc())
            bs = DataBaseSerializer(data=data)
            if bs.is_valid():
                bs.save(project=obj)  # create方法
                return JsonResponse(code="999999", msg="新增成功！")
            else:
                print(bs.errors)
                return JsonResponse(code="999996", msg="失败！",data=bs.errors)
class DataBaseList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取数据库连接信息
        :param request:
        :return:
        """
        name = request.GET.get('name')
        project_id = request.GET.get('project_id')
        if name:
            obm = DataBase.objects.filter(name=name).order_by("id")
        else:
            obm = DataBase.objects.filter(project_id=project_id).order_by("id")
        serialize = DataBaseSerializer(obm, many=True)
        return JsonResponse(data= serialize.data, code="999999", msg="成功")


class UpdateDataBase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()


    def post(self, request):
        """
        修改数据库信息
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        try:
            obi = DataBase.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return JsonResponse(code="999992", msg="host不存在！")
        name = DataBase.objects.filter(name=data["name"]).exclude(id=data["id"])
        if len(name):
            return JsonResponse(code="999997", msg="存在相同名称！")
        else:
            serializer = DataBaseSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 外键project_id
                    serializer.update(instance=obi, validated_data=data)
                    # 记录动态
                    record_dynamic(project=data["project_id"],
                                   _type="更新", operationObject="数据库信息", user=request.user.pk, data=data["name"])
                    return JsonResponse(code="999999", msg="成功！")
                return JsonResponse(code="999998", msg="失败！")


class DelDataBase(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()


    def post(self, request):
        """
        删除数据库信息
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        try:
            DataBase.objects.filter(id=data["id"]).delete()
            return JsonResponse(code="999999", msg="成功！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")

class  TestConnection(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def runData(self,host,user,passwd,name):  # 查询
        conn = pymysql.connect(host=host, port=3306, user=user, passwd=passwd, db=name, charset='utf8')
        cur = conn.cursor()
        # 关闭数据库连接
        cur.close()
        conn.close()
        return True
    def get(self, request):
        """
        测试数据库是否连接成功
        :param request:
        :return:
        """
        id = request.GET.get('id')
        obm = DataBase.objects.filter(id=id).values()[0]
        print(obm)
        try:
            self.runData(obm["host"], obm["user"], obm["passwd"], obm["dataname"])
            return JsonResponse( code="999999", msg="成功")
        except:
            return JsonResponse( code="999996", msg="连接失败，请检查信息!")
