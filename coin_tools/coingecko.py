import os
import requests

from termcolor import cprint
from langchain.tools import tool
from dotenv import load_dotenv
from textwrap import dedent

load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class CoingeckoApiTools():
    @tool("Search token id")
    def search_coin_id(context):
        """
        Useful to find token id in public API coingeco.com, given query_name in context that user required.
        :param context: Dict that contain query_name, that you need to find in API.
        example:
        {
        "query_name": "Solana",
        }
        In this case you should use: https://api.coingecko.com/api/v3/search?query=solana
        Return dict with query_name and token id from coingecko API by current coin if success else the same context
        """
        if 'query_name' in context.keys():
            query_name = context["query_name"]
            cprint(f'\nSerching token id from {query_name=} in coingecko API', "black", "on_green")
            url = "https://api.coingecko.com/api/v3/search"
            headers = {"x-cg-api-key": COINGECKO_API_KEY}
            params = {"query": query_name}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                api_coins = response.json()
                id = api_coins["coins"][0]["id"]
                cprint(f"\nCoin id: {id} exist in coingecko",
                       "black", "on_green", force_color=True)
                return {"query_name": query_name, "id": id}
            else:
                cprint(dedent(f"""\nNo data available in the response for current {query_name=}, 
                                    that means will be returned the same context"""),
                       "white", "on_red", force_color=True)
                return context
        else:
            cprint(dedent(f"""\nNo query_name in context. 
                                That means will be returned the same {context=}"""),
                   "white", "on_red")
            return context

    @tool("Search token social media info")
    def get_coin_social(context):
        """
        Useful to find token social media links in public API coingeco.com, given token id in context.
        :param context: Dict that contain token id and query_name.
        example:
        {
        "query_name": "Solana",
        "id": "solana",
        }
        Return Dict with query_name, token id and additional social media links, statistic and home page link
        if success else the same context.
        """
        if all(field in context.keys() for field in ['id', 'query_name']):
            return_coin_info = {"query_name": context["query_name"], "id": context["id"]}

            cprint(f'\nGetting social media information about {return_coin_info["id"]=} in coingecko API',
                   "black", "on_green", force_color=True)
            url = f'https://api.coingecko.com/api/v3/coins/{return_coin_info["id"]}'
            headers = {"x-cg-api-key": COINGECKO_API_KEY}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                coin_info = response.json()
                need_fields = ["chat_url", "telegram_channel_identifier", "community_data", "contract_address", "links"]
                for field in need_fields:
                    if field in coin_info.keys():
                        return_coin_info[field] = coin_info[field]
                cprint(f"\nSocial media information using {context=} was extracted:\n {return_coin_info=}",
                       "black", "on_green", force_color=True)
            else:
                cprint(f"\nSocial media information don't available by API for current {return_coin_info=}",
                       "white", "on_red", force_color=True)
            return return_coin_info
        else:
            cprint(f"\nWrong context: no id or query_name in context, will be returned the same\n {context=}",
                   "white", "on_red", force_color=True)
            return context
    @tool("Get coin report") # TODO
    def get_coin_report(context):
        """Get context from previous task and save it to html file"""
        print(f"{context=}")
        return context


#     def get_coins_list(self,):
#         # Return pd.DataFrame(id, symbil, name) with all coins on the market provided by coingecko
#         """
#         Return list with dict of coins, each dict contain (id, symbil, name)
#         with all coins on the market provided by coingecko
#         if success else None
#         """
#
#         url = "https://api.coingecko.com/api/v3/coins/list"
#         headers = {"x-cg-api-key": COINGECKO_API_KEY}
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             coins_list = response.json()
#             return coins_list
#             # print(response.json())
#             # df = pd.DataFrame(coins_list, columns=["id", "symbol", "name"])
#             # return df
#         else:
#             cprint("No data available in the response.", "white", "on_red")
#             return None
