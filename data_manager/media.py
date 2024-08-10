from datetime import datetime


class Media:
    def __init__(self, **kwargs):
        self.media_url = kwargs.get("media_url", None)
        self.storage_path = kwargs.get("storage_path", None)
        self.suffix_type = kwargs.get("suffix_type", None)
        self.content_md5 = kwargs.get("content_md5", None)
        self.create_time = kwargs.get("create_time", None)
        self.lastchange_time = kwargs.get("lastchange_time", None)
        self.id = kwargs.get("id", None)

    def __str__(self):
        return (
            "{"
            + "{}:{},{}:{},{}:{},{}:{},{}:{},{}:{},{}:{}".format(
                "media_url",
                self.media_url,
                "storage_path",
                self.storage_path,
                "suffix_type",
                self.suffix_type,
                "content_md5",
                self.content_md5,
                "create_time",
                self.create_time,
                "lastchange_time",
                self.lastchange_time,
                "id",
                self.id
            )
            + "}"
        )
        
    
    def __repr__(self):
        return self.__str__()
    

    def set_media_url(self, media_url: str):
        self.media_url = media_url

    def get_media_url(self) -> str:
        return self.media_url

    def set_storage_path(self, storage_path: str):
        self.storage_path = storage_path

    def get_storage_path(self) -> str:
        return self.storage_path

    def set_suffix_type(self, suffix_type: str):
        self.suffix_type = suffix_type

    def get_suffix_type(self) -> str:
        return self.suffix_type

    def set_content_md5(self, content_md5: str):
        self.content_md5 = content_md5

    def get_content_md5(self) -> str:
        return self.content_md5

    def set_create_time(self, create_time: datetime):
        self.create_time = create_time

    def get_create_time(self) -> datetime:
        return self.create_time

    def set_lastchange_time(self, lastchange_time: datetime):
        self.lastchange_time = lastchange_time

    def get_lastchange_time(self) -> datetime:
        return self.lastchange_time

    def set_id(self, id: int):
        self.id = id

    def get_id(self) -> int:
        return self.id
