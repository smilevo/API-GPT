from bertopic import BERTopic
import json
import pandas as pd
import os
import preprocessing as ppc

prompts = []
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
                                prompts.append(ppc.preprocess_text(conversation['Prompt']))

prompt("DevGPT/snapshot_20230727")
prompt("DevGPT/snapshot_20230803")
prompt("DevGPT/snapshot_20230810")
prompt("DevGPT/snapshot_20230817")
prompt("DevGPT/snapshot_20230824")
prompt("DevGPT/snapshot_20230831")

print (len(prompts))

topic_model = BERTopic(embedding_model="all-MiniLM-L12-v2")
topics, probs = topic_model.fit_transform(prompts)

topic_df = pd.DataFrame(topic_model.get_topic_info())
topic_df.to_excel('topic_names.xlsx', index=False)

prompt_df = pd.DataFrame({'topic': topics, 'prompt': prompts})
prompt_df.to_excel('topic_prompts.xlsx', index=False)

print(topic_model.get_topic_info())

topic_model.visualize_topics()
