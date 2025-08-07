import requests
from common.logger import logger
import warnings
from urllib3.exceptions import InsecureRequestWarning

from config import TestConfig

#忽略HTTPS警告
warnings.simplefilter('ignore',InsecureRequestWarning)
# BASE_URL = "https://192.168.0.101/admin-api"
def login(mobile, code):
    #使用手机和万能验证码进行登录，获取Token
    login_url = f'{TestConfig.BASE_URL}/system/auth/sms-login'
    payload = {
        "mobile": mobile,
        "code": code,
    }
    # 创建headers并放入租户id
    headers = {
        'tenant-id': TestConfig.TENANT_ID,
        'Content-Type': 'application/json',
    }
    logger.info(f"开始使用手机号码和短信验证码登录，URL: {login_url},手机号为：{mobile}")
    try:
        response = requests.post(login_url, json=payload, headers=headers,verify=False)
        response_json = response.json()
        if(response_json.get("code") == 0):
            token = response_json.get("data", {}).get("accessToken")
            if(token):
                logger.info("登录成功，已经取到token")
                return token
            else:
                logger.error(f"登录接口返回成功，但在data中未找到accessToken: {response.json()}")
                return None
        else:
            logger.info(f"登录失败，响应: {response.json()}")
            return None
    except Exception as e:
        logger.error(f"登录请求发生异常: {e}", exc_info=True)
        return None

def get_sms_code(mobile):
    # 调用获取短信验证码的接口
    get_code_url = f"{TestConfig.BASE_URL}/system/auth/send-sms-code"
    payload = {
        "mobile": mobile,
        "scene": "21"  # 获取验证码通常需要一个场景值，请确认
    }
    headers = {
        'tenant-id': TestConfig.TENANT_ID,
    }
    logger.info(f"开始请求获取短信验证码，手机号: {mobile}")
    try:
        response = requests.post(get_code_url, json=payload, headers=headers, verify=False)
        if response.json().get("code") == 0:
            logger.info("成功触发服务器生成验证码状态。")
            return True
        else:
            logger.info(f"获取验证码接口调用失败: {response.json()}")
            return False
    except Exception as e:
        logger.error(f"获取验证码请求异常: {e}", exc_info=True)
        return False