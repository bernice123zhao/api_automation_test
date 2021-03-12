import django
import sys
import os
import traceback
import jsonpath

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_automation_test.settings")
django.setup()
import json
import re
import operator
import requests
import simplejson
import random
from api_test.common.PublicVariableData import *
from django.core import serializers
from requests import ReadTimeout
from api_test.common.common import check_json, record_results
from api_test.serializers import AutomationCaseApiSerializer, AutomationParameterRawSerializer
from api_test.models import *
from api_test.common.custom_function import *

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


def txt_wrap_by(start_str, end, html):  # 截取两个字符串之间得值
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def test_api(host_id, case_id, project_id, _id):
    """
    执行接口测试
    :param host_id: 测试的host域名
    :param case_id: 测试用例ID
    :param _id:  用例下接口ID
    :param project_id: 所属项目
    :return:
    """
    host = GlobalHost.objects.get(id=host_id, project=project_id)
    print("host的取值：%s"%host)
    try:
        print("--------------取tokenData前")
        # TokenData = GlobalHost.objects.get(id=host_id)
        TokenData = GlobalHost.objects.get(id=host_id)
        print("--------------取tokenData后")
        print("TokenData的数据：%s"%TokenData)
        print("TokenData的类型：%s"%type(TokenData))
        print("TokenData的key:%s"%TokenData.key)
        print("TokenData的value:%s"%TokenData.value)

    except:
        print("----------TokenData赋值空步骤")
        TokenData = ' '  # 有存tokenData则取值，无则赋值空
    data = AutomationCaseApiSerializer(AutomationCaseApi.objects.get(id=_id, automationTestCase=case_id)).data
    http_type = data['httpType']
    request_type = data['requestType']
    address = host.host + data['apiAddress']
    # print(address)
    if 'getAuthorization' in address:
        address = '172.22.7.87:8020/mock' + data['apiAddress']
    if 'oatask.qa' in address:
        address = data['apiAddress']
    print(_id)
    print(AutomationHead.objects.filter(automationCaseApi=_id))
    # head={}
    head = json.loads(serializers.serialize('json', AutomationHead.objects.filter(automationCaseApi=_id)))
    header = {}
    request_parameter_type = data['requestParameterType']
    examine_type = data['examineType']
    http_code = data['httpCode']
    response_parameter_list = data['responseData']  # 校验数据
    if http_type == 'HTTP':
        url = 'http://' + address
    else:
        url = 'https://' + address
    # print(url)
    url_Sp = url.split('--')
    finnal_url = ''
    for i in url_Sp:
        if '|' in i:
            print(i)
            i = i.strip('/')
            if '/' in i:
                s = i.split('/')
                i = s[0]
                i2 = s[1]
            api_id = i.split('|')[0]
            Associatedpath = i.split('|')[1]
            param_data = eval(json.loads(serializers.serialize(
                'json',
                AutomationTestResult.objects.filter(automationCaseApi=api_id)))[0]['fields']["responseData"])
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
    # if '--'in url:
    #     print(url.split('--'))
    #     zuizhongurl=url.split('--')[0]
    #     value=url.split('--')[1]
    #     print(9887)
    #     print(value)
    #     #print(value)
    #     if '/' in value:
    #         value=value.split('/')
    #         value_s1='/'+value[1]
    #         value = value[0]
    #
    #     else:
    #         value_s1=''
    #     #print(value)
    #     api_id = value.split('|')[0]
    #     Associatedpath = value.split('|')[1]
    #     param_data = eval(json.loads(serializers.serialize(
    #         'json',
    #         AutomationTestResult.objects.filter(automationCaseApi=api_id)))[0]['fields'][
    #                           "responseData"])
    #     param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
    #     url=zuizhongurl+str(param_data)+value_s1
    #     #print('最终url')
    #     #print(url)
    if data['requestParameterType'] == 'form-data':
        parameter_list = json.loads(serializers.serialize('json',
                                                          AutomationParameter.objects.filter(automationCaseApi=_id)))
        parameter = {}
        # print(parameter_list)
        for i in parameter_list:
            key_ = i['fields']['name']
            value = i['fields']['value']
            if '$*' in value:  # 判断随机数
                value_spilt = value.split('$*')[0]
                ran = txt_wrap_by('$*', '*', value)
                try:
                    print(ran)
                    rang_value = eval(ran)
                    value = value_spilt + str(rang_value)
                except:
                    print(traceback.print_exc())
            try:
                if i['fields']['interrelate'] and i['fields']['parInterrelate'] == False:  # 判断是否响应关联
                    # print(type(value))
                    # print(value)
                    if '[' in value and '{' in value:
                        value = eval(value)
                        # print(value)
                        # print(type(value))
                        for i in range(len(value)):
                            # print(i)
                            for k, v in value[i].items():
                                if '|' in str(v):
                                    # print(v)
                                    api_id = v.split('|')[0]
                                    # print(api_id)
                                    Associatedpath = v.split('|')[1]
                                    try:
                                        param_data = eval(json.loads(serializers.serialize(
                                            'json',
                                            AutomationTestResult.objects.filter(automationCaseApi=api_id)))[0][
                                                              'fields'][
                                                              "responseData"])
                                        # print('关联得返回数据22')
                                        param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                                        # param_data = eval(f'{param_data}{Associatedpath}')
                                        # print('关联得返回数据99999992')
                                    except Exception as e:
                                        logging.exception(e)
                                        record_results(_id=_id, url=url, request_type=request_type, header=header,
                                                       parameter=parameter,
                                                       host=host.name,
                                                       status_code=http_code, examine_type=examine_type,
                                                       examine_data=response_parameter_list,
                                                       _result='ERROR', code="", response_data="关联有误！")
                                        return 'fail'
                                    value[i][k] = param_data
                                    # print(value)
                                    # print('找到变量改变了值')
                                    # print(k)
                                    # print(param_data)
                        parameter[key_] = value
                    else:
                        api_id = value.split('|')[0]
                        Associatedpath = value.split('|')[1]
                        # print(api_id)
                        try:
                            param_data = eval(json.loads(serializers.serialize(
                                'json',
                                AutomationTestResult.objects.filter(automationCaseApi=api_id)))[0]['fields'][
                                                  "responseData"])
                            # print('关联得返回数据22')
                            # param_data=json.dumps(param_data, ensure_ascii=False)
                            # param_data = json.loads(param_data)
                            # #print(param_data)
                            # #print(type(param_data))
                            # print(Associatedpath)
                            param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                            # param_data = eval(f'{param_data}{Associatedpath}')
                            # print('关联得返回数据99999992')
                            # print(param_data)
                        except Exception as e:
                            logging.exception(e)
                            record_results(_id=_id, url=url, request_type=request_type, header=header,
                                           parameter=parameter,
                                           host=host.name,
                                           status_code=http_code, examine_type=examine_type,
                                           examine_data=response_parameter_list,
                                           _result='ERROR', code="", response_data="关联有误！")
                            return 'fail'
                        parameter[key_] = param_data
                elif i['fields']['parInterrelate']:  # 参数关联
                    print('参数关联')
                    print(ParameterVariable.objects.get(id=value).value)
                    parameter[key_] = ParameterVariable.objects.get(id=value).value
                # elif '[' in value:
                #     value = eval(value)
                #     parameter[key_] = value
                elif i['fields']['_type'] == 'List':
                    parameter[key_] = eval(value)
                elif i['fields']['_type'] == 'Dict':
                    parameter[key_] = eval(value)
                elif i['fields']['_type'] == 'String':
                    parameter[key_] = str(value)
                elif i['fields']['_type'] == 'Int':
                    parameter[key_] = int(value)
                else:
                    parameter[key_] = value
                # elif i['fields']['_type']=='Bool':
                #     parameter[key_] = eval(value)
                dataVariable = {"automationTestCase": case_id, "automationCaseApi": _id, "name": key_,
                                "value": parameter[key_]}
                addParameVariable(dataVariable)
            except KeyError as e:
                logging.exception(e)
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               host=host.name,
                               status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                               _result='ERROR', code="", response_data="关联有误！")
                return 'fail'
        if data["formatRaw"]:
            request_parameter_type = "raw"

    else:
        parameter = AutomationParameterRawSerializer(AutomationParameterRaw.objects.filter(automationCaseApi=_id),
                                                     many=True).data

        if len(parameter) > 0:
            # print(parameter)
            if parameter[0]["data"]:
                # from collections import OrderedDict

                try:
                    # print(type(parameter[0]))
                    parameter = json.loads(parameter[0]["data"])
                    # parameter = eval(parameter[0]["data"])
                except Exception as e:
                    logging.exception(e)
                    record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                                   host=host.name,
                                   status_code=http_code, examine_type=examine_type,
                                   examine_data=response_parameter_list,
                                   _result='ERROR', code="", response_data="")
                    return 'fail'
            else:
                parameter = {}
        else:
            parameter = {}

    for i in head:
        key_ = i['fields']['name']
        value = i['fields']['value']
        # print('值')
        # print(value)
        # print(i)
        if i['fields']['interrelate']:
            try:
                api_id = value.split('|')[0]
                Associatedpath = value.split('|')[1]
                # print(api_id)
                try:
                    param_data = eval(json.loads(serializers.serialize(
                        'json',
                        AutomationTestResult.objects.filter(automationCaseApi=api_id)))[-1]['fields'][
                                          "responseData"])
                    # print('关联得返回数据')
                    param_data = jsonpath.jsonpath(param_data, expr=Associatedpath)[0]
                    # param_data = eval(f'{param_data}{Associatedpath}')
                    # print('关联得返回数据9999999')
                    # print(param_data)
                except Exception as e:
                    logging.exception(e)
                    record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                                   host=host.name,
                                   status_code=http_code, examine_type=examine_type,
                                   examine_data=response_parameter_list,
                                   _result='ERROR', code="", response_data="关联有误！")
                    return 'fail'
                header[key_] = param_data
            except Exception as e:
                logging.exception(e)
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               host=host.name,
                               status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                               _result='ERROR', code="", response_data="关联有误！")
                return 'fail'
        else:
            header[key_] = value

    # 处理header中token为None的情况
    try:
        if TokenData:
            if TokenData.key is None:
                pass
            else:
                header[TokenData.key] = TokenData.value
        else:
            pass
        if request_type == 'GET':
            if 'oatask.qa' in url:
                header = {}
                code, response_data, header_data, response_text = get(header, url, request_parameter_type, parameter)
            else:
                print("---------库里取得数据，重新拼接请求")
                code, response_data, header_data, response_text = get(header, url, request_parameter_type, parameter)
            if response_data == '':
                response_data = {"接口返回": "空"}
                response_text = {"接口返回": "空"}
        elif request_type == 'POST':
            code, response_data, header_data, response_text = post(header, url, request_parameter_type, parameter)
            if response_data == '':
                response_data = {"接口返回": "空"}
                response_text = {"接口返回": "空"}
            # print(response_data)
        elif request_type == 'PUT':
            code, response_data, header_data, response_text = put(header, url, request_parameter_type, parameter)
            if response_data == '':
                response_data = {"接口返回": "空"}
                response_text = {"接口返回": "空"}
        elif request_type == 'DELETE':
            code, response_data, header_data, response_text = delete(header, url, parameter)
            if response_data == '':
                response_data = {"接口返回": "空"}
                response_text = {"接口返回": "空"}
        else:
            return 'ERROR'
    except ReadTimeout:
        # print(traceback.#print_exc())
        logging.exception(ReadTimeout)
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter, host=host.name,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       _result='TimeOut', code="408", response_data="")
        return 'timeout'
    if examine_type == 'no_check':
        """
            不校验，直接返回false
        """
        # print('raw的参数')
        # print(parameter)
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter, host=host.name,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       _result='PASS', code=code, response_data=response_data)
        return 'success'

    elif examine_type == 'json':    # json校验 TODO
        if int(http_code) == code:
            if not response_parameter_list:
                response_parameter_list = "{}"
            try:
                logging.info(response_parameter_list)
                logging.info(response_data)
                result = check_json(json.loads(response_parameter_list), response_data)
                print("-----json校验后的结果：%s"%result)
            except Exception:
                logging.info(response_parameter_list)
                result = check_json(eval(
                    response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                    response_data)
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data)
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data)
            return result
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="JSON校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data)
            return 'fail'

    elif examine_type == 'only_check_status':
        """
            只校验响应状态码
        """
        if int(http_code) == code:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="校验HTTP状态", examine_data=response_parameter_list,
                           host=host.name, _result='PASS', code=code, response_data=response_data)
            return 'success'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="校验HTTP状态", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data)
            return 'fail'

    elif examine_type == 'entirely_check':  # 包含校验
        """
            转换后，类似字符串包含校验
            特殊字符：true，false，null转换为：True，False，None，判等
        """
        if int(http_code) == code:
            try:
                if str(response_parameter_list).replace(" ", "").replace("\n", "") in str(response_text).replace(" ",
                                                                                                                 "").replace(
                        "\n", ""):
                    result = 'success'
                    # print('正确')
                else:
                    result = False
            except Exception as e:
                logging.exception(e)
                result = operator.eq(eval(
                    response_parameter_list.replace('true', 'True').replace('false', 'False').replace("null", "None")),
                    response_data)
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="包含校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data)
                return 'success'
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="包含校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data)
                return 'fail'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="包含校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data)
            return 'fail'   #

    elif examine_type == 'Regular_check':   # TODO 输入框正则匹配
        """
            正则校验
        """
        if int(http_code) == code:
            try:
                logging.info(response_parameter_list)
                print("-----888正则响应校验的数据：%s"%response_parameter_list)
                print("api请求的数据：%s"%response_data)
                result = re.findall(response_parameter_list,
                                    json.dumps(response_data).encode('latin-1').decode('unicode_escape'))   # TODO latin-1的含义：ISO-8859-1的别名
                logging.info(result)
            except Exception as e:
                logging.exception(e)
                return "fail"
            if result:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                               host=host.name, _result='PASS', code=code, response_data=response_data)
                return 'success'
            else:
                record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                               status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                               host=host.name, _result='FAIL', code=code, response_data=response_data)
                return 'fail'
        else:
            record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                           status_code=http_code, examine_type="正则校验", examine_data=response_parameter_list,
                           host=host.name, _result='FAIL', code=code, response_data=response_data)
            return 'fail'

    else:
        record_results(_id=_id, url=url, request_type=request_type, header=header, parameter=parameter,
                       status_code=http_code, examine_type=examine_type, examine_data=response_parameter_list,
                       host=host.name, _result='FAIL', code=code, response_data=response_data)
        return 'fail'


def post(header, address, request_parameter_type, data):
    """
    post 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    print(address)
    print(data)
    print(header)
    response = requests.post(url=address, data=data, headers=header, timeout=80)
    try:
        return response.status_code, response.json(), response.headers, response.text
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except Exception as e:
        # print(traceback.#print_exc())
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers, response.text


def get(header, address, request_parameter_type, data):
    """
    get 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    print("-----get封装-------")
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    print("-----参数数据-------")
    print(f"address:{address} \n"
            f"data:{data} \n"
            f"header:{header} \n"
            )
    response = requests.get(url=address, params=data, headers=header, timeout=80)
    print("---------------get响应结果后-------------")
    if response.status_code == 301:
        response = requests.get(url=response.headers["location"])
    try:
        return response.status_code, response.json(), response.headers, response.text
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers, response.text


def put(header, address, request_parameter_type, data):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param request_parameter_type: 接口请求参数格式 （form-data, raw, Restful）
    :param data: 请求参数
    :return:
    """
    if request_parameter_type == 'raw':
        data = json.dumps(data)
    response = requests.put(url=address, data=data, headers=header, timeout=80)
    try:
        return response.status_code, response.json(), response.headers, response.text
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers, response.text


def delete(header, address, data):
    """
    put 请求
    :param header:  请求头
    :param address:  host地址
    :param data: 请求参数
    :return:
    """
    response = requests.delete(url=address, params=data, headers=header)
    try:
        return response.status_code, response.json(), response.headers, response.text
    except json.decoder.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except simplejson.errors.JSONDecodeError:
        return response.status_code, '', response.headers, response.text
    except Exception as e:
        logging.exception('ERROR')
        logging.error(e)
        return {}, {}, response.headers, response.text
