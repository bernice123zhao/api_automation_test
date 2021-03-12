import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from api_test.common.api_response import JsonResponse
from api_test.models import Project
from api_test.serializers import *
from api_test.common.common import record_dynamic
import traceback



def addParameVariable(data):
    """
    新增项目project_id,case_id,name,value
    :param request:
    :return:
    """
    print(data)
    Serializer = ParameterVariableSerializer(data=data)
    print(data["automationCaseApi"])
    try:
        obj=ParameterVariable.objects.get(name=data["name"],automationCaseApi_id=data["automationCaseApi"])
        print(obj.value)
        obj.value=data["value"]
        obj.save()
        print('uapdate成功')
        return 'uapdate成功'
    except :
        # print(traceback.print_exc())
        if Serializer.is_valid():
            Serializer.save()
            print('存储参数成功')
            return True
        else:
            print(Serializer.errors)
            return False

class ParameList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目列表
        :param request:
        :return:
        """
        CaseApi = request.GET.get("automationCaseApi")
        testCase = request.GET.get("automationTestCase")
        if CaseApi:
            obi = ParameterVariable.objects.filter(automationCaseApi_id=CaseApi,automationTestCase=testCase).order_by("id")
        else:
            obi = ParameterVariable.objects.filter(automationTestCase=testCase).order_by("id")
        serialize = ParameterListSerializer(obi, many=True)
        return JsonResponse(data=serialize.data
                                  , code="999999", msg="成功")
