# 可以在这里定义一些所有测试用例都能共享的“固定装置”，比如数据库连接，登录token等待
import pytest
from api.auth_api import login,get_sms_code
from common.logger import logger
from config import TestConfig


@pytest.fixture(scope="session")
def login_fixture():
    """
    这个专用的fixture,在整个测试会话中只执行一次
    它会完成登录并返回一个可用的Token
    :return:
    """
    logger.info("--- 开始执行登录操作 (Session级别Fixture) ---")
    # test_phone = "19981927939"
    # code = "666666"
    get_code_success = get_sms_code(TestConfig.mobile)
    assert get_code_success, "获取验证码接口调用失败，无法继续登录！"
    token = login(TestConfig.mobile,TestConfig.code)

    # 这里加一个断言非常重要，如果登录失败，所有使用该fixture的测试都会跳过
    assert token is not None,"登录失败，无法获取到Token，后续测试无法进行！"
    logger.info(f"--- 登录成功，Token已准备就绪 ---")
    return token
