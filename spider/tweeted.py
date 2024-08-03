from tool.decorators import LoggerWrapper
from . import logger
import requests
from configs.config import headers
from .parse import *
import sys
from tool.tool import get_formatted_json_str

@LoggerWrapper(logger)
def get_all_twitted_info(rest_id: str) -> list:
    """获取一个用户发布的以及转贴的所有twitter信息

    Args:
        rest_id (str): 用户的rest id

    Returns:
        list: 该用户的所有推文信息
    """
    try:
        next_url = get_base_url(rest_id)
        all_entry_info = []
        counter = 1
        while next_url != None:
            logger.info("Round :{}".format(counter))
            counter += 1
            entry_info = get_tweeted_info_by_url(next_url)
            next_url = get_next_url(rest_id, entry_info)
            current_entry_info = entry_info[:-2]
            all_entry_info += current_entry_info
            # 打印本页所有信息数量
            logger.info("The count of current round is {}, all count is {}".format(len(current_entry_info), len(all_entry_info)))
            # 如果本页没有了，则终止
            if len(entry_info) == 0:
                break
        return all_entry_info
    except Exception as ex:
        logger.exception(ex)
        return []


def get_next_url(rest_id: str, entry_info: list) -> str:
    """获取下一页的url

    Args:
        rest_id (str): 用户id
        entry_info (list): 上一轮获取的信息

    Returns:
        str: 下一页的url
    """
    url_prefix, url_suffix = get_url_prefix_suffix(rest_id)
    if len(entry_info) > 0:
        cursor: str = entry_info[-1].get("content_info", {}).get("cursor", None)
        if cursor != None and cursor.strip() != "":
            return url_prefix + '"cursor":"{}",'.format(cursor) + url_suffix
    return None


def get_url_prefix_suffix(rest_id: str) -> tuple:
    """获取url的前后缀

    Args:
        rest_id (str): 用户id

    Returns:
        tuple: (url前缀, url后缀)
    """
    url_prefix = 'https://twitter.com/i/api/graphql/2inuEWeVPJC1aHMoIyAEYg/UserTweets?variables={"userId":"' + rest_id + '","count":20,'
    url_suffix = '"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticlePlainText":false}'
    return (url_prefix, url_suffix)


def get_base_url(rest_id: str) -> str:
    """获取起始url

    Args:
        rest_id (str): 用户id

    Returns:
        str: 起始url
    """
    return "".join(get_url_prefix_suffix(rest_id))


@LoggerWrapper(logger)
def get_tweeted_info_by_url(url: str) -> dict:
    """通过url获取tw信息

    Args:
        url (str): url

    Returns:
        list: tw信息列表
    """
    try:
        result = requests.get(url, headers = headers)
        twitter_result = result.json()
        entries = get_entries_from_tweeted_response(twitter_result)
        entry_info_list = get_entry_info_list_from_entries(entries)
        return entry_info_list
    except Exception as ex:
        logger.exception(ex)
        return []


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input rest id of the user")
        exit(-1)
    rest_id = sys.argv[1]
    twitter_info = get_all_twitted_info(rest_id)
    print(get_formatted_json_str(twitter_info))