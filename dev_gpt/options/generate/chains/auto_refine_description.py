import json

from dev_gpt.apis.gpt import ask_gpt
from dev_gpt.options.generate.parser import identity_parser
from dev_gpt.options.generate.prompt_factory import context_to_string



def auto_refine_description(context):
    context['microservice_description'] = ask_gpt(
        better_description_prompt,
        identity_parser,
        context_string=context_to_string(context)
    )
    context['request_schema'] = ask_gpt(
        generate_request_schema_prompt,
        identity_parser,
        context_string=context_to_string(context)
    )
    context['response_schema'] = ask_gpt(
        generate_output_schema_prompt,
        identity_parser,
        context_string=context_to_string(context)
    )
    context['microservice_description'] = ask_gpt(
        summarize_description_and_schemas_prompt,
        identity_parser,
        context_string=context_to_string(context)
    )
    # details = extract_information(context['microservice_description'], ['database connection details', 'URL', 'secret'])
    # if details:
    #     context['microservice_description'] += '\n\nAdditional information:' + json.dumps(details, indent=4)
    # del context['details']


better_description_prompt = f'''{{context_string}}
Update the description of the Microservice to make it more precise without adding or removing information.
Note: the output must be a list of tasks the Microservice has to perform.
Example for the description: "return the average temperature of the 5 days weather forecast for a given location."
1. get the 5 days weather forcast from the https://openweathermap.org/ API
2. extract the temperature from the response
3. calculate the average temperature'''

generate_request_schema_prompt = '''{context_string}
Generate the lean request json schema of the Microservice.
Note: If you are not sure about the details, then come up with the minimal number of parameters possible.'''

generate_output_schema_prompt = '''{context_string}
Generate the lean response json schema for the Microservice.
Note: If you are not sure about the details, then come up with the minimal number of parameters possible.'''

summarize_description_and_schemas_prompt = '''{context_string}
Write an updated microservice description by incorporating information about the request and response parameters in a concise way without losing any information.
Note: You must not mention any details about algorithms or the technical implementation.
Note: You must not mention that there is a request and response JSON schema
Note: You must not use any formatting like triple backticks.
Note: If an external API is mentioned in the description, then you must mention the API in the updated description as well.'''
