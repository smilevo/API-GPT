import pandas as pd
import re

# path to the excel file
file_path = "conv_api_label.xlsx"
df = pd.read_excel(file_path)
# print(df.head())

# to get individual counts for each possible class
one_occur = {}
two_occur = {}
three_occur = {}
four_occur = {}
five_occur = {}
six_occur = {}

one_occur['count'] = 0
two_occur['count'] = 0
three_occur['count'] = 0
four_occur['count'] = 0
five_occur['count'] = 0
six_occur['count'] = 0

# helps write less code while looping by directly get dictionary name through length
occurrence_dict_map = {
    1: one_occur,
    2: two_occur,
    3: three_occur,
    4: four_occur,
    5: five_occur,
    6: six_occur
}

# storing all final method class single labels
rows = []

keywords = ['api gateway', 'api headers', 'api key', 'cache', 
 'endpoint','grpc', 'graphql', 'http', 'microservices', 'openid connect', 'parameters', 'rpc', 'rest',
 'soap', 'status codes', 'webhooks', 'api definition', 'json', 'json schema', 'openapi', 'raml', 'xml',
 'api collaboration', 'api mocking', 'api testing', 'shift-left testing', 'ajax', 'api client',
 'api marketplace', 'api platform', 'api portal', 'curl', 'api access', 'api authentication', 'api credentials',
 'cors', 'oauth', 'openid connect', 'api call', 'api economy', 'api ecosystem', 'api-first', 'api request',
 'collections', 'collection runner', 'newman', 'postman cli', 'fork', 'postman flows', 'private api network',
 'public api network', 'user group', 'workspaces']

pattern = re.compile('|'.join(map(re.escape, keywords)))
def is_api_related(prompt):
    return bool(pattern.search(prompt))

# making 0 entries to start counting in all dictionaries
method_subclasses = ['get', 'put', 'post', 'patch', 'delete', 'crud']
for i in range(1,7):
    for subclass in method_subclasses:
        occurrence_dict_map[i][subclass] = 0

# loop over dataframe rows and index
for index, row in df.iterrows():
    s = row['Class']
    classes = [cls.strip() for cls in s.split(',') if cls.strip()]
    if 'Method' in classes:
        s = row['Subclass']
        subclasses = [subcls.strip() for subcls in s.split(',') if subclass.strip()]
        subclasses = [subclass for subclass in subclasses if subclass in method_subclasses]

        # get the number of classes and increment count
        num_classes = len(subclasses)
        occurrence_dict_map[num_classes]['count'] += 1

        if num_classes==1:
            if subclasses[0] == 'get' or subclasses[0] == 'put':
                prompt_reply = str(row['Prompt']) + ' ' + str(row['Reply'])
                if is_api_related(prompt_reply):
                    rows.append({'Prompt': row['Prompt'], 'Reply': row['Reply'], 'Subclass': subclasses[0]})
            elif subclasses[0] in method_subclasses:
                rows.append({'Prompt': row['Prompt'], 'Reply': row['Reply'], 'Subclass': subclasses[0]})

        for cls in subclasses:
            if cls in occurrence_dict_map[num_classes]:
                occurrence_dict_map[num_classes][cls] += 1
            else:
                occurrence_dict_map[num_classes][cls] = 1

for i in range(1,7):
    print(i, 'occurence')
    print (occurrence_dict_map[i])

new_df = pd.DataFrame(rows, columns=['Prompt', 'Reply', 'Subclass'])
new_df.to_excel('method_singlelbl_subclass.xlsx', index=False)

# Go for checking methods
# Do classification on method class and its subclass
# method is the most important class

# make github repo and share with professor
# get examples where get and put
