import requests
import yaml

from textwrap import dedent
from termcolor import cprint
from langchain.tools import tool


class WebsiteTools():
    @tool("Extract text from website")
    def extract_content_from_website(context):
        """
        Useful to extruct text content from the websites, given homepage link in context for required token.
        :param context: Dict with token information that necessary includes field links and subfield homepage
        example:
        {
           "query_name":"Solana",
           "id":"solana",
           "community_data":{
              "facebook_likes":"None",
              "twitter_followers":2597884,
              "reddit_average_posts_48h":0.0,
              "reddit_average_comments_48h":0.0,
              "reddit_subscribers":0,
              "reddit_accounts_active_48h":0,
              "telegram_channel_user_count":60161
           },
           "links":{
              "homepage":["https://solana.com/",],
              "whitepaper":"",
              "blockchain_site":[
                 "https://solscan.io/",
                 "https://xray.helius.xyz/",
                 "https://solana.fm/",
                 "https://solanabeach.io/",
                 "https://www.oklink.com/sol",
                 "https://explorer.solana.com/",],
                  ...
            }, ...
        }
        In this case you should use https://solana.com/ for extracting text information about token from the website.
        Return Dict with token information and text information from homepage token website
        if success else return previous context
        """
        if ("links" in context.keys()) and ("homepage" in context["links"].keys()):
            return_coin_info = context.copy()
            token_homepage_url = context['links']['homepage'][0]
            cprint(f"Extracting text from {token_homepage_url=} website.", "black", "on_green")
            base_url = "https://r.jina.ai/"
            # input_url = ["https://bonkcoin.com/", "https://solana.com/"][-1]
            full_url = base_url + token_homepage_url
            headers = {
                "Accept": "text/event-stream"
            }
            response = requests.get(full_url, headers=headers, stream=True)
            temp_str = ""
            max_len_content = 0
            try:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if len(decoded_line) >= max_len_content:
                            max_len_content = len(decoded_line)
                            temp_str = decoded_line
            finally:
                response.close()
            yaml_content = yaml.safe_load(temp_str)
            return_coin_info['homepage_content'] = yaml_content
            cprint(dedent(f"""\nText homepage content was extracted from {token_homepage_url=} 
                                and added to context homepage_content field. 
                                \n Current context:\n {return_coin_info=}"""),
                   "black", "on_green", force_color=True)
            return return_coin_info
        else:
            cprint(f"Check input \n {context=}.\n Looks like it doesn't have required links",
                   "white", "on_red", force_color=True)
            return context
