from .abstract_parser import AbstractParser
from abc import abstractmethod


class CommonParser(AbstractParser):
    
    def get_entries_from_instructions(self, instructions: list) -> list:
        """从instructions中获取entries

        Args:
            instructions (list): instructions

        Returns:
            list: entries
        """
        all_entries = []
        for instruction in instructions:
            if not isinstance(instruction, dict):
                continue
            entries = instruction.get("entries", [])
            all_entries += entries
        return all_entries
    
    
    @abstractmethod
    def get_instructions_from_response(self, response: dict) -> list:
        return response.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", [])
    
    
    def get_entries_from_response(self, response: dict) -> list:
        instructions = self.get_instructions_from_response(response)
        return self.get_entries_from_instructions(instructions)
    
    
    def get_entry_info_list_from_entries(self, entries: list) -> list:
        """获取所有entries的entry_info

        Args:
            entries (list): entries

        Returns:
            list: entry_info列表
        """
        entry_info_list = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_info_list += self.get_entry_info_list_from_entry(entry)
        return entry_info_list
    
    
    def get_entry_info_list_from_entry(self, entry: dict) -> list:
        # 如果有下级entry则所有使用所有下级entry的信息
        item_entries = self.get_sub_item_entries(entry)
        if isinstance(item_entries, list) and len(item_entries) > 0:
            return self.get_entry_info_list_from_entries(item_entries)
        
        entry_info = self.get_entry_info_from_entry(entry)
        if entry_info != None:
            return [entry_info]
        return []
    

    def get_sub_item_entries(self, entry: dict) -> list:
        """获取entry的下级entry，回复信息的entry是在一个总entry[content][items]结构中的

        Args:
            entry (dict): entry

        Returns:
            list: 该entry的所有下级entry
        """
        # 对于带有评论的推文，推文和评论都是在一个总的entry下面的的子entry，所以这里返回一个列表，包含评论自身和原推文
        # 如果下载指定推文，除了第一个是推文本身外（非这种items结构），下面所有的回复也都是这个结构，但是由于不会显示对回复的回复，所以这时候只会有一个item
        # 如果下载的是media，那么一开始的评论里面的media都是包在一个entry下面的一系列子entry
        # 如果下载一个用户所有推文，自己评论自己的会显示在原推文下面，自己对自己推文的评论也是这个结构，最后一个是本体，前面是回复信息
        return entry.get("content", {}).get("items")


    def get_entry_info_from_entry(self, entry: dict) -> dict:
        """从entry中获取entry_info

        Args:
            entry (dict): 入参entry

        Returns:
            dict: 信息，格式如下：
            ```json
            {
                "content_info": {
                    "result_list": [
                        {
                            "type_name": "Tweet",
                            "rest_id": "123",
                            "user_info": {
                                "type_name": "User",
                                "rest_id": "123",
                                "created_at": "创建时间",
                                "description": "作者的签名描述",
                                "location": "作者的位置描述",
                                "name": "作者名称",
                                "screen_name": "作者的screen_name"
                            },
                            "twitter_info": {
                                "created_at": "创建时间",
                                "full_text": "TW的全文内容",
                                "conversation_id_str": "所在twitter id",
                                "in_reply_to_status_id_str": "回复的id",
                                "reply_count": 1,
                                "tags": ["标签"],
                                "medias": [
                                    {
                                        "type": "类型",
                                        "url": "推文链接",
                                        "media_url_https": "图片链接",
                                        "vedio_info": {
                                            "content_type": "视频类型",
                                            "url": "视频链接"
                                        }
                                    }
                                ],
                                "tombstone_info": {
                                    "text": "信息"
                                }
                            }
                        }
                    ],
                    "cursor_type": "指针类型",
                    "cursor": "指针值"
                }
            }
            ```
            
        """
        # 以who-to-follow为开头的entry是推荐关注用户，这里排掉
        if entry.get("entryId", "").startswith("who-to-follow"):
            return None
        
        entry_info = {}
        entry_info["sort_index"] = entry.get("sortIndex")
        entry_info["entry_id"] = entry.get("entryId")
        content = entry.get("content")
        if content == None:
            content = entry.get("item", {})
        entry_info["content_info"] = self.get_content_info_from_content(content)
        return entry_info


    def get_content_info_from_content(self, content: dict) -> dict:
        """从content中获取content信息

        Args:
            content (dict): 入参

        Returns:
            dict: 信息
        """
        content_info = {}
        content_info["cursor"] = content.get("value")
        content_info["cursor_type"] = content.get("cursorType")
        content_info["result"] = self.get_result_info_from_item_content(content.get("itemContent", {}))
        return content_info


    def get_result_info_from_item_content(self, item_content: dict) -> dict:
        """从item_content中获取result信息

        Args:
            item_content (dict): item_content

        Returns:
            dict: result
        """
        result = item_content.get("tweet_results", {}).get("result", {})
        retweeted_status_result = result.get("legacy", {}).get("retweeted_status_result", {}).get("result")
        if retweeted_status_result != None:
            result = retweeted_status_result
        tweet = result.get("tweet")
        if tweet != None:
            result = tweet
        return self.get_result_info_from_result(result)


    def get_result_info_from_result(self, result: dict) -> dict:
        """从result中获取需要的信息
        Args:
            result (dict): tw的result

        Returns:
            dict: 信息
        """
        result_info = {}
        result_info["type_name"] = result.get("__typename")
        result_info["rest_id"] = result.get("rest_id")
        result_info["user_info"] = self.get_user_info_from_core(result.get("core", {}))
        result_info["twitter_info"] = self.get_twitter_info_from_legacy(result.get("legacy", {}))
        result_info["tombstone_info"] = self.get_tombstone_info_from_tombstone(result.get("tombstone", {}))
        return result_info


    def get_tombstone_info_from_tombstone(self, tombstone: dict) -> dict:
        """获取tombstone信息

        Args:
            tombstone (dict): tombstone

        Returns:
            dict: 信息
        """
        tombstone_info = {}
        tombstone_info["text"] = tombstone.get("text")
        return tombstone_info
        
    def get_user_info_from_core(self, core: dict) -> dict:
        """从core中获取用户信息

        Args:
            core (dict): core

        Returns:
            dict: 信息
        """
        user_info = {}
        result = core.get("user_results", {}).get("result", {})
        user_info["type_name"] = result.get("__typename")
        user_info["rest_id"] = result.get("rest_id")
        legacy = result.get("legacy", {})
        user_info["created_at"] = legacy.get("created_at")
        user_info["description"] = legacy.get("description")
        user_info["location"] = legacy.get("location")
        user_info["name"] = legacy.get("name")
        user_info["screen_name"] = legacy.get("screen_name")
        return user_info


    def get_twitter_info_from_legacy(self, legacy: dict) -> dict:
        """获取推文信息

        Args:
            legacy (dict): 入参

        Returns:
            dict: 信息
        """
        content_info = {}
        content_info["created_at"] =  legacy.get("created_at")
        content_info["full_text"] = legacy.get("full_text")
        content_info["conversation_id_str"] = legacy.get("conversation_id_str")
        content_info["in_reply_to_status_id_str"] = legacy.get("in_reply_to_status_id_str")
        content_info["reply_count"] = legacy.get("reply_count")
        content_info["url"] = self.get_url_from_full_text(legacy.get("full_text"))
        entities = legacy.get("entities", {})
        hashtags = entities.get("hashtags", [])
        medias = entities.get("media", [])
        content_info["tags"] = [x.get("text") for x in hashtags if isinstance(x, dict)]
        content_info["medias"] = [self.get_media_info_from_media(x) for x in medias if isinstance(x, dict)]
        return content_info


    def get_url_from_full_text(self, full_text: str) -> str:
        """从full_text中提取twitter的url，没有则返回None

        Args:
            full_text (str): 推特全文

        Returns:
            str: 推特链接
        """
        if full_text != None:
            last_word = full_text.split(" ")[-1].strip()
            if last_word.startswith("http"):
                return last_word
        return None


    def get_media_info_from_media(self, media: dict) -> dict:
        """获取媒体信息

        Args:
            media (dict): 入参

        Returns:
            dict: 信息
        """
        media_info = {}
        media_info["type"] = media["type"]
        media_info["url"] = media["url"]
        media_info["media_url_https"] = media["media_url_https"]
        variants = media.get("video_info", {}).get("variants", [])
        media_info["vedio_info"] = self.get_video_info_from_variants(variants)
        return media_info
        
        
    def get_video_info_from_variants(self, variants: list) -> dict:
        """获取视频信息

        Args:
            variants (list): 入参

        Returns:
            dict: 信息
        """
        vedio_info = {}
        if len(variants) >= 1:
            variant = variants[-1]
            vedio_info["content_type"] = variant["content_type"]
            vedio_info["url"] = variant["url"]
        return vedio_info