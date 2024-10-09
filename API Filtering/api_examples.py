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

prompt("DevGPT/snapshot_20230727")
prompt("DevGPT/snapshot_20230803")
prompt("DevGPT/snapshot_20230810")
prompt("DevGPT/snapshot_20230817")
prompt("DevGPT/snapshot_20230824")
prompt("DevGPT/snapshot_20230831")


examples = []

api_crud=0
api_json=0
api_test=0
api_curl=0
api_cors=0
api_request=0

def example_generator(conversation):
    global api_crud
    global api_json
    global api_test
    global api_curl
    global api_cors
    global api_request
    global examples
    
    if 'crud' in conversation[0] and 'crud' in conversation[1] and api_crud<5:
        t = (conversation[0], conversation[1], 'crud')
        examples.append(t)
        api_crud+=1
    if 'json' in conversation[0] and 'json' in conversation[1] and api_json<5:
        t = (conversation[0], conversation[1], 'json')
        examples.append(t)
        api_json+=1
    if 'api test' in conversation[0] and 'api test' in conversation[1] and api_test<5:
        t = (conversation[0], conversation[1], 'api testing')
        examples.append(t)
        api_test+=1
    if 'curl' in conversation[0] and 'curl' in conversation[1] and api_curl<5:
        t = (conversation[0], conversation[1], 'curl')
        examples.append(t)
        api_curl+=1
    if 'cors' in conversation[0] and 'cors' in conversation[1] and api_cors<5:
        t = (conversation[0], conversation[1], 'cors')
        examples.append(t)
        api_cors+=1
    if 'api request' in conversation[0] and 'api call' in conversation[1] and api_request<5:
        t = (conversation[0], conversation[1], 'api call')
        examples.append(t)
        api_request += 1

for conversation in conversations:
    example_generator(conversation)

df = pd.DataFrame(examples, columns=['prompt', 'reply', 'class'])
df.to_csv('api_examples_prompt_term.csv', index=False)
