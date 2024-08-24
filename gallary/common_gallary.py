from .gallary import Gallary
from tool.decorators import LoggerWrapper
from . import logger
from . import module_config
import os
from tqdm import tqdm
import uuid
import json
from io import TextIOWrapper
from configs.constants import COLORS


class CommonGallary(Gallary):
    @LoggerWrapper(logger, True)
    def generate(self, source_dir_list: list[str], target_dir: str, title: str) -> str:
        try:
            target_dir = os.path.abspath(target_dir)
            file_name = self.generate_file_name(target_dir)
            dir_path_list = self.get_dir_path_list(source_dir_list)
            self.write_info(dir_path_list, file_name, title)
            tqdm.write(f"{COLORS['orange']}Gallary saved at: {file_name}{COLORS['reset']}")
            self.after_open(file_name)
            return file_name
        except Exception as ex:
            logger.exception(ex)
            
            
    def after_open(self, file_name):
        try:
            gallary_open_with = module_config.get("gallary_open_with")
            if gallary_open_with != None:
                os.system(gallary_open_with.format(file_name))
        except Exception as ex:
            logger.exception(ex)
            
            
    def get_dir_path_list(self, source_dir_list: list[str]) -> list[str]:
        result = []
        for source_dir in source_dir_list:
            dir_names = os.listdir(source_dir)
            dir_names.sort(reverse = True)
            dir_path_list = [os.path.join(source_dir, dir_name) for dir_name in dir_names]
            result += dir_path_list
        return result


    def write_info(self, dir_path_list: list[str], file_name: str, title: str):
        with open(file_name, "w", encoding = "utf8") as md_file:
            md_file.write("# {}\n\n".format(title))
            with tqdm(total=len(dir_path_list), desc="Gallary generate progress", colour="red") as pbar:
                for dir_path in dir_path_list:
                    if not os.path.isdir(dir_path):
                        continue
                    self.write_entry_info(md_file, dir_path)
                    pbar.update(1)


    def write_entry_info(self, md_file: TextIOWrapper, dir_path: str):
        summary_json = self.get_summary_json(dir_path)
        
        self.write_content_info(md_file, summary_json)
                    
        self.write_media_info(md_file, dir_path)


    def write_media_info(self, md_file: TextIOWrapper, dir_path: str):
        sub_dir_names = os.listdir(dir_path)
        for sub_dir_name in sub_dir_names:
            if sub_dir_name.endswith(".json") or sub_dir_name.endswith(".txt"):
                continue
            if self.is_vedio(sub_dir_name):
                md_file.write('<video id="video" loop controls="" src="{}" preload="none">\n\n'.format(os.path.abspath(os.path.join(dir_path, sub_dir_name))))
            else:
                md_file.write("![{}]({})\n\n".format(sub_dir_name, os.path.abspath(os.path.join(dir_path, sub_dir_name))))


    def write_content_info(self, md_file: TextIOWrapper, summary_json: dict):
        result_json = summary_json.get("content_info", {}).get("result", {})
        full_text = result_json.get("twitter_info", {}).get("full_text")
        if full_text != None:
            md_file.write("## <font color='red'>\<{}\></font> {}\n\n".format(result_json.get("user_info", {}).get("name"), full_text.replace("\n", " ")))
        else:
            md_file.write("## <font color='red'>\<{}\></font>\n\n".format(result_json.get("user_info", {}).get("name")))
        md_file.write("> **Author ID:** {}\n".format(str(result_json.get("user_info", {}).get("screen_name"))))
        md_file.write(">\n")
        md_file.write("> **Discription:** {}\n".format(str(result_json.get("user_info", {}).get("description"))))
        md_file.write(">\n")
        md_file.write("> **Create Time:** {}\n".format(str(result_json.get("twitter_info", {}).get("created_at"))))
        md_file.write(">\n")
        md_file.write("> **Reply Count:** {}\n".format(str(result_json.get("twitter_info", {}).get("reply_count"))))
        md_file.write(">\n")
        tag_str = " ".join(["`{}`".format(x) for x in result_json.get("twitter_info", {}).get("tags")])
        
        if tag_str != "":
            md_file.write("> **Tags:** {}\n".format(tag_str))
            md_file.write(">\n")
        url = self.get_url(result_json)
        md_file.write("> [Twitter Link]({})\n\n".format(str(url)))

        # full_text已经写在标题上了，这里先不写了                    
        # if full_text != None:
        #     full_text.replace("\n", "<br/>")
        #     md_file.write(full_text)
        #     md_file.write("\n\n")


    def get_url(self, result_json):
        url = result_json.get("twitter_info", {}).get("url")
        if url == None or url == "":
            screen_name = result_json.get("user_info", {}).get("screen_name")
            rest_id = result_json.get("rest_id")
            if screen_name != None and rest_id != None:
                url = "https://x.com/{}/status/{}".format(screen_name, rest_id)
        return url


    def get_summary_json(self, dir_path: str) -> dict:
        summary_json_path = os.path.join(dir_path, "entry.json")
        if not os.path.isfile(summary_json_path):
            logger.error("[{}] is not existed".format(summary_json_path))
            return {}
        return self.get_file_json(summary_json_path)


    def get_file_json(self, summary_json_path: str) -> dict:
        try:
            with open(summary_json_path, "rb") as summary_json_file:
                summary_json = json.loads(summary_json_file.read().decode("utf8"))
                return summary_json
        except Exception as ex:
            logger.exception(ex)
        return {}


    def generate_file_name(self, target_dir: str) -> str:
        return os.path.abspath(os.path.join(target_dir, str(uuid.uuid4()) + ".md"))
    
    
    def is_vedio(self, name: str) -> bool:
        name = name.lower()
        name_list = [
            "mp4", "flv", "f4v", "webm", "rm", "rmvb", "wmv", "avi", 'asf', 'mpg', 'mpeg', 'mpe', 'ts', 'div', 'dv', 'divx', 'vob', 'dat', 'mkv', 'lavf', 'cpk', 'dirac', 'ram', 'qt', 'fli', 'flc', 'mod'
        ]
        for name_suffix in name_list:
            if name.endswith(name_suffix):
                return True
        return False