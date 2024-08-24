from .common_parser import CommonParser

class TweetedParser(CommonParser):
    def get_sub_item_entries(self, entry: dict) -> list:
        """获取entry的下级entry，回复信息的entry是在一个总entry[content][items]结构中的

        Args:
            entry (dict): entry

        Returns:
            list: 该entry的所有下级entry
        """
        # 如果下载一个用户所有推文，自己评论自己的会显示在原推文下面，自己对自己推文的评论也是这个结构，最后一个是本体，前面是回复信息，这种的处理下来就重复了，所以只取最后一个本体
        items = entry.get("content", {}).get("items")
        if items != None and isinstance(items, list):
            return [items[-1]]
        return None