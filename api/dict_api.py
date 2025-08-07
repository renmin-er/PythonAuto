import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning

from common.logger import logger
from config import TestConfig

# 当设置verify=False时，控制台会打印一个InsecureRequestWarning 警告，下面的代码可以禁用它。
warnings.simplefilter('ignore',InsecureRequestWarning)
# BASE_URL = 'https://192.168.0.101/admin-api'

# 封装一个获取字典列表的请求
# /system/dict-data/list-all-simple
def get_dict_data_list(token):
    url =  f'{TestConfig.BASE_URL}/system/dict-data/list-all-simple'
    headers = {
        "Authorization": f"Bearer {token}",
        'tenant-id': TestConfig.TENANT_ID  # <-- 3. 加入租户ID
    }
    #添加日志
    logger.info(f"开始请求获取字典列表数据，URL:{url}")

    try:
        response = requests.get(url,timeout=10,headers=headers,verify=False)   #设置10秒超时
        logger.info(f"请求成功，状态码：{response.status_code},data数据内容为：{response.json().get('data')}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"请求发生异常：{e}", exc_info=True)
        return None