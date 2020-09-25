import pandas as pd
from pprint import PrettyPrinter
import re

df =  pd.read_csv('../data/indeed_df.csv')

skills = ['Python', 'R', 'SQL', 'NoSQL', 'GIT', 'Spark', 'Flask', 'Streamlit', 
          'Docker', 'Kubernetes', 'ReactJS', 'Machine Learning', 'Deep Learning',
          'NLP', 'VueJS', 'AngularJS', 'Scala', 'PySpark', 
          'PowerBI', 'SQLServer', 'Dataiku', 'Keras', 'TensorFlow', 'NLU', 'Pytorch',  
          'ScikitLearn', 'Scikit-Learn', 'SAS', 'Java', 'Scikit learn', 'Hadoop',
          'Hive', 'ML DL', 'Azure', 'AWS', 'NoSQL', 'mysql', 'postgresql']

'''
Replace a set of multiple sub strings with a new string in main string.
'''
def replaceMultiple(mainString, toBeReplaces, newString):
    # Iterate over the strings to be replaced
    for elem in toBeReplaces :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString

'''
Created list of list of word for each description
'''
def description_tolist(column_df):
    txt = column_df
    desc = txt.tolist()
    #print(desc)
    desc_list = [replaceMultiple(desc[i], [':', '-', '.','(',')','\n', '/'], ' ') for i in range(len(desc))]
    desc_list = [re.sub(r'\W', ' ', desc_list[i])for i in range(len(desc_list))] #sub(pattern, repl, string[, count, flags])
    desc_list = [elem.lower().split() for elem in desc_list]
    return desc_list

'''
Return commons elements between two list of word
'''
def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    skills_unique = list(set(result)) 
    return skills_unique

'''
Convert dataframe to json file
'''
def df_to_json(df):
    result = df.to_json(orient="index")
    parsed = json.loads(result)
    new_files = json.dumps(parsed, indent=2)
    #new_file = re.sub(r"\n", '', new_files)
    #new_file = re.sub(r"^\s+", '', new_files)
    new_file = new_files.replace('\n', '')    # do your cleanup here
    return new_file

keyword_list = [elem.lower() for elem in skills]
desc_list = description_tolist(df['Descriptions'])
skills_jobcard = [common_elements(desc_list[i], keyword_list) for i in range(len(desc_list))]
print(skills_jobcard)
print(len(skills_jobcard))
print(len(desc_list))

df['Skills'] = skills_jobcard

# All str in lower except Links
df2 = df.apply(lambda x: x.astype(str).str.lower())
df2['Links'] = df['Link']
del df2['Link']

new_file = df_to_json(df)

pp = PrettyPrinter()
pp.pprint(new_file)
