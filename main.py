from crewai import Crew, Process
from agents import AIForecastCoinAgent
from tasks import AIForecastCoinTask
from langchain_openai import ChatOpenAI
from textwrap import dedent
from termcolor import cprint
from dotenv import load_dotenv
import os

load_dotenv()
model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo-0125")
default_llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
                        openai_api_key=os.environ.get("OPENAI_API_KEY"),
                        temperature=0.1,
                        model_name=model_name,
                        # top_p=0.3
                         )


class CoinCrew:
    def __init__(self, query, llm):
        self.query = query
        self.llm = llm

    def run(self):

        agents = AIForecastCoinAgent()
        tasks = AIForecastCoinTask()

        finder_id = agents.find_token_id_agent()
        finder_media = agents.find_token_social_info_agent()
        extractor_url = agents.extract_text_from_url_agent()

        find_token_id_task = tasks.find_coin_id_task(finder_id,  [self.query])
        find_token_media_info_task = tasks.find_coin_social_media_task(finder_media, [find_token_id_task])
        extract_url_task = tasks.extract_text_website_task(extractor_url, [find_token_media_info_task])

        crew = Crew(
            agents=[finder_id, finder_media, extractor_url],
            tasks=[find_token_id_task, find_token_media_info_task, extract_url_task],
            process=Process.sequential,
            verbose=1,
            manager_llm=self.llm,
            function_calling_llm=self.llm,
            )
        crew_result = crew.kickoff()
        return crew_result


if __name__ == "__main__":
    # EXAMPLE:
    #token_name = "Rally"
    token_name = input(
        dedent("""
      What token do you want to analyze?
      Example: Solana
    """))
    query = {"query_name": token_name}
    coin_crew = CoinCrew(query, default_llm)
    cprint(coin_crew.run(),"black", "on_green", force_color=True)
