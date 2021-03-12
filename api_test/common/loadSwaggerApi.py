import logging

import requests
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from api_test.common.common import record_dynamic
from api_test.models import Project, ApiInfo, ApiHead, ApiParameter, ApiParameterRaw, ApiResponse, ApiOperationHistory
from django.db import transaction
from api_test.models import *
from api_test.serializers import ApiInfoDeserializer, ApiHeadDeserializer, ApiParameterDeserializer, \
    ApiResponseDeserializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def swagger_api(url, project, user):
    """
    请求swagger地址，数据解析
    :param url: swagger地址
    :param project: 项目ID
    :param user: 用户model
    :return:
    """
    #print(url)
    req = requests.get(url)
    # #print (req.text)
    # data =req.text
    data = req.json()
    apis = data["paths"]
    try:
        params = data["definitions"]
    except KeyError:
        pass
    for api, m in apis.items():
        requestApi = {
            "project_id": project, "status": True, "mockStatus": "200", "code": "", "desc": "",
            "httpType": "HTTP", "responseList": []}
        requestApi["apiAddress"] = api
        for requestType, data in m.items():
            requestApi["requestType"] = requestType.upper()
            #print(requestApi["apiAddress"])
            #print(requestApi["requestType"])
            group=data["tags"][0]#分组

            try:
                requestApi["name"] = data["summary"]
            except KeyError:
                pass
            if len(data["consumes"])>0:
                try:
                    if len(data["consumes"])>0:
                        if data["consumes"][0] == "application/json-patch+json":
                            requestApi["requestParameterType"] = "raw"
                        else:
                            requestApi["requestParameterType"] = "raw"
                        requestApi["headDict"] = [{"name": "Content-Type", "value": data["consumes"][0]}]
                    else:
                        if data["produces"][0] == "application/json-patch+json":
                            requestApi["requestParameterType"] = "raw"
                        else:
                            requestApi["requestParameterType"] = "raw"
                        requestApi["headDict"] = [{"name": "Content-Type", "value": "application/json"}]
                except KeyError:
                    requestApi["requestParameterType"] = "form-data"
            else:
                requestApi["requestParameterType"] = "form-data"
            if len(data["parameters"])>0:
                for j in data["parameters"]:
                    # #print(j)
                    if j["in"] == "header":
                        requestApi["headDict"].append({"name": j["name"].title(), "value": "String"})
                    # try:
                    #     parameter = []
                    #     parameter.append({"name": j['name'], "value": j["type"], "_type": '1',
                    #                       "required": True, "restrict": "", "description": ""})
                    #     requestApi["requestList"] = parameter
                    # except:
                    #     import traceback
                    #     #print('参数')
                    #     #print(traceback.#print_exc())
                    #     pass
                    elif j["in"] == "body":
                        dto = j["schema"]["$ref"].replace('#/definitions/','')
                        #print('dto')
                        #print(dto)
                        try:
                            if requestApi["requestParameterType"] == "raw":
                                parameter = {}
                                for key, value in params[dto]["properties"].items():
                                    parameter[key] = value['type']
                                    requestApi["requestList"] = str(parameter)
                            else:
                                parameter = []
                                for key, value in params[dto]["properties"].items():
                                    parameter.append({"name": key, "value": value["type"], "_type": 'String',
                                                      "required": True, "restrict": "", "description": ""})
                                requestApi["requestList"] = parameter
                        except:
                            import traceback
                            #print('参数')
                            #print(traceback.#print_exc())
                            pass
                    elif j["in"] == "query":
                        parameter = []
                        if 'description' in j.keys():
                            description=j["description"]
                        else:
                            description=''
                        parameter.append({"name": j["name"], "value": j["type"], "_type": 'String',
                                              "required": j["required"], "restrict": "", "description": description})
                        requestApi["requestList"] = parameter
                    elif j["in"] == "path":
                        parameter = []
                        requestApi["requestList"] = parameter
                    #     parameter = []
                    #     parameter.append({"name": j["name"], "value": j["type"], "_type": 'String',
                    #                           "required": j["required"], "restrict": "", "description": "路径"})
                    #     requestApi["requestList"] = parameter
                    else:
                        parameter = []
                        requestApi["requestList"] = parameter
            else:
                parameter = []
                requestApi["requestList"] = parameter
            requestApi["userUpdate"] = user.id
            print(requestApi)
            result = add_swagger_api(requestApi, user,group)


def add_swagger_api(data, user,group):
    """
    swagger接口写入数据库
    :param data:  json数据
    :param user:  用户model
    :return:
    """
    try:
        obj = Project.objects.get(id=data["project_id"])
        #print(group)
        try:
            with transaction.atomic():  # 执行错误后，帮助事物回滚
                serialize = ApiInfoDeserializer(data=data)
                if serialize.is_valid():
                    serialize.save(project=obj)
                    api_id = serialize.data.get("id")
                    try:
                        obj = ApiGroupLevelFirst.objects.get(project_id=data["project_id"], name=group)
                        #print('分组id')
                        ApiInfo.objects.filter(id=api_id).update(apiGroupLevelFirst=obj.id)
                    except ObjectDoesNotExist:
                        #print('创建分组%')
                        #print(group)
                        obj=ApiGroupLevelFirst.objects.create(name=group, project_id=data["project_id"])
                        print('api_id')
                        print(api_id)
                        print(obj.id)
                        ApiInfo.objects.filter(id=api_id).update(apiGroupLevelFirst=obj.id)
                    # if len(data.get("headDict")):
                    #     for i in data["headDict"]:
                    #         if i.get("name"):
                    #             i["api"] = api_id
                    #             head_serialize = ApiHeadDeserializer(data=i)
                    #             if head_serialize.is_valid():
                    #                 head_serialize.save(api=ApiInfo.objects.get(id=api_id))
                    if data["requestParameterType"] == "form-data":
                        #print('开始存储form-data')
                        # #print(data)
                        if len(data.get("requestList")):
                            for i in data["requestList"]:
                                if i.get("name"):
                                    i["api"] = api_id
                                    param_serialize = ApiParameterDeserializer(data=i)
                                    if param_serialize.is_valid():
                                        param_serialize.save(api=ApiInfo.objects.get(id=api_id))
                                    else:
                                        pass
                                        print('失败')
                                        #print(param_serialize.errors)
                            #print('form-data存储完成')
                    else:
                        if data.get("requestList"):
                            ApiParameterRaw(api=ApiInfo.objects.get(id=api_id), data=str(data["requestList"]).replace("'", "\"")).save()
                        else:
                            ApiParameterRaw(api=ApiInfo.objects.get(id=api_id)).save()
                    if len(data.get("responseList")):
                        for i in data["responseList"]:
                            if i.get("name"):
                                i["api"] = api_id
                                response_serialize = ApiResponseDeserializer(data=i)
                                if response_serialize.is_valid():
                                    response_serialize.save(api=ApiInfo.objects.get(id=api_id))
                    record_dynamic(project=data["project_id"],
                                   _type="新增", operationObject="接口", user=user.pk,
                                   data="新增接口“%s”" % data["name"])
                    api_record = ApiOperationHistory(api=ApiInfo.objects.get(id=api_id),
                                                     user=User.objects.get(id=user.pk),
                                                     description="新增接口“%s”" % data["name"])
                    api_record.save()
        except Exception as e:
            import traceback
            #print(traceback.#print_exc())
            logging.exception(e)
            return False
    except ObjectDoesNotExist:
        return False
