import json

from random import sample


data_file = open("result.json", 'r')
json_data = json.load(data_file)

for i in json_data:
    sample_data = open(f'{i["antipattern"]}.txt', 'w')
    sample_data.write(f'Antipattern {i["antipattern"]}')
    for j in sample(i["cases"], min(len(i["cases"]),30)):
        sample_data.write(j)
    sample_data.close()

