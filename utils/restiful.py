from django.http import JsonResponse


class HttpCode(object):
    methoderror = 405  # 请求方法错误
    servererror = 500  # 服务器错误
    ok = 200  # ok
    paramserror = 400  # 参数错误
    unauth = 401  # 没有授权


def req_result(code=HttpCode.ok, message="", data=None, kwargs=None):
    json_dict = {'code': code, 'message': message, 'data': data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)


def success(message='', data=None):
    return req_result(message=message, data=data)


def unauth(message='', data=None):
    return req_result(code=HttpCode.unauth, message=message, data=data)


def paramserror(message='', data=None):
    return req_result(code=HttpCode.paramserror, message=message, data=data)


def method_error(message='', data=''):
    return req_result(code=HttpCode.methoderror, message=message, data=data)


