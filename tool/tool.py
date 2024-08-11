import copy
import json
import types
import hashlib


def cover(o1: dict, o2: dict) -> dict:
    """
    o1和o2是dict，用o2覆盖o1中的值

    对于o2和o1键相同且值均为dict类型的情况，递归调用cover处理

    Args:
        o1 (dict): 被覆盖的dict
        o2 (dict): 覆盖的dict
    """
    for key in o2:
        if type(o2.get(key)) == dict:
            if type(o1.get(key)) == dict:
                cover(o1[key], o2[key])
            else:
                o1[key] = {}
                cover(o1[key], o2[key])
        elif not isinstance(o2[key], types.ModuleType):
            # 这里一定要copy，否则如果o2[key]也是对象，o1[key]会直接指向o2[key]
            o1[key] = copy.deepcopy(o2[key])
        else:
            o1[key] = o2[key]
    return o1


def get_formatted_json_str(json_info) -> str:
    """获取格式化好的json转的str

    Args:
        json_info (any): json对象

    Returns:
        str: 格式化结果
    """
    return json.dumps(
        json_info, sort_keys=True, indent=4, separators=(", ", ": "), ensure_ascii=False
    )


def generate_md5_hash(data_bytes: bytes) -> str:
    # 创建一个md5 hash对象
    md5_hash = hashlib.md5()

    # 更新hash对象的数据
    md5_hash.update(data_bytes)

    # 获取十六进制形式的哈希值
    hex_digest = md5_hash.hexdigest()

    return hex_digest