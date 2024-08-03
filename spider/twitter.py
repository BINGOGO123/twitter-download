from . import logger
from configs.config import headers
from .parse import *
import sys
from tool.tool import get_formatted_json_str
from .single_downloader import AbstractSinglePageDownloader
from .err import *


class TwitterInfoDownloader(AbstractSinglePageDownloader):
    def get_url(self, *args):
        if len(args) == 0:
            raise ArgsException("At least one arg required")
        if not isinstance(args[0], str):
            raise ArgsException("The first arg must be str")
        return 'https://x.com/i/api/graphql/ldqoq5MmFHN1FhMGvzC9Jg/TweetDetail?variables={"focalTweetId":"' + twitter_id +  '","with_rux_injections":false,"rankingMode":"Relevance","includePromotedContent":true,"withCommunity":true,"withQuickPromoteEligibilityTweetFields":true,"withBirdwatchNotes":true,"withVoice":true}&features={"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}&fieldToggles={"withArticleRichContentState":true,"withArticlePlainText":false,"withGrokAnalyze":false,"withDisallowedReplyControls":false}'
    
    
    def parse_response_info(self, data: dict) -> dict:
        entries = get_entries_from_twitter_response(data)
        return get_entry_info_list_from_entries(entries)
    

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input twitter id")
        exit(-1)
    twitter_id = sys.argv[1]
    downloader = TwitterInfoDownloader(headers)
    twitter_info = downloader.get_info(twitter_id)
    print(get_formatted_json_str(twitter_info))