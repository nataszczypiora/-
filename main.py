import json

from SQLLexer import MySqlLexer

def random_sort_antipattern(tokens):
    if 'TOP' in tokens and 'NEWID' in tokens:
        return True
    return False

def select_all_antipattern(tokens):
    for i in range(0, len(tokens)-1):
        if tokens[i] != 'L_PARENTIS' and tokens[i] != 'COUNT' and tokens[i+1] == 'ALL':
            return True
    return False

def search_by_regex_antipattern(tokens):
    if 'REGEX' in tokens:
        return True
    return False

def search_by_empty_string_as_null_antipattern(tokens):
    for i in range(0, len(tokens)-1):
        if (tokens[i] == 'EQUAL' or tokens[i] == 'NOT_EQUAL') and tokens[i+1] == 'EMPTY_STRING':
            return True
    return False

'''
SELECT * FROM TABLE cat FULL JOIN owner ON owner.cat = cat.id WHERE owner NOT NULL
'''
def search_full_join_antipattern(tokens):
    is_full_join = False
    for i in range(0, len(tokens) - 1):
        if tokens[i] == 'FULL' and tokens[i+1] == 'JOIN':
            is_full_join = True
        if tokens[i:i+3] == ['VARIABLE', 'EQUAL', 'VARIABLE'] and is_full_join:
            return True


    return False
f = open('sql_data.txt', 'r')
content = f.readlines()
myParser = MySqlLexer()
myParser.build()

query_counter = 0
antipatterns = [0, 0, 0, 0, 0]
random_sorts = []
select_alls = []
search_by_regexes = []
search_by_empty_strings = []
full_join_wheres = []
result = []

for i in content:
    myParser.set_input(i.replace('\n', ''))
    tokens = myParser.get_tokens_as_list()
    if random_sort_antipattern(tokens):
        random_sorts.append(i)
        antipatterns[0] += 1
    if select_all_antipattern(tokens):
        select_alls.append(i)
        antipatterns[1] += 1
    if search_by_regex_antipattern(tokens):
        search_by_regexes.append(i)
        antipatterns[2] += 1
    if search_by_empty_string_as_null_antipattern(tokens):
        antipatterns[3] += 1
        search_by_empty_strings.append(i)
    if search_full_join_antipattern(tokens):
        antipatterns[4] += 1
        full_join_wheres.append(i)

    query_counter += 1

result.append({"antipattern": "random_sort", "cases": random_sorts, "count": antipatterns[0]})
result.append({"antipattern": "select_all", "cases": select_alls, "count": antipatterns[1]})
result.append({"antipattern": "search_by_regex", "cases": search_by_regexes, "count": antipatterns[2]})
result.append({"antipattern": "search_by_empty_string", "cases": search_by_empty_strings, "count": antipatterns[3]})
result.append({"antipattern": "search_full_join", "cases": full_join_wheres, "count": antipatterns[4]})

res_file = open("result.json", 'w')
res_file.write(json.dumps(result))

print(f'Out of {query_counter} queries we have: ')
print(f'{antipatterns[0]} random sorts')
print(f'{antipatterns[1]} select alls')
print(f'{antipatterns[2]} searches by regex')
print(f'{antipatterns[3]} searches by empty string')
print(f'{antipatterns[4]} searches by full join')
