from textwrap import dedent
from crewai import Task


class AIForecastCoinTask():

    def find_coin_id_task(self, agent, context):
        return Task(
            description=f'Check, that token from {context=} available by API and add token id to context',
            agent=agent,
            async_execution=False,
            expected_output=dedent("""
                Dicts with token info including query_name and id
                Example output:
                {
                "query_name": "Solana",
                "id": "solana",
                }
            """),
        )


    def find_coin_social_media_task(self, agent, context):
        return Task(
            description=dedent(f"""Using token id from {context=}, find in API social media information, 
                                homepage urls and links about token and add it to context"""),
            agent=agent,
            async_execution=False,
            context=context,
            expected_output=dedent("""
                Dicts with social media information about token including homepage url and other links.           
                Example output:
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
            """),
        )


    def extract_text_website_task(self, agent, context):
        return Task(
            description=dedent(f"""Using url from links/homepage in {context=}, 
                                extract text from this website and add it to context."""),
            agent=agent,
            async_execution=False,
            context=context,
            expected_output=dedent("""
                Dict with token id, social media information about token and homepage text content of token.   
                Example output:
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
                   "homepage_content": "Powerful for developers. Fast for everyone. Bring blockchain to the people. 
                                        Solana supports experiences for power users, new consumers, 
                                        and everyone in between! Powering tools and integrations from companies 
                                        all around the world. Join a community of millions...." 
                }
                """),
        )


    # def extract_coin_task(self, agent, query):
    #     return Task(
    #         description=dedent(f"""Extract from the query: {query} the name of the coin
    #                               or coins and what you want to do with them, including additional arguments"""),
    #         agent=agent,
    #         async_execution=False,
    #         expected_output=dedent("""
    #         List with coins, each one include dict with mandatory  name of coin and usage, add_args are optional.

    #             Example output:
    #             [
    #                 {
    #                     'name': 'ETH',
    #                     'usage': 'predict',
    #                     'add_args': '100 days'
    #                 },
    #                 {
    #                     'name': 'BTC',
    #                     'usage': 'predict',
    #                     'add_args': '100 days'
    #                 }
    #             ]
    #         """),
    #     )


    # def fetch_history_task(self, agent, context):
    #     return Task(
    #         description=dedent(f"""Return history data of coin getting parameters from context
    #                           and making request with that parameters, if don't found in storage"""),
    #         agent=agent,
    #         context=context,
    #         async_execution=False,
    #         expected_output=dedent("""
    #         List of lists, each one contain datetime, open, high, low, close of coin

    #             Example output:
    #             [
    #                 [1704153600000, 0.01503925, 0.01679391, 0.01285355, 0.01492669],
    #                 [1704499200000, 0.01521003, 0.01530565, 0.00499933, 0.01107309], ...
    #             ]
    #         """),
    #     )


    # def predict_coin_task(self, agent, context):
    #     return Task(
    #         description="Make report with forecasting of coin, learning on historical data and return forecasting",
    #         agent=agent,
    #         comtext=context,
    #         async_execution=True,
    #         expected_output=dedent("""
    #         Dict with methods of forecasting and lists with datetime, forecasting close price inside each one

    #        Example output:
    #            {
    #                'NBEATS': [[1704844800000, 0.01730565], [1705190400000, 0.01830965],...],
    #                'NHITS': [[1704844800000, 0.01730545], [1705190400000, 0.01833965],...],
    #                'PatchTST': [[1704844800000, 0.01730464], [1705190400000, 0.01830565],...]
    #            }
    #            """),
    #     )
