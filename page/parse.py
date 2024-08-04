

def get_entries_from_favorite_response(data: dict) -> list:
    """获取一条favorite response的所有entries

    Args:
        data (dict): favorite response

    Returns:
        list: 所有entries
    """
    instructions: list = data.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", [])
    return get_entries_from_instructions(instructions)


def get_entries_from_tweeted_response(data: dict) -> list:
    """获取一条user response的所有entries

    Args:
        data (dict): user response

    Returns:
        list: 所有entries
    """
    instructions: list = data.get("data", {}).get("user", {}).get("result", {}).get("timeline_v2", {}).get("timeline", {}).get("instructions", [])
    return get_entries_from_instructions(instructions)


def get_entries_from_twitter_response(data: dict) -> list:
    """获取一条twitter response中所有的entries

    Args:
        data (dict): twitter response

    Returns:
        list: 所有entries
    """
    instructions: list = data.get("data", {}).get("threaded_conversation_with_injections_v2", {}).get("instructions", [])
    return get_entries_from_instructions(instructions)


def get_entries_from_instructions(instructions: list) -> list:
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


def get_entry_from_entries_by_rest_id(entries: list, rest_id: str) -> dict:
    """从entries中获取entry_id符合指定rest_id的entry，如果找不到则返回None

    Args:
        entries (list): entries
        id (str): entry_id

    Returns:
        dict: 指定rest_id的entry
    """
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_id = entry.get("entryId")
        if isinstance(entry_id, str) and entry_id.endswith(rest_id):
            return entry
    return None


def get_entry_info_list_from_entries(entries: list) -> list:
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
        entry_info = get_entry_info_from_entry(entry)
        if entry_info != None:
            entry_info_list.append(entry_info)
    return entry_info_list


def get_entry_info_from_entry(entry: dict) -> dict:
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
    entry_info = {}
    # 以who-to-follow为开头的entry是推荐关注用户，这里排掉
    if entry.get("entryId", "").startswith("who-to-follow"):
        return None
    content = entry.get("content", {})
    entry_info["content_info"] = get_content_info_from_content(content)
    return entry_info


def get_content_info_from_content(content: dict) -> dict:
    """从content中获取content信息

    Args:
        content (dict): 入参

    Returns:
        dict: 信息
    """
    content_info = {}
    content_info["cursor"] = content.get("value")
    content_info["cursor_type"] = content.get("cursorType")
    content_info["result_list"] = []
    
    # 如果有items（twitter下面附带的回复信息）
    items = content.get("items", [])
    if isinstance(items, list) and len(items) > 0:
        for item in items:
            content_info["result_list"].append(get_result_info_from_content(item.get("item")))
    else:
        content_info["result_list"].append(get_result_info_from_content(content))
    return content_info

def get_result_info_from_content(content: dict) -> dict:
    """从content中获取resutl信息

    Args:
        content (dict): content

    Returns:
        dict: result
    """
    result = content.get("itemContent", {}).get("tweet_results", {}).get("result", {})
    retweeted_status_result = result.get("retweeted_status_result", {}).get("result")
    if retweeted_status_result != None:
        result = retweeted_status_result
    tweet = result.get("tweet")
    if tweet != None:
        result = tweet
    return get_result_info_from_result(result)


def get_result_info_from_result(result: dict) -> dict:
    """从result中获取需要的信息
    Args:
        result (dict): tw的result

    Returns:
        dict: 信息
    """
    result_info = {}
    result_info["type_name"] = result.get("__typename")
    result_info["rest_id"] = result.get("rest_id")
    result_info["user_info"] = get_user_info_from_core(result.get("core", {}))
    result_info["twitter_info"] = get_twitter_info_from_legacy(result.get("legacy", {}))
    result_info["tombstone_info"] = get_tombstone_info_from_tombstone(result.get("tombstone", {}))
    return result_info


def get_tombstone_info_from_tombstone(tombstone: dict) -> dict:
    """获取tombstone信息

    Args:
        tombstone (dict): tombstone

    Returns:
        dict: 信息
    """
    tombstone_info = {}
    tombstone_info["text"] = tombstone.get("text")
    return tombstone_info
    
def get_user_info_from_core(core: dict) -> dict:
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


def get_twitter_info_from_legacy(legacy: dict) -> dict:
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
    content_info["url"] = get_url_from_full_text(legacy.get("full_text"))
    entities = legacy.get("entities", {})
    hashtags = entities.get("hashtags", [])
    medias = entities.get("media", [])
    content_info["tags"] = [x.get("text") for x in hashtags if isinstance(x, dict)]
    content_info["medias"] = [get_media_info_from_media(x) for x in medias if isinstance(x, dict)]
    return content_info


def get_url_from_full_text(full_text: str) -> str:
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


def get_media_info_from_media(media: dict) -> dict:
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
    media_info["vedio_info"] = get_video_info_from_variants(variants)
    return media_info
    
    
def get_video_info_from_variants(variants: list) -> dict:
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


def get_user_info_from_user_response(response: dict) -> dict:
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