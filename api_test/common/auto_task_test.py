import django
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_automation_test.settings")
django.setup()
import jsonpath
import json
import logging
import re
import operator
from django.core import serializers
from requests import ReadTimeout
import random
from api_test.common.confighttp import get, post, put, delete
from api_test.common.common import check_json, record_auto_results
from api_test.models import AutomationCaseApi, AutomationParameter, AutomationHead, \
    AutomationParameterRaw, AutomationCaseTestResult
from api_test.serializers import AutomationCaseApiSerializer, AutomationParameterRawSerializer
from api_test.models import *
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。
import traceback
def txt_wrap_by(start_str, end, html):  # 截取两个字符串之间得值
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
def test_api(host, case_id, _id, time,project_id):
    """
    执行接口测试
    :param host: 测试的host域名
    :param case_id: 测试用例ID
    :param _id:  用例下接口ID
    :param time: 测试时间
    :return:
    """
    data = AutomationCaseApiSerializer(AutomationCaseApi.objects.get(id=_id, automationTestCase=case_id)).data
    TokenData = GlobalHost.objects.get(id=host.id)
    http_type = data['httpType']
    request_type = data['requestType']
    address = host.host + data['apiAddress']
    head = json.loads(serializers.serialize('json', AutomationHead.objects.filter(automationCaseApi=_id)))
    header = {}
    request_parameter_type = data['requestParameterType']
    examine_type = data['examineType']
    http_code = data['httpCode']
    response_parameter_list = data['responseData']
    if http_type == 'HTTP':
        url = 'http://'+address
    else:
        url = 'https://'+address
    url_Sp = url.split('--')
    finnal_url = ''
    print(url_Sp)
    for i in url_Sp:
        if '|' in i:
            print(i)
            i = i.strip('/')
            if '/' in i:#假如url关联xxx/3
                s = i.split('/')
                i = s[0]
                i2 = s[1]
            api_id = i.split('|')[0]
            Associatedpath = i.split('|')[1]
            param_data = eval(json.loads(serializers.serialize(
                'json',
                AutomationCaseTestResult.objects.filter(automationCaseApi=api_id).order_by('-id')))[0]['fields']["responseData"])
            print(Associatedpath)
            i = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
            print(i)
            i = str(i) + '/'
        try:
            finnal_url = finnal_url + i + i2
        except:
            finnal_url = finnal_url + i
    print(finnal_url[-1])
    if finnal_url[-1] == '/':
        finnal_url = finnal_url[:-1]
    url = finnal_url
    print(98564)
    print(finnal_url)
    if data['requestParameterType'] == 'form-data':
        parameter_list = json.loads(serializers.serialize('json',
                                                          AutomationParameter.objects.filter(automationCaseApi=_id)))
        parameter = {}
        print(parameter_list)
        for i in parameter_list:
            key_ = i['fields']['name']
            value = i['fields']['value']
            if '$*' in value:#判断随机数
                value_spilt=value.split('$*')[0]
                ran=txt_wrap_by('$*','*',value)
                try:
                    print('随机数')
                    print(ran)
                    rang_value=eval(ran)
                    value=value_spilt+str(rang_value)
                except:
                    print(traceback.print_exc())
                    print('随机数生成错误')
            try:
                if i['fields']['interrelate'] and i['fields']['parInterrelate']==False:
                    print(type(value))
                    print(value)
                    if '[' in value and '{' in value :
                        value=eval(value)
                        print(value)
                        print(type(value))
                        for i in range(len(value)):
                            print(i)
                            for k, v in value[i].items():
                               if '|' in str(v):
                                   print(v)
                                   api_id = v.split('|')[0]
                                   print(api_id)
                                   Associatedpath = v.split('|')[1]
                                   try:
                                       param_data = eval(json.loads(serializers.serialize(
                                           'json',
                                           AutomationCaseTestResult.objects.filter(automationCaseApi=api_id).order_by('-id')))[0]['fields'][
                                                             "responseData"])
                                       print('关联得返回数据22')
                                       param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                                       # param_data = eval(f'{param_data}{Associatedpath}')
                                       print('关联得返回数据99999992')
                                   except Exception as e:
                                       logging.exception(e)
                                       record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                                           _result='ERROR', code="", response_data="关联错误！", time=time,
                                                           responseHeader="{}")

                                       return 'fail'
                                   value[i][k] = param_data
                                   print(value)
                                   print('找到变量改变了值')
                                   print(k)
                                   print(param_data)
                        parameter[key_] = value
                    else:
                        api_id = value.split('|')[0]
                        Associatedpath = value.split('|')[1]
                        print(api_id)
                        try:
                            param_data = eval(json.loads(serializers.serialize(
                                'json',
                                AutomationCaseTestResult.objects.filter(automationCaseApi=api_id).order_by('-id')))[0]['fields'][
                                                  "responseData"])
                            print('关联得返回数据22')
                            # param_data=json.dumps(param_data, ensure_ascii=False)
                            # param_data = json.loads(param_data)
                            # print(param_data)
                            # print(type(param_data))
                            print(Associatedpath)
                            param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                            # param_data = eval(f'{param_data}{Associatedpath}')
                            print('关联得返回数据99999992')
                            print(param_data)
                        except Exception as e:
                            logging.exception(e)

                            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                                _result='ERROR', code="", response_data="", time=time,
                                                responseHeader="{}")
                            return 'fail'
                        parameter[key_] = param_data
                elif i['fields']['parInterrelate']:#参数关联
                    print('参数关联')
                    print(ParameterVariable.objects.get(id=value).value)
                    parameter[key_]=ParameterVariable.objects.get(id=value).value
                elif i['fields']['_type'] == 'List':
                    parameter[key_] = eval(value)
                elif i['fields']['_type'] == 'Dict':
                    parameter[key_] = eval(value)

                elif i['fields']['_type']=='String':
                    parameter[key_] = str(value)
                elif i['fields']['_type']=='Int':
                    parameter[key_] = int(value)
                else:
                    parameter[key_] = value

            except KeyError as e:
                logging.exception(e)
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='ERROR', code="", response_data="", time=time,
                                    responseHeader="{}")

                return 'fail'
        if data["formatRaw"]:
            request_parameter_type = "raw"
    else:
        parameter = AutomationParameterRawSerializer(AutomationParameterRaw.objects.filter(automationCaseApi=_id),
                                                     many=True).data
        print(parameter)
        if len(parameter)>0:
            print(parameter)
            if len(parameter[0]["data"]):
                try:
                    parameter = json.loads(parameter[0]["data"])
                except Exception:
                    record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                        _result='ERROR', code="", response_data="", time=time, responseHeader="{}")
                    return 'fail'
            else:
                parameter = []
        else:
            parameter = {}

    for i in head:
        key_ = i['fields']['name']
        value = i['fields']['value']
        if i['fields']['interrelate']:

            try:
                api_id = value.split('|')[0]
                Associatedpath=value.split('|')[1]
                print(api_id)
                try:
                    param_data = eval(json.loads(serializers.serialize(
                        'json',
                        AutomationCaseTestResult.objects.filter(automationCaseApi=api_id).order_by('-id')))[-1]['fields'][
                                          "responseData"])
                    print('关联得返回数据')
                    param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                    # param_data = eval(f'{param_data}{Associatedpath}')
                    print('关联得返回数据9999999')
                    print(param_data)
                except Exception as e:
                    record_auto_results(_id=_id, header=header, parameter=parameter, caseUrl=url,
                                        _result='ERROR', code="", response_data="关联错误！",
                                        time=time, responseHeader="{}")
                    return 'fail'

                header[key_] = param_data

            except Exception as e:
                logging.exception("ERROR")
                logging.error(e)
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='ERROR', code="", response_data="", time=time, responseHeader="{}")
                return 'fail'
        else:
            header[key_] = value

    # header["Content-Length"] = '%s' % len(str(parameter))==长度
    header[TokenData.key] = TokenData.value
    try:
        if request_type == 'GET':
            if '/api/BasicEmployeeGroup/List' in url:
                print(6544)
                print(url)
                print(header)
                print(request_parameter_type)
                print(parameter)
            code, response_data, header_data,response_text = get(header, url, request_parameter_type, parameter)
        elif request_type == 'POST':
            code, response_data, header_data,response_text = post(header, url, request_parameter_type, parameter)
        elif request_type == 'PUT':
            code, response_data, header_data,response_text = put(header, url, request_parameter_type, parameter)
        elif request_type == 'DELETE':
            code, response_data, header_data,response_text = delete(header, url, parameter)
        else:
            return 'ERROR'
    except ReadTimeout:
        record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                            _result='TimeOut', code="", response_data="", time=time, responseHeader="{}")
        return 'timeout'
    if examine_type == 'no_check':
        record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                            _result='PASS', code=code, response_data=response_data,
                            time=time, responseHeader=header_data)
        return 'success'

    elif examine_type == 'json':
        if int(http_code) == code:
            # try:
            #     result = check_json(eval(response_parameter_list), response_data)
            # except:
            #     result = check_json(eval(response_parameter_list.replace('true', 'True').replace('false', 'False')),
            #                         response_data)
            if not response_parameter_list:
                response_parameter_list = "{}"
            try:
                logging.info(response_parameter_list)
                logging.info(response_data)
                result = check_json(json.loads(response_parameter_list), response_data)
            except Exception:
                logging.info(response_parameter_list)
                result = check_json(eval(response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")), response_data)
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
            return result
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'only_check_status':
        if int(http_code) == code:
            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                _result='PASS', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'success'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'entirely_check':
        if int(http_code) == code:
            try:
                if str(response_parameter_list).replace(" ", "").replace("\n", "") in str(response_text).replace(" ", "").replace("\n", ""):
                    result='success'
                    #print('正确')
                else:
                    result = False
            except:
                result = operator.eq(eval(response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                                     response_data)
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'success'
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'fail'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    elif examine_type == 'Regular_check':
        if int(http_code) == code:
            try:
                # result = operator.eq(json.loads(response_parameter_list), response_data)
                print('校验判断1')
                print(response_parameter_list)
                print(response_data)
                if str(response_parameter_list) in str(response_data).replace("'", '"'):
                    result='success'
                    print('正确')
                else:
                    result = False
            except Exception as e:
                logging.exception(e)
                return "fail"
            if result:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='PASS', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'success'
            else:
                record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                    _result='FAIL', code=code, response_data=response_data,
                                    time=time, responseHeader=header_data)
                return 'fail'
        else:
            record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                                _result='FAIL', code=code, response_data=response_data,
                                time=time, responseHeader=header_data)
            return 'fail'

    else:
        record_auto_results(_id=_id, header=header, parameter=parameter,caseUrl=url,
                            _result='FAIL', code=code, response_data=response_data,
                            time=time, responseHeader=header_data)
        return 'fail'
