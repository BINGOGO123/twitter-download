from . import logger
from .parse import *
import sys
from tool.tool import get_formatted_json_str
from .tweet_page import AbstractTweetPage
from . import module_config

class TweetedTweetPage(AbstractTweetPage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page_count = kwargs.get("page_count", module_config.get("page_count"))
        
        
    def get_url_prefix_suffix(self, rest_id: str) -> tuple:
        url_prefix = 'https://twitter.com/i/api/graphql/2inuEWeVPJC1aHMoIyAEYg/UserTweets?variables={"userId":"' + rest_id + '","count":' + str(self.page_count) + ','
        url_suffix = '"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticlePlainText":false}'
        return (url_prefix, url_suffix)


    def parse_response_info(self, data: dict) -> dict:
        entries = get_entries_from_tweeted_response(data)
        return get_entry_info_list_from_entries(entries)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input rest id of the user")
        exit(-1)
    rest_id = sys.argv[1]
    tweet = TweetedTweetPage()
    twitter_info = tweet.get_info(rest_id)
    print(get_formatted_json_str(twitter_info))