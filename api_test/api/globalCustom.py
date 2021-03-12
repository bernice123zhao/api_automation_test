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
class GlobalCustom(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取自定义参数列表
        :param request:
        :return:
        """
        obm=PublicVariable.objects.all()
        serialize = PublicVariableSerializer(obm, many=True)
        return JsonResponse(data= serialize.data, code="999999", msg="成功")