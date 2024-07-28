import os
import sys
import json
import uuid

def is_vedio(name: str) -> bool:
    name = name.lower()
    name_list = [
        "mp4", "flv", "f4v", "webm", "rm", "rmvb", "wmv", "avi", 'asf', 'mpg', 'mpeg', 'mpe', 'ts', 'div', 'dv', 'divx', 'vob', 'dat', 'mkv', 'lavf', 'cpk', 'dirac', 'ram', 'qt', 'fli', 'flc', 'mod'
    ]
    for name_suffix in name_list:
        if name.endswith(name_suffix):
            return True
    return False

if __name__ == "__main__":
    target_dir = sys.argv[1]
    dir_names = os.listdir(target_dir)
    dir_names.sort(reverse = True)
    file_name = "md/" + str(uuid.uuid4()) + ".md"
    md_file = open(file_name, "w", encoding = "utf8")
    md_file.write("# {}\n\n".format(target_dir))
    for dir_name in dir_names:
        dir_path = os.path.join(target_dir, dir_name)
        if not os.path.isdir(dir_path):
            continue
        summary_json_path = os.path.join(dir_path, "summary.json")
        if not os.path.exists(summary_json_path):
            continue
        summary_json_file = open(summary_json_path, "rb")
        summary_json = json.loads(summary_json_file.read().decode("utf8"))
        summary_json_file.close()
        md_file.write("## {}\n\n".format(summary_json.get("name")))
        md_file.write("> **Author ID:** {}\n".format(str(summary_json.get("screen_name"))))
        md_file.write(">\n")
        md_file.write("> **Discription:** {}\n".format(str(summary_json.get("description"))))
        md_file.write(">\n")
        md_file.write("> **Create Time:** {}\n".format(str(summary_json.get("created_at"))))
        md_file.write(">\n")
        md_file.write("> [Twitter Link]({})\n\n".format(str(summary_json.get("url"))))
        
        full_text: str = summary_json.get("full_text")
        if full_text != None:
            full_text.replace("\n", "<br/>")
            md_file.write(full_text)
            md_file.write("\n\n")
        
        sub_dir_names = os.listdir(dir_path)
        medias_dict = dict()
        for sub_dir_name in sub_dir_names:
            if sub_dir_name.endswith("json") or sub_dir_name.endswith("txt"):
                continue
            prefix = sub_dir_name.split(".")[0]
            if is_vedio(sub_dir_name):
                medias_dict[prefix] = sub_dir_name
            elif medias_dict.get(prefix) == None:
                medias_dict[prefix] = sub_dir_name
        
        medias = list(medias_dict.values())
        medias.sort()
            
        for media in medias:
            if is_vedio(media):
                md_file.write('<video id="video" controls="" src="{}" preload="none">\n\n'.format(os.path.abspath(os.path.join(dir_path, media))))
            else:
                md_file.write("![{}]({})\n\n".format(media, os.path.abspath(os.path.join(dir_path, media))))
    print(os.path.abspath(file_name))
    md_file.close()
    