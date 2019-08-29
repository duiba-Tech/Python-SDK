from urllib.parse import parse_qs, urlencode
from urllib.request import urlparse
import hashlib
import time

#兑吧sdk工具类对象
class CreditsTool:
    appKey = ''
    appSecret=''
    def __init__(self,appKey,appSecret):
        self.appKey=appKey
        self.appSecret=appSecret

    #Md5加密
    def get_md5_value(self,src):
        myMd5 = hashlib.md5()
        myMd5.update(src.encode("utf-8"))
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    #构建请求参数
    def bulid_params( self,uid, credits, **sets):
        params = {}
        params['appKey'] = self.appKey
        params['appSecret'] = self.appKey
        params['timestamp'] = int(time.time() * 1000)
        params['uid'] = uid
        params['credits'] = credits
        for key, value in sets.items():
            params[key] = value
        return params


    #签名
    def sign(self,params):
        '对参数进行签名验证'
        sign_str = ''
        keys = sorted(params.keys())
        for key in keys:
            if key != 'sign':
                sign_str = sign_str + str(params[key])
        sign = self.get_md5_value(sign_str)
        return sign

    #签名校验方法
    def signVerify(self, params):
        params['appSecret'] = self.appSecret
        if params['sign'] == self.sign(params):
            return True
        else:
            return False

    #构建兑吧请求方法
    def buildUrlWithSign(self,url, params):
        '拼装签名链接地址'
        if '?' in url and not url.endswith('?'):
            url = url + '&'
        elif '?' not in url:
            url = url + '?'
        params['appKey']=self.appKey
        params['appSecret']=self.appSecret
        if params.get('timestamp')==None:
            params['timestamp']=int(time.time()*10000)
        signstr = self.sign(params)
        #'将签名串放入列表中'
        params['sign'] = signstr
        #'拼接免登陆地址时候，移除appSecret'
        del params['appSecret']
        urlparam = urlencode(params)  # '对参数进行urlencode编码'
        return url + urlparam

    #构建扣积分请求解析
    def credits_consurme(self, request_params):
        if self.appKey != request_params['appKey']:
            raise Exception("appKey not match !")
        elif request_params["timestamp"] == '':
            raise Exception("timestamp can't be null ! ")
        elif self.signVerify(self.appSecret, request_params) == False:
            raise Exception("sign verify fail! ")
        else:
            return request_params

    #虚拟商品充值请求接口解析
    def credits_virtual(self, request_params):
        if self.appKey != request_params['appKey']:
            raise Exception("appKey not match !")
        elif request_params["timestamp"] == '':
            raise Exception("timestamp can't be null ! ")
        elif self.signVerify(self.appSecret, request_params) == False:
            raise Exception("sign verify fail! ")
        else:
            return request_params

    #扣积分兑换结果通知参数解析
    def credits_notify(self, request_params):
        if self.appKey != request_params['appKey']:
            raise Exception("appKey not match !")
        elif request_params["timestamp"] == '':
            raise Exception("timestamp can't be null ! ")
        elif self.signVerify(self.appSecret, request_params) == False:
            raise Exception("sign verify fail! ")
        else:
            return request_params

    # 加积分请求参数解析
    def add_credits(self, request_params):
        if self.appKey != request_params['appKey']:
            raise Exception("appKey not match !")
        elif request_params["timestamp"] == '':
            raise Exception("timestamp can't be null ! ")
        elif self.signVerify(self.appSecret, request_params) == False:
            raise Exception("sign verify fail! ")
        else:
            return request_params


