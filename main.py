import requests
import uuid
import hashlib
import os
import logging
import os
import datetime
import shutil
import time
import sys
import json
from configs.config import headers

__target = "./target/"
__map_relation = "map_relation.txt"
__output_file_dir = "./output/"

# 起始时间
file_name_start = time.time()

# 初始化日志对象
def initialLogger(logger, name, logs_dir, logger_level, file_level, stream_level):
  # 如果不存在logs文件夹则创建
  if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
  handler1 = logging.FileHandler(os.path.join(logs_dir, name + "." + str(datetime.date.today()) + ".log"),"a",encoding="utf8")
  handler2 = logging.StreamHandler()
  formatter1 = logging.Formatter(fmt="%(asctime)s [%(levelname)s] [%(lineno)d] [%(funcName)s] >> %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
  formatter2 = logging.Formatter(fmt = "[%(levelname)s] >> %(message)s")
  handler1.setFormatter(formatter1)
  handler2.setFormatter(formatter2)
  handler1.setLevel(file_level)
  handler2.setLevel(stream_level)
  logger.setLevel(logger_level)
  logger.addHandler(handler1)
  logger.addHandler(handler2)

module_name = "tw_downloader"
logger = logging.getLogger(module_name)
initialLogger(logger, module_name, "logs/", logging.DEBUG, logging.DEBUG, logging.INFO)


# 从TW返回的内容提取有用的信息
{
    "name": "作者名称",
    "screen_name": "作者的ID",
    "create_at": "创建时间",
    "description": "作者的签名描述",
    "url": "TW的url链接",
    "full_text": "TW的全文内容",
    "cursor": "指针",
    "cursor_type": "指针类型",
    "medias": [
        {
            "media_url_https": "图片url地址",
            "variant_url": "视频地址",
            "variant_content_type": "视频类型"
        }
    ]
}
def get_tw_info(data: dict) -> list:
    result = []
    try:
        entities = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][-1]["entries"]
        
        for entity in entities:
            tw_info = {}
            try:
                try:
                    core_legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["retweeted_status_result"]["result"]["core"]["user_results"]["result"]["legacy"]
                    if core_legacy == None:
                        core_legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]
                    if core_legacy == None:
                        core_legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["core"]["user_results"]["result"]["legacy"]
                except:
                    logger.debug("no retweeted_status_result.result.core.user_results.result.legacy")
                    try:
                        core_legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]
                    except:
                        logger.debug("no result.core.user_results.result.legacy")
                        core_legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["core"]["user_results"]["result"]["legacy"]
                tw_info["name"] = core_legacy.get("name")
                tw_info["screen_name"] = core_legacy.get("screen_name")
                tw_info["created_at"] = core_legacy.get("created_at")
                tw_info["description"] = core_legacy.get("description")
            except Exception as ex:
                logger.debug(ex)
                logger.debug("core_legacy abnormal")

            try:
                try:
                    legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["retweeted_status_result"]["result"]["legacy"]
                    if legacy == None:
                        legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                    if legacy == None:
                        legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["legacy"]
                except:
                    logger.debug("no retweeted_status_result.result.legacy")
                    try:
                        legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                    except:
                        logger.debug("no result.legacy")
                        legacy = entity["content"]["itemContent"]["tweet_results"]["result"]["tweet"]["legacy"]
                full_text = legacy.get("full_text")
                tw_info["full_text"] = legacy.get("full_text")
                if full_text != None:
                    last_word = full_text.split(" ")[-1].strip()
                    if last_word.startswith("http"):
                        tw_info["url"] = last_word
                try:
                    medias = legacy["entities"]["media"]
                    tw_info["medias"] = []
                    for media in medias:
                        tw_info_media = {}
                        tw_info_media["media_url_https"] = media.get("media_url_https")
                        tw_info_media["url"] = media.get("url")
                        if tw_info.get("url") == None or tw_info.get("url") == "":
                            tw_info["url"] = media.get("url")
                        try:
                            variant = media["video_info"]["variants"][-1]
                            tw_info_media["variant_content_type"] = variant.get("content_type")
                            tw_info_media["variant_url"] = variant.get("url")
                        except Exception as ex:
                            logger.debug(ex)
                            logger.debug("variant abnormal")
                        tw_info["medias"].append(tw_info_media)
                except Exception as ex:
                    logger.debug(ex)
                    logger.debug("medias abnormal")
            except Exception as ex:
                logger.debug(ex)
                logger.debug("legacy abnormal")
            
            try:
                content = entity["content"]
                tw_info["cursor"] = content.get("value")
                tw_info["cursor_type"] = content.get("cursorType")
            except Exception as ex:
                logger.debug(ex)
                logger.debug("content abnormal")

            result.append(tw_info)
    except Exception as ex:
        logger.debug(ex)
        logger.debug("entities abnormal")
    return result

# 获取一个用户推文信息
def get_data(url_prefix, url_suffix, existed_data: dict, scan_all, limited_count = 999999999):
    s = requests.session()

    next_url = url_prefix + url_suffix
    all_info = []
    round = 1
    logger.info("Start download twitter records")
    while next_url != None and next_url != "":
        logger.info("Round: {}, present count of all_info is {}".format(round, (len(all_info))))
        round += 1
        # 请求获取response
        response = s.get(next_url, headers = headers)
        # 解析为json格式响应内容
        json_data = response.json()
        # 从json格式的响应内容中提取信息
        tw_info = get_tw_info(json_data)
        # 获取下一页的请求url
        next_url = get_next_page_url(url_prefix, url_suffix, tw_info)
        # 获取本页的信息
        tw_info = tw_info[:-2]
        # 打印本页所有信息数量
        logger.info("Current cycle count of twitter info is {}".format(len(tw_info)))
        # 有效的信息，必须有twitter url才行，最后两个是指针，丢弃
        valid_tw_info = [x for x in tw_info if x.get("url") != None and x.get("url") != ""]
        logger.info("Valid count of twitter info is {}".format(len(valid_tw_info)))
        # 没有信息则终止
        if len(valid_tw_info) == 0:
            break
        # 剔除掉已经存在的信息
        new_favorite_info = []
        for one_info in valid_tw_info:
            url = one_info.get("url")
            if url not in existed_data:
                new_favorite_info.append(one_info)
        # 打印本轮最终的有效信息
        logger.info("Final count without repeated of twitter count is {}".format(len(new_favorite_info)))
        # 如果没有新增内容，则终止，如果是扫描全部信息，则不终止
        if not scan_all and len(new_favorite_info) == 0:
            break
        # 增加本次新增的信息
        all_info += new_favorite_info
        # 信息上限
        if len(all_info) >= limited_count:
            break
    logger.info("End download twitter records")
    return all_info

# 获取下一页的url
def get_next_page_url(url_prefix, url_suffix, tw_info):
    try:
        cursor = tw_info[-1]["cursor"]
        next_url = url_prefix + '"cursor":"{}",'.format(cursor) + url_suffix
    except:
        next_url = None
    return next_url
  
# 获取md5加密结果
def get_md5(content):
    return hashlib.md5(content.encode()).hexdigest()
      
# 将所有TW信息保存到指定的目录下
def save_all_data(all_info, target_folder_path, map_relation_path):
    # 获取已经保存的TW信息的存储位置
    saved_tw_location_info: dict = get_all_saved_tw_location(map_relation_path)
    new_tw_info = []
    total_info_count = len(all_info)
    logger.info("Start download twitter information")
    for i in range(len(all_info)):
        # 获取下一个目录名称
        folder_name = get_next_folder_name(target_folder_path, i)
        logger.info("Present schedule: {}/{}, target name: {}".format(i + 1, total_info_count, folder_name))
        # 保存一条TW信息
        save_one_data(all_info[i], saved_tw_location_info, folder_name, new_tw_info)
    logger.info("End download twitter information")
    # 备份
    backup(map_relation_path)
    # 更新已经保存的TW信息的存储位置
    update_all_saved_tw_location(map_relation_path, saved_tw_location_info)
    # 备份
    backup(os.path.join(target_folder_path, __map_relation))
    # 往对应目录下写入新的数据记录
    add_new_data(target_folder_path, new_tw_info)

# 往对应目录下写入新的数据记录
def add_new_data(target_folder_path, new_tw_info):
    if len(new_tw_info) <= 0:
        return
    new_data = ("\n".join(new_tw_info) + "\n").encode("utf8")
    folder_name = os.path.join(target_folder_path, __map_relation)
    old_data = None
    if os.path.exists(folder_name):
        f = open(folder_name, "rb")
        old_data = f.read()
        f.close()
    f = open(folder_name, "wb")
    f.write(new_data)
    if old_data != None:
        f.write(old_data)
    f.close()

# 获取下一个目录名称
def get_next_folder_name(target_folder_path, i):
    counter = 1000000000
    folder_name = os.path.join(target_folder_path, "{}_{}".format(str(int(round(file_name_start * 1000))), str(counter - i).zfill(10)))
    return os.path.abspath(folder_name)

# 更新已经保存的TW信息的存储位置
def update_all_saved_tw_location(map_relation_path, saved_tw_location_info):
    map_relation = open(map_relation_path, "w", encoding = "utf8")
    for key in saved_tw_location_info:
        map_relation.write("{},{}\n".format(key, saved_tw_location_info.get(key)))
    map_relation.close()

# 备份文件信息
def backup(file_name):
    if not os.path.exists(file_name):
        return
    f = open(file_name, "rb")
    f_backup = open(file_name + ".backup", "wb")
    f_backup.write(f.read())
    f.close()
    f_backup.close()

# 获取已经保存的TW信息的存储位置
def get_all_saved_tw_location(map_relation_path): 
    if not os.path.exists(map_relation_path):
        return dict()
    map_relation = open(map_relation_path, "r", encoding = "utf8")
    all_lines = map_relation.readlines()
    result = dict()
    for line in all_lines:
        data = line.strip().split(",")
        result[data[0]] = data[1]
    map_relation.close()
    return result

# 保存一条TW信息
def save_one_data(info, saved_tw_location_info, folder_name, new_tw_info):
    try:
        url = info.get("url")
        # 如果该信息已经存在，则直接复制到指定目录下
        location = saved_tw_location_info.get(url)
        if location != None and os.path.exists(location):
            # 复制粘贴
            shutil.copytree(location, folder_name)
            # 新增项
            new_tw_info.append("{},{}".format(url, folder_name))
            logger.info("Saved tw info from existed info")
            return
        # 创建目录
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        # 写入媒体信息
        write_medias_info(info, folder_name)
        # 写入总结信息
        write_summary_info(info, os.path.join(folder_name, "summary.txt"))
        # 写入总结信息，json内容
        write_summary_json(info, os.path.join(folder_name, "summary.json"))
        logger.info("Saved tw info from download")
        # 全局写入信息
        saved_tw_location_info[url] = folder_name
        # 新增项
        new_tw_info.append("{},{}".format(url, folder_name))
    except Exception as ex:
        logger.error(ex)
        logger.error("Download info error, {}".format(info))

# 写入媒体信息到指定目录
def write_medias_info(info, full_folder_name):
    medias = info.get("medias")
    if medias != None:
        # 遍历媒体信息
        for j in range(len(medias)):
            media = medias[j]
            image_url = media.get("media_url_https")
            variant_url = media.get("variant_url")
            # 写入图片
            if image_url != None:
                image = requests.get(image_url)
                suffix = image_url.split(".")[-1]
                save_media("{}.{}".format(os.path.join(full_folder_name, str(j + 1)), suffix), image.content)
            # 写入视频
            if variant_url != None:
                variant = requests.get(variant_url)
                variant_content_type = media.get("variant_content_type")
                suffix = variant_content_type.split("/")[-1]
                save_media("{}.{}".format(os.path.join(full_folder_name, str(j + 1)), suffix), variant.content)

# 写入指定文件总结信息
def write_summary_info(info, summary_file_name):
    full_text = info.get("full_text")
    name = info.get("name")
    screen_name = info.get("screen_name")
    create_at = info.get("create_at")
    description = info.get("description")
    url = info.get("url")
    f = open(summary_file_name, "w", encoding = "utf8")
    if name != None:
        f.write("name: {}\n".format(name))
    if screen_name != None:
        f.write("screen_name: {}\n".format(screen_name))
    if description != None:
        f.write("description: {}\n".format(description))
    if create_at != None:
        f.write("create_at: {}\n".format(create_at))
    if full_text != None:
        f.write("full_text: {}\n".format(full_text))
    if url != None:
        f.write("url: {}\n".format(url))
    f.close()
    
# 写入指定文件总结信息, json
def write_summary_json(info, summary_file_name):
    f = open(summary_file_name, "w", encoding = "utf8")
    f.write(json.dumps(info, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    f.close()

# 将指定内容保存到指定文件中
def save_media(file_name, content):
    f = open(file_name, "wb")
    f.write(content)
    f.close()

# 获取用户的tw信息
def get_favorite_tw_info(url_prefix, url_suffix, target_dir, scan_all, ignore_existed_data, limited_count):
    # 如果ignore_existed_data=True，则忽略已经下载过的信息
    if ignore_existed_data:
        existed_data = dict()
    else:
        existed_data = get_all_saved_tw_location(os.path.join(target_dir, __map_relation))

    # 获取所有tw信息
    all_info = get_data(url_prefix, url_suffix, existed_data, scan_all, limited_count)
    return all_info

# 输出参数规则
def print_regular():
    print("""
There are 8 supported parameters as follows:
1. The uid of the user info you wanted to aquired.
2. The info type, all supported types: favorite, user.
3. The specified data source. You can directly input the content of data source or input the file name of data source.
4. The specified directory of downloaded tiwtter information.
5. Whether only download the twitter info records or not. [T, F].
6. Whether scan all records of the target. [T, F].
7. Whether ignore the existed data of the target. [T, F].
8. The maxinum of the target twitter records.

The first two parameters are required, and the others are optional.""")
    
# 读取参数
def get_argv_params(logger):
    if len(sys.argv) < 3:
        logger.error("Lack argv.")
        print_regular()
        exit(-1)
    uid = sys.argv[1]
    data_type = sys.argv[2]
    data_source = sys.argv[3] if len(sys.argv) > 3 else ""
    target_dir = sys.argv[4] if len(sys.argv) > 4 else ""
    only_check = sys.argv[5].lower() == "true" or sys.argv[5] == "t" if len(sys.argv) > 5 else False
    scan_all = sys.argv[6].lower() == "true" or sys.argv[6] == "t" if len(sys.argv) > 6 else False
    ignore_existed_data = sys.argv[7].lower() == "true" or sys.argv[7] == "t" if len(sys.argv) > 7 else False
    try:
        limited_count = int(sys.argv[8]) if len(sys.argv) > 8 else 999999999
    except:
        logger.error("Invalid limited_count: {}".format(sys.argv[8]))
        print_regular()
        exit(-1)
    
    if data_type.lower() == "favorite" or data_type.lower() == "like":
        url_prefix = 'https://x.com/i/api/graphql/ayhH-V7xvuv4nPZpkpuhFA/Likes?variables={"userId":"' + uid + '","count":20,'
        url_suffix = '"includePromotedContent":false,"withClientEventToken":false,"withBirdwatchNotes":false,"withVoice":true,"withV2Timeline":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticlePlainText":false}'
        folder_type = "favorite"
    elif data_type.lower() == "user":
        url_prefix = 'https://twitter.com/i/api/graphql/2inuEWeVPJC1aHMoIyAEYg/UserTweets?variables={"userId":"' + uid + '","count":20,'
        url_suffix = '"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticlePlainText":false}'
        folder_type = "user"
    else:
        logger.error("Unrecognized data type: {}".format(data_type))
        print_regular()
        exit(-1)

    # 目标路径
    if target_dir == None or target_dir == "" or target_dir.lower() == "none" or target_dir.lower() == "null" or target_dir.lower() == "false" or target_dir.lower() == 'f':
        target_dir = os.path.join(__target, uid, folder_type)
    
    # 打印本次启动的所有参数
    logger.info("Start parameters [uid={}, data_type={}, only_check={}, scan_all={}, ignore_existed_data={}, limited_count={}, target_dir={}]".format(uid, data_type, only_check, scan_all, ignore_existed_data, limited_count, target_dir))
    
    return uid,data_source,only_check,scan_all,ignore_existed_data,url_prefix,url_suffix,folder_type,target_dir

# 从data_source中获取待下载的tw信息
def get_from_data_source(data_source) -> dict:
    if data_source == None:
        return None
    data_source = data_source.strip()
    if data_source == "" or target_dir.lower() == "none" or data_source.lower() == "null" or data_source.lower() == "false" or data_source.lower() == 'f':
        return None

    if os.path.exists(data_source):
        data_source_file = open(data_source, "rb")
        data = data_source_file.read()
        data_source_file.close()
        try:
            text = data.decode("utf8")
        except:
            logger.error("Can not decode data source file with utf8")
            exit(-1)
        try:
            return json.loads(text)
        except:
            logger.error("Data source file is not valid json formatted file")
            exit(-1)
    try:
        return json.loads(data_source)
    except:
        logger.error("Data source is not valid json formatted file")
        exit(-1)
        


# 保存本次执行需要下载的所有tw信息
def save_tw_info_records(__output_file_dir, logger, all_info):
    if not os.path.exists(__output_file_dir):
        os.makedirs(__output_file_dir)
    output_file_name = os.path.join(__output_file_dir, str(uuid.uuid4()) + ".json")
    f = open(output_file_name, "w", encoding = "utf8")
    f.write(json.dumps(all_info, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
    f.close()
    logger.info("Output file is: {}".format(os.path.abspath(output_file_name)))

if __name__ == "__main__":
    # 读取参数
    uid, data_source, only_check, scan_all, ignore_existed_data, url_prefix, url_suffix, folder_type, target_dir = get_argv_params(logger)

    # 如果不存在则创建目录
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 从data_source中获取tw信息
    all_info = get_from_data_source(data_source)
    
    # download获取所有信息
    if all_info == None:
        all_info = get_favorite_tw_info(url_prefix, url_suffix, target_dir, scan_all = scan_all, ignore_existed_data = ignore_existed_data, limited_count = 999999999)
    
    # 打印本次执行需要下载的所有tw信息
    save_tw_info_records(__output_file_dir, logger, all_info)
    
    # 仅输出所有待下载内容
    if only_check:
        exit(0)
    
    # 存储所有信息
    save_all_data(all_info, target_dir, os.path.join(__target, __map_relation))