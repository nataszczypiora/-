from SQLLexer import MySqlLexer

def random_sort_antipattern(tokens):
    if 'TOP' in tokens and 'NEWID' in tokens:
        return True
    return False

def select_all_antipattern(tokens):
    if 'ALL' in tokens:
        return True
    return False

def search_by_regex_antipattern(tokens):
    if 'REGEX' in tokens:
        return True
    return False

def search_by_empty_string_as_null_antipattern(tokens):
    for i in range(0, len(tokens)):
        if (tokens[i] == 'EQUAL' or tokens[i] == 'NOT_EQUAL') and tokens[i+1] == 'EMPTY_STRING':
            return True
    return False

'''
SELECT * FROM TABLE cat FULL JOIN owner ON owner.cat = cat.id WHERE owner NOT NULL
'''
def search_full_join_antipattern(tokens):
    is_full_join = False
    for i in range(0, len(tokens)):
        if tokens[i] == 'FULL' and tokens[i+1] == 'JOIN':
            is_full_join = True
        if tokens[i:i+3] == ['VARIABLE', 'EQUAL', 'VARIABLE'] and is_full_join:
            return True


    return False
f = open('test_file.txt', 'r')
content = f.read()
myParser = MySqlLexer()

myParser.build()
myParser.set_input("SELECT TOP 1 * FROM Countries ORDER BY NEWID();")
tokens = myParser.get_tokens_as_list()

output = random_sort_antipattern(tokens)

print(output)

myParser.set_input("SELECT * FROM Countries;")
tokens = myParser.get_tokens_as_list()

output = select_all_antipattern(tokens)

print(output)

myParser.set_input("""SELECT * FROM Email, Addresses WHERE Email ~* "*QWER";""")
tokens = myParser.get_tokens_as_list()

output = search_by_regex_antipattern(tokens)

print(output)

myParser.set_input("""SELECT * FROM Email WHERE CAT_NAME = "MRUCZEK" AND Email = "";""")
tokens = myParser.get_tokens_as_list()
output = search_by_empty_string_as_null_antipattern(tokens)
print(output)

myParser.set_input("""SELECT * FROM TABLE cat FULL JOIN owner ON owner.cat = cat.id WHERE owner NOT NULL;""")
tokens = myParser.get_tokens_as_list()
output = search_full_join_antipattern(tokens)
print(output)