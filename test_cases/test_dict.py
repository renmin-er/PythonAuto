import pytest
import allure
from api.dict_api import get_dict_data_list

@allure.feature("字典管理模块")
class TestDictData:
    @allure.story("获取字典列表")
    @allure.title("成功获取列举出所有字典数据")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_dict_data_list(self,login_fixture):
        """
        测试成功获取到所有的字典数据的场景
        :return:
        """
        token = login_fixture
        with allure.step("发送获取所有字典数据的请求"):
            response = get_dict_data_list(token)
        with allure.step("断言响应状态码为200"):
            assert  response.status_code == 200
        with allure.step("断言响应体中的code是否为0"):
            response_json = response.json()
            assert  response_json.get("code") == 0
            # 断言响应中的data不为空
            assert response_json.get("data") is not None
        # 其它断言.....


