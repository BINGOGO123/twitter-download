from .common_parser import CommonParser

class TwitterParser(CommonParser):
    def get_instructions_from_response(self, response: dict) -> list:
        return response.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [])
    
    
    def get_content_info_from_content(self, content: dict) -> dict:
        content_info = {}
        item_content = content.get("itemContent", {})
        content_info["cursor"] = item_content.get("value")
        content_info["cursor_type"] = item_content.get("cursorType")
        content_info["result"] = self.get_result_info_from_item_content(item_content)
        return content_info