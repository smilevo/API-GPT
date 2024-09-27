import json
import os
import matplotlib.pyplot as plt

def prompt_tracker(directory):
    prompt_frequency = {}
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
                        if 'NumberOfPrompts' in sharing_data:
                            num_prompts = sharing_data['NumberOfPrompts']
                            prompt_frequency[num_prompts] = prompt_frequency.get(num_prompts, 0) + 1
    return prompt_frequency


def type_tracker(directory):
    type_frequency = {}
    # iterating over each json file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file_path = os.path.join(directory, filename)
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
            # iterating through sources list in the json data
            # sources is the outermost enclosing for these file
            for source in data['Sources']:
                source_type = source.get('Type', 'Unknown')  # Default to 'Unknown' if 'Type' is not present
                type_frequency[source_type] = type_frequency.get(source_type, 0) + 1
    return type_frequency

# prompts_0727 = prompt_tracker("DevGPT/snapshot_20230727")
# commenting out the rest of the snapshots for now
# prompts_0803 = prompt_tracker("DevGPT/snapshot_20230803")
# prompts_0810 = prompt_tracker("DevGPT/snapshot_20230810")
# prompts_0817 = prompt_tracker("DevGPT/snapshot_20230817")
# prompts_0824 = prompt_tracker("DevGPT/snapshot_20230824")
# prompts_0831 = prompt_tracker("DevGPT/snapshot_20230831")

# type_0727 = type_tracker("DevGPT/snapshot_20230727")
# commenting out the rest of the snapshots for now
# type_0803 = type_tracker("DevGPT/snapshot_20230803")
# type_0810 = type_tracker("DevGPT/snapshot_20230810")
# type_0817 = type_tracker("DevGPT/snapshot_20230817")
# type_0824 = type_tracker("DevGPT/snapshot_20230824")
# type_0831 = type_tracker("DevGPT/snapshot_20230831")

'''
print("Printing:")
for key in list(prompts_0727.keys()):
    print("Prompts:", key, " Count:", prompts_0727[key])
for key in list(type_0727.keys()):
    print("Type:", key, " Count:", type_0727[key])
'''

# generating bar graphs
def barGraph(prompt_frequency):
    num_prompts = list(prompt_frequency.keys())
    frequencies = list(prompt_frequency.values())
    plt.figure(figsize=(10, 6))
    plt.bar(num_prompts, frequencies)
    plt.xlabel('Number of Prompts')
    plt.ylabel('Frequency')
    plt.title('Frequency of Number of Prompts')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
# barGraph(prompts_0727)


# creating a list to store 'conversations' based on num of prompts = 2
conversations_2_prompts = []
def prompt2(directory):
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
                        if 'NumberOfPrompts' in sharing_data and sharing_data['NumberOfPrompts'] == 2:
                            # Check for the 'conversations' attribute and store it
                            if 'Conversations' in sharing_data:
                                conversations_2_prompts.append(sharing_data['Conversations'])

prompt2("DevGPT/snapshot_20230727")


# testing for commit_sharing file

conv_2_prompts = []
with open("DevGPT/snapshot_20230727/20230727_200003_commit_sharings.json", 'r') as json_file:
    data = json.load(json_file)
# iterating through sources list in the json data
# sources is the outermost enclosing for these file
for source in data['Sources']:
    if 'ChatgptSharing' in source:
        for sharing_data in source['ChatgptSharing']:
            if 'NumberOfPrompts' in sharing_data and sharing_data['NumberOfPrompts'] == 2:
                # Check for the 'conversations' attribute and store it
                if 'Conversations' in sharing_data:
                    conv_2_prompts.append(sharing_data['Conversations'])

print(len(conv_2_prompts))
index = 1
for conversation in conv_2_prompts:
    print('Conversation', index)
    print(json.dumps(conversation, indent=2))
    index=index+1


'''
# printing the first 10 stored conversations for objects with NumberOfPrompts = 2
print(len(conversations_2_prompts))
index = 0
for conversation in conversations_2_prompts[:10]:
    print('Conversation', index)
    print(json.dumps(conversation, indent=2))
    index=index+1
'''