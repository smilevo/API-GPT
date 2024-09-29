import json
import os
from nltk.tokenize import word_tokenize
import re
import pandas as pd

def clean(text):
    # tokenization
    tokens = word_tokenize(text)
    # lowercasing
    tokens = [token.lower() for token in tokens]
    # removing special characters
    tokens = [re.sub(r'[^a-zA-Z0-9]', '', token) for token in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

conversations = []
def prompt(directory):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist!")
        return
    
    # iterating over each json file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file_path = os.path.join(directory, filename)
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # iterating through sources list in the json data
            # sources is the outermost enclosing for these file
            for source in data['Sources']:
                if 'ChatgptSharing' in source:
                    for sharing_data in source['ChatgptSharing']:
                        # Check for the 'conversations' attribute and store it
                        if 'Conversations' in sharing_data:
                            for conversation in sharing_data['Conversations']:
                                prompt = clean(conversation['Prompt'])
                                reply = clean(conversation['Answer'])
                                conversations.append((prompt, reply))


prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230727")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230803")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230810")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230817")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230824")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230831")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230907")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20230914")
prompt(r"D:/Study material/RIT stuff/Applied Data Science/DevGPT/snapshot_20231012")

'''
keywords = [
    'CRUD', 'DELETE', 'GET', 'PATCH', 'POST', 'PUT', 'API gateway', 'API headers', 'API key', 'Cache',
'Endpoint', 'gRPC', 'GraphQL', 'HTTP', 'Microservices', 'OpenID Connect', 'Parameters', 'RPC', 'REST',
'SOAP', 'Status codes', 'Webhooks', 'API definition', 'JSON', 'JSON Schema', 'OpenAPI', 'RAML', 'XML',
'API collaboration', 'API mocking', 'API testing', 'Shift-left testing', 'AJAX', 'API client', 'API marketplace',
'API platform', 'API portal', 'cURL', 'API access', 'API authentication', 'API credentials', 'CORS', 'OAuth',
'OpenID Connect', 'API call', 'API economy', 'API ecosystem', 'API-first', 'API request', 'Collections',
'Collection Runner', 'Newman', 'Postman CLI', 'Fork', 'Postman Flows', 'Private API Network', 'Public API Network',
'User group', 'Workspaces'
]

# keywords = [keyword.lower() for keyword in keywords]
'''

'''
keywords = ['crud', 'delete', 'get', 'patch', 'post', 'put', 'api gateway', 'api headers', 'api key', 'cache', 
 'endpoint','grpc', 'graphql', 'http', 'microservices', 'openid connect', 'parameters', 'rpc', 'rest',
 'soap', 'status codes', 'webhooks', 'api definition', 'json', 'json schema', 'openapi', 'raml', 'xml',
 'api collaboration', 'api mocking', 'api testing', 'shift-left testing', 'ajax', 'api client',
 'api marketplace', 'api platform', 'api portal', 'curl', 'api access', 'api authentication', 'api credentials',
 'cors', 'oauth', 'openid connect', 'api call', 'api economy', 'api ecosystem', 'api-first', 'api request',
 'collections', 'collection runner', 'newman', 'postman cli', 'fork', 'postman flows', 'private api network',
 'public api network', 'user group', 'workspaces']
'''

#keywords = ['api collaboration', 'api mocking', 'api testing', 'shift-left testing']

#pattern = re.compile('|'.join(map(re.escape, keywords)))

#def is_api_related(prompt):   
#    return bool(pattern.search(prompt))

labels = {}

def add_label(conversation, api_class, api_subclass):
    global labels
    if conversation in labels:
        update = labels[conversation]
        update[0].add(api_class)
        update[1].add(api_subclass)
        labels[conversation] = update
    else:
        update = [set(), set()]
        update[0].add(api_class)
        update[1].add(api_subclass)
        labels[conversation] = update

api_crud = 0
api_delete = 0
api_get = 0
api_patch = 0
api_post = 0
api_put = 0

def method_counter(conversation):
    global api_crud
    global api_delete
    global api_get
    global api_patch
    global api_post
    global api_put
    if 'crud' in conversation[0] or 'crud' in conversation[1]:
        api_crud+=1
        add_label(conversation, 'Method', 'crud')
    if 'delete' in conversation[0] or 'delete' in conversation[1]:
        api_delete+=1
        add_label(conversation, 'Method', 'delete')
    if 'get' in conversation[0] or 'get' in conversation[1]:
        api_get+=1
        add_label(conversation, 'Method', 'get')
    if 'patch' in conversation[0] or 'patch' in conversation[1]:
        api_patch+=1
        add_label(conversation, 'Method', 'patch')
    if 'post' in conversation[0] or 'post' in conversation[1]:
        api_post+=1
        add_label(conversation, 'Method', 'post')
    if 'put' in conversation[0] or 'put' in conversation[1]:
        api_put+=1
        add_label(conversation, 'Method', 'put')

api_definition = 0
api_json = 0
api_json_schema = 0
api_openapi = 0
api_raml = 0
api_xml = 0

def schema_format_counter(conversation):
    global api_definition
    global api_json
    global api_json_schema
    global api_openapi
    global api_raml
    global api_xml
    
    if 'api definition' in conversation[0] or 'api definition' in conversation[1]:
        api_definition+=1
        add_label(conversation, 'Schema_format', 'api_definition')
    if 'json' in conversation[0] or 'json' in conversation[1]:
        api_json+=1
        add_label(conversation, 'Schema_format', 'json')
    if 'json schema' in conversation[0] or 'json schema' in conversation[1]:
        api_json_schema+=1
        add_label(conversation, 'Schema_format', 'json_schema')
    if 'openapi' in conversation[0] or 'openapi' in conversation[1]:
        api_openapi+=1
        add_label(conversation, 'Schema_format', 'openapi')
    if 'raml' in conversation[0] or 'raml' in conversation[1]:
        api_raml+=1
        add_label(conversation, 'Schema_format', 'raml')
    if 'xml' in conversation[0] or 'xml' in conversation[1]:
        api_xml+=1
        add_label(conversation, 'Schema_format', 'xml')

api_colab = 0
api_mock = 0
api_test = 0
api_shift_test = 0

def process_counter(conversation):
    global api_colab
    global api_mock
    global api_test
    global api_shift_test
    if 'api collaboration' in conversation[0] or 'api collaboration' in conversation[1]:
        api_colab+=1
        add_label(conversation, 'Process', 'api_collaboration')
    if 'api mocking' in conversation[0] or 'api mocking' in conversation[1]:
        api_mock+=1
        add_label(conversation, 'Process', 'api_mocking')
    if 'api testing' in conversation[0] or 'api testing' in conversation[1]:
        api_test+=1
        add_label(conversation, 'Process', 'api_testing')
    if 'shift left testing' in conversation[0] or 'shift left testing' in conversation[1]:
        api_shift_test+=1
        add_label(conversation, 'Process', 'shift_left_testing')

api_ajax = 0
api_client = 0
api_marketplace = 0
api_platform = 0
api_portal = 0
api_curl = 0

def tools_counter(conversation):
    global api_ajax
    global api_client
    global api_marketplace
    global api_platform
    global api_portal
    global api_curl
    if 'ajax' in conversation[0] or 'ajax' in conversation[1]:
        api_ajax+=1
        add_label(conversation, 'Tools', 'ajax')
    if 'api client' in conversation[0] or 'api client' in conversation[1]:
        api_client+=1
        add_label(conversation, 'Tools', 'api_client')
    if 'api marketplace' in conversation[0] or 'api marketplace' in conversation[1]:
        api_marketplace+=1
        add_label(conversation, 'Tools', 'api_marketplace')
    if 'api platform' in conversation[0] or 'api platform' in conversation[1]:
        api_platform+=1
        add_label(conversation, 'Tools', 'api_platform')
    if 'api portal' in conversation[0] or 'api portal' in conversation[1]:
        api_portal+=1
        add_label(conversation, 'Tools', 'api_portal')
    if 'curl' in conversation[0] or 'curl' in conversation[1]:
        api_curl+=1
        add_label(conversation, 'Tools', 'curl')

api_access = 0
api_authentication = 0
api_credentials = 0
api_cors = 0
api_oauth = 0
api_openid_connect = 0

def security_counter(conversation):
    global api_access
    global api_authentication
    global api_credentials
    global api_cors
    global api_oauth
    global api_openid_connect
    if 'api access' in conversation[0] or 'api access' in conversation[1]:
        api_access+=1
        add_label(conversation, 'Security', 'api_access')
    if 'api authentication' in conversation[0] or 'api authentication' in conversation[1]:
        api_authentication+=1
        add_label(conversation, 'Security', 'api_authentication')
    if 'api credentials' in conversation[0] or 'api credentials' in conversation[1]:
        api_credentials+=1
        add_label(conversation, 'Security', 'api_credentials')
    if 'cors' in conversation[0] or 'cors' in conversation[1]:
        api_cors+=1
        add_label(conversation, 'Security', 'cors')
    if 'oauth' in conversation[0] or 'oauth' in conversation[1]:
        api_oauth+=1
        add_label(conversation, 'Security', 'oauth')
    if 'openid connect' in conversation[0] or 'openid connect' in conversation[1]:
        api_openid_connect+=1
        add_label(conversation, 'Security', 'openid_connect')

api_call = 0
api_economy = 0
api_ecosystem = 0
api_first = 0
api_request = 0

def related_counter(conversation):
    global api_call
    global api_economy
    global api_ecosystem
    global api_first
    global api_request
    if 'api call' in conversation[0] or 'api call' in conversation[1]:
        api_call+=1
        add_label(conversation, 'Related_terms', 'api_call')
    if 'api economy' in conversation[0] or 'api economy' in conversation[1]:
        api_economy+=1
        add_label(conversation, 'Related_terms', 'api_economy')
    if 'api ecosystem' in conversation[0] or 'api ecosystem' in conversation[1]:
        api_ecosystem+=1
        add_label(conversation, 'Related_terms', 'api_ecosystem')
    if 'api first' in conversation[0] or 'api first' in conversation[1]:
        api_first+=1
        add_label(conversation, 'Related_terms', 'api_first')
    if 'api request' in conversation[0] or 'api request' in conversation[1]:
        api_request+=1
        add_label(conversation, 'Related_terms', 'api_request')
                  
api_gateway = 0
api_headers = 0
api_key = 0
api_cache = 0
api_endpoint = 0
api_grpc = 0
api_graphql = 0
api_http = 0
api_microservices = 0
api_parameters = 0
api_rpc = 0
api_rest = 0
api_soap = 0
api_status_codes = 0
api_webhooks = 0

def architecture_components_counter (conversation):
    global api_gateway
    global api_headers
    global api_key
    global api_cache
    global api_endpoint
    global api_grpc
    global api_graphql
    global api_http
    global api_microservices
    global api_parameters
    global api_rpc
    global api_rest
    global api_soap
    global api_status_codes
    global api_webhooks

    if 'gateway' in conversation[0] or 'gateway' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'api_gateway')
        api_gateway+=1
    if 'headers' in conversation[0] or 'headers' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'api_headers')
        api_headers+=1
    if 'key' in conversation[0] or 'key' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'api_key')
        api_key+=1
    if 'cache' in conversation[0] or 'cache' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'cache')
        api_cache+=1
    if 'endpoint' in conversation[0] or 'endpoint' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'endpoint')
        api_endpoint+=1
    if 'grpc' in conversation[0] or 'grpc' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'grpc')
        api_grpc+=1
    if 'graphql' in conversation[0] or 'graphql' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'graphql')
        api_graphql+=1
    if 'http' in conversation[0] or 'http' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'http')
        api_http+=1
    if 'microservices' in conversation[0] or 'microservices' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'microservices')
        api_microservices+=1
    if 'parameters' in conversation[0] or 'parameters' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'parameters')
        api_parameters+=1
    if 'rpc' in conversation[0] or 'rpc' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'rpc')
        api_rpc+=1
    if 'rest' in conversation[0] or 'rest' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'rest')
        api_rest+=1
    if 'soap' in conversation[0] or 'soap' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'soap')
        api_soap+=1
    if 'status codes' in conversation[0] or 'status codes' in conversation[1]:
        add_label(conversation, 'Architecture_Components', )
        api_status_codes+=1
    if 'webhooks' in conversation[0] or 'webhooks' in conversation[1]:
        add_label(conversation, 'Architecture_Components', 'webhooks')
        api_webhooks+=1
    

for conversation in conversations:
    method_counter(conversation)
    schema_format_counter(conversation)
    process_counter(conversation)
    tools_counter(conversation)
    security_counter(conversation)
    related_counter(conversation)

rows = []
for key, value in labels.items():
    prompt_txt = key[0]
    reply = key[1]
    class_str = ', '.join(value[0])
    subclass_str = ', '.join(value[1])
    
    rows.append({'Prompt': prompt_txt, 'Reply': reply, 'Class': class_str, 'Subclass': subclass_str})

df = pd.DataFrame(rows, columns=['Prompt', 'Reply', 'Class', 'Subclass'])
df.to_excel('conv_api_label.xlsx', index=False)

print('METHOD TERMS')
print('api_crud', api_crud)
print('api_delete', api_delete)
print('api_get', api_get)
print('api_patch', api_patch)
print('api_post', api_post)
print('api_put', api_put)
print('--------------------------------------')

print('SCHEMA AND FORMAT TERMS')
print('api_definition', api_definition)
print('api_json', api_json)
print('api_json_schema', api_json_schema)
print('api_openapi', api_openapi)
print('api_raml', api_raml)
print('api_xml', api_xml)
print('--------------------------------------')

print('PROCESS TERMS')
print ('api_colab', api_colab)
print('api_mock', api_mock)
print('api_test', api_test)
print('api_shift_test', api_shift_test)
print('--------------------------------------')

print ('TOOL TERMS')
print('api_ajax', api_ajax)
print('api_client', api_client)
print('api_marketplace', api_marketplace)
print('api_platform', api_platform)
print('api_portal', api_portal)
print('api_curl', api_curl)
print('--------------------------------------')

print('SECURITY TERMS')
print('api_access', api_access)
print('api_authentication', api_authentication)
print('api_credentials', api_credentials)
print('api_cors', api_cors)
print('api_oauth', api_oauth)
print('api_openid_connect', api_openid_connect)
print('--------------------------------------')

print('RELATED CONCEPT TERMS')
print('api_call', api_call)
print('api_economy', api_economy)
print('api_ecosystem', api_ecosystem)
print('api_first', api_first)
print('api_request', api_request)
print('--------------------------------------')

print('ARCHITECTURE AND COMPONENTS')
print('api gateway', api_gateway)
print('api headers', api_headers)
print('api key', api_key)
print('cache', api_cache)
print('endpoint', api_endpoint)
print('grpc', api_grpc)
print('graphql', api_graphql)
print('http', api_http)
print('microservices', api_microservices)
print('parameters', api_parameters)
print('rpc', api_rpc)
print('rest', api_rest)
print('soap', api_soap)
print('status_codes', api_status_codes)
print('webhooks', api_webhooks)
print('--------------------------------------')