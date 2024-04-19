from langchain.tools import tool
from langchain.chains import create_extraction_chain
from termcolor import cprint
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class NerTools(): # TODO https://huggingface.co/dslim/bert-base-NER
    @tool("Extract coins from user query")
    def extract_coins(query):
        """
        This tool is a tool designed to extract coin-related names from a user query.
        :param query: stirng with query from user
        example: "Can you find social media homepage link info for Rambox?"
        Return list of dicts with coins that was required by user, actions and additional arguments if success else None.
        """
        cprint(f'Extracting coin names from {query=} by vanilla NER',
               "black", "on_green", force_color=True)
        schema = {
            "properties": {
                "name": {"type": "string"},
                "action": {"type": "string"},
                "add_args": {"type": "string"}
            },
            "required": ["name", "action"]
        }
        load_dotenv()
        model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo-0125")
        llm = ChatOpenAI(openai_api_base=os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
                                 openai_api_key=os.environ.get("OPENAI_API_KEY"),
                                 temperature=0.1,
                                 model_name=model_name,
                                 # top_p=0.3
                                 )
        chain = create_extraction_chain(schema, llm)
        result = chain.run(query)
        if result:
            cprint(f"Next usage will be connected with this coins: {result}",
                   "black", "on_green", force_color=True)
            return result
        else:
            cprint(f"No data extracted like a coin from {query=}, change your query and try again",
                   "white", "on_red", force_color=True)
            return None
