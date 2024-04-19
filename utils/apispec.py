from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
import json

with open('./utils/source/coingecko_swagger.json') as f:
    json_spec_file = json.load(f)

json_spec_file["servers"] = [
    {
      "url": "https://api.coingecko.com/api/v3"
    }
  ]

coingecko_spec = reduce_openapi_spec(json_spec_file)

verbose= True #TODO
if verbose:
    from termcolor import cprint
    import tiktoken
    import yaml

    endpoints = [
        (route, operation) for route, operations in json_spec_file["paths"].items() for operation in operations
        if operation in ["get"]
    ]

    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def count_tokens(s):
        return len(enc.encode(s))

    cprint(f"Tokens in openapi file: {count_tokens(yaml.dump(coingecko_spec))}"
           f"Get endpoints in current api: {len(endpoints)}", "white", "on_green")
