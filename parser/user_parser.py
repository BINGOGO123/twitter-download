from .parser import Parser

class UserParser(Parser):
    def parse(self, response: dict) -> dict:
        """从用户response中获取用户信息

        Args:
            response (dict): 用户响应结果

        Returns:
            dict: 用户信息，格式如下：
            ```json
            {
                "name": "名称",
                "rest_id": "123",
                "screen_name": "唯一ID"
            }
            ```
        """
        user_info = {}
        if response.get("data") != None:
            if response.get("data").get("user_result_by_screen_name") != None:
                if response.get("data").get("user_result_by_screen_name").get("result") != None:
                    user_info["rest_id"] = response.get("data").get("user_result_by_screen_name").get("result").get("rest_id")
                    if response.get("data").get("user_result_by_screen_name").get("result").get("legacy") != None:
                        user_info["name"] = response.get("data").get("user_result_by_screen_name").get("result").get("legacy").get("name")
                        user_info["screen_name"] = response.get("data").get("user_result_by_screen_name").get("result").get("legacy").get("screen_name")
        return user_info
