import os

from crewai import Agent
from coin_tools.coingecko import CoingeckoApiTools
from tools.website_tools import WebsiteTools
from tools.ner_tools import NerTools
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from textwrap import dedent

load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class AIForecastCoinAgent():
    def __init__(self):
        load_dotenv()
        model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo-0125")
        self.llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
                         openai_api_key=os.environ.get("OPENAI_API_KEY"),
                         temperature=0.1,
                         model_name=model_name,
                         # top_p=0.3
                         )

    def find_token_id_agent(self):
        return Agent(
            role="Senior finder token id in API engineer",
            goal=dedent("""Find in external API required token.
                            It means make success requests using API with query_name of this token and return id."""),
            tools=[CoingeckoApiTools.search_coin_id],
            backstory=dedent("""Expert for cryptocurrency search in API information about token id. 
                                That will be pruff that token are existing in API"""),
            verbose=True,
            allow_deligation=False,
            llm=self.llm,
        )

    def find_token_social_info_agent(self):
        return Agent(
            role="Senior engineer whom will find al token social media links in API",
            goal=dedent("""Find in external API social media links and information about the required token. 
                            It means make success requests using API with token id like parameter 
                            and add homepage link and other social media urls and information to context."""),
            tools=[CoingeckoApiTools.get_coin_social],
            backstory=dedent("""Expert for cryptocurrency searching for social media links, 
                                information about token and homepage website link in API."""),
            verbose=True,
            allow_deligation=False,
            llm=self.llm,
        )

    def extract_text_from_url_agent(self):
        return Agent(
            role="Senior text extractor from website",
            goal=dedent("""Extract text from token homepage website and add it to context. 
                            It means to find in the context homepage url, make request to this url, 
                            extract text from this website and add it to context field homepage_content."""),
            tools=[WebsiteTools.extract_content_from_website],
            backstory="Expert for extracting text from websites and adding it to the context.",
            verbose=True,
            allow_deligation=False,
            llm=self.llm,
        )

    # def ner_coin_agent(self):
    #     return Agent(
    #         role="Senior NLP engineer",
    #         goal="Find in query, that coins user asking about and what he want to do with it",
    #         tools=[NerTools.extract_coins],
    #         backstory=dedent("""Expert for cryptocurrency searching in query, detect coins name,
    #         necessary action and additional information from user query"""),
    #         verbose=True,
    #         allow_deligation=False,
    #         llm=self.llm,
    #     )


    # def get_history_agent(self):
    #     return Agent(
    #         role="History data fetcher",
    #         goal="Return historical data from external API based on request coin and required days",
    #         tools=[CoingeckoApiTools.find_coin_info],
    #         backstory=dedent("""Expert of crypt historical data, have file storage where contain data
    #                           and can make requests if some data don't have in the storage,
    #                           borne to provide required history coin data."""),
    #         verbose=True,
    #         allow_deligation=True,
    #     )
    #

