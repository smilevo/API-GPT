import pandas as pd

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

for classes in df["Class"]:
    # split the string by commas to get individual classes
    class_list = [cls.strip() for cls in classes.split(',') if cls.strip()]
    
    # get the number of classes and increment count
    num_classes = len(class_list)
    occurrence_dict_map[num_classes]['count'] += 1

    for cls in class_list:
        if cls in occurrence_dict_map[num_classes]:
            occurrence_dict_map[num_classes][cls] += 1
        else:
            occurrence_dict_map[num_classes][cls] = 1

for i in range(1,7):
    print(i, 'occurence')
    print (occurrence_dict_map[i])


# Go for checking methods
# Do classification on method class and its subclass

# method is the most important class