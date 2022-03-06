import ply.lex as lex
import ply.yacc as yacc


class MySqlLexer(object):
    reserved = {
        'SELECT': 'SELECT',
        'FROM': 'FROM',
        'COUNT': 'COUNT',
        'JOIN': 'JOIN',
        'LEFT': 'LEFT',
        'RIGHT': 'RIGHT',
        'FULL': 'FULL',
        'NOT': 'NOT',
        'NULL': 'NULL',
        'INNER': 'INNER',
        'OUTER': 'OUTER',
        'ON': 'ON',
        'WHERE': 'WHERE',
        'BETWEEN': 'BETWEEN',
        'LIKE': 'LIKE',
        'IN': 'IN',
        'ORDER': 'ORDER',
        'GROUP': 'GROUP',
        'BY': 'BY',
        'HAVING': 'HAVING',
        "DISTINCT": "DISTINCT",
        "DESC": "DESC",
        "ASC": 'ASC',
        "LIMIT": "LIMIT",
        "OFFSET": "OFFSET",
        "TOP": "TOP",
        "NEWID": "NEWID",
    }

    tokens = [
                 'END',
                 'VARIABLE',
                 'ANY',
                 'EQUAL',
                 'NOT_EQUAL',
                 'COMMA',
                 'LESS',
                 'MORE',
                 'LESS_EQ',
                 'MORE_EQ',
                 'ALL',
                 'NUMBER',
                 'L_PARENTIS',
                 'R_PARENTIS',
                 'L_SQUARE_PARENTIS',
                 'R_SQUARE_PARENTIS',
                 'L_BRACE',
                 'R_BRACE',
                 'REGEX',
                 'EMPTY_STRING',
                 'QUOTE',
                 'PLUS',
                 'MINUS',
                 'UNDERSCORE',
                 'HASH',
                 'SLASH',
                 'SCREAM',
                 'QUESTION_MARK',
                 'DOUBLE_DOTS',
                 'DOLLAR',
                 'HAT',
                 'DASH',
                 'GERUND',
                 'FENCE',
                 'LINUX_HOME',
                 'SINGLE_CHAR'
             ] + list(reserved.values())

    t_ALL = r'\*'
    t_EQUAL = r'\='
    t_NOT_EQUAL = r'\!='
    t_LESS = r'\<'
    t_MORE = r'\>'
    t_LESS_EQ = r'\<='
    t_MORE_EQ = r'\>='
    t_NUMBER = r'[0-9]+'
    t_ignore = ' \t\'%@.'
    t_COMMA = r','
    t_END = r';'
    t_L_PARENTIS = r'\('
    t_R_PARENTIS = r'\)'
    t_L_SQUARE_PARENTIS = r'\['
    t_R_SQUARE_PARENTIS = r'\]'
    t_L_BRACE = r'\{'
    t_R_BRACE = r'\}'
    t_EMPTY_STRING = r'\""'
    t_QUOTE = r'\"'
    t_REGEX = r'\~\*'
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_UNDERSCORE = r'\_'
    t_ANY = r'[a-zA-Z][a-zA-Z0-9]'
    t_HASH = r'\#'
    t_SLASH = r'\/'
    t_SCREAM = r'\!'
    t_QUESTION_MARK = r'\?'
    t_DOUBLE_DOTS = r'\:'
    t_DOLLAR = r'\$'
    t_HAT = r'\^'
    t_DASH = r'–'
    t_GERUND = r'\`'
    t_FENCE = r'\|'
    t_LINUX_HOME = r'\~'
    t_SINGLE_CHAR = r'.'

    def __init__(self):
        self.lexer = None
        self.parser = None
        self.select_trees = []

    def t_VARIABLE(self, t):
        r"[a-zA-Z][a-zA-Z0-9]*"
        t.type = MySqlLexer.reserved.get(t.value, 'VARIABLE')  # Check for reserved words
        t.value = t.value.lower()
        return t

    # def t_ANY(self, t):
    #     r"[a-zA-Z][a-zA-Z0-9]*"
    #     return t

    def t_error(self, t):
        print("Invalid Token:", t.value[0])
        t.lexer.skip(1)

    def p_program(self, p):
        """
            program : select_tree END
                | program select_tree END
        """
        return p

    def p_select(self, p):
        """
            select_tree : SELECT ARGS FROM_PARSE
                | SELECT TOP_C FROM_PARSE
                | SELECT ALL FROM_PARSE
        """
        return p

    def p_FROM_PARSE(self, p):
        """
            FROM_PARSE : FROM ARGS
                | FROM ARGS ADDITIONAL_CLAUSES
        """
        return p

    def p_ADDITIONAL_CLAUSES(self, p):
        """
            ADDITIONAL_CLAUSES : JOIN_C ADDITIONAL_CLAUSES
                | WHERE_C ADDITIONAL_CLAUSES
                | GROUP_BY_C ADDITIONAL_CLAUSES
                | HAVING_C ADDITIONAL_CLAUSES
                | ORDER_BY_C ADDITIONAL_CLAUSES
                | LIMIT_C ADDITIONAL_CLAUSES
                | OFFSET_C ADDITIONAL_CLAUSES
                | JOIN_C
                | WHERE_C
                | GROUP_BY_C
                | HAVING_C
                | ORDER_BY_C
                | LIMIT_C
                | OFFSET_C
        """
        return p

    def p_JOIN_C(self, p):
        """
            JOIN_C : INNER JOIN_C
                | LEFT JOIN_C
                | RIGHT JOIN_C
                | FULL JOIN_C
                | OUTER JOIN_C
                | JOIN ARGS JOIN_C
                | ON VARIABLE
                | ON VARIABLE EQUAL VARIABLE
        """
        return p

    def p_WHERE_C(self, p):
        """
            WHERE_C : WHERE CONDITION
        """
        return p

    def p_HAVING_C(self, p):
        """
            HAVING_C : HAVING CONDITION
        """
        return p

    def p_CONDITION(self, p):
        """
            CONDITION : VARIABLE OPERATOR MATCH
        """
        return p

    def p_MATCH(self, p):
        """
            MATCH : QUOTE ANY QUOTE
                | VARIABLE
                | EMPTY_STRING
        """
        pass

    def p_GROUP_BY_C(self, p):
        """
            GROUP_BY_C : GROUP BY VARIABLE
        """
        return p

    def p_INNER_SELECT_C(self, p):
        """
            INNER_SELECT_C : L_PARENTIS SELECT ARGS FROM_PARSE R_PARENTIS
        """
        return p

    def p_ORDER_BY_C(self, p):
        """
            ORDER_BY_C : ORDER BY VARIABLE
                | ORDER BY VARIABLE DESC
                | ORDER BY VARIABLE ASC
                | ORDER BY NEWID_C
        """
        return p

    def p_LIMIT_C(self, p):
        """
            LIMIT_C : LIMIT NUMBER
        """
        return p

    def p_OFFSET_C(self, p):
        """
            OFFSET_C : OFFSET NUMBER
        """
        return p

    def p_ARG_LIST(self, p):
        """
            ARGS : ARGS COMMA VARIABLE
                | ARGS VARIABLE
                | DISTINCT VARIABLE
                | INNER_SELECT_C
                | VARIABLE
                | P_COUNT
        """
        return p

    def p_COUNT(self, p):
        """
            P_COUNT : COUNT L_PARENTIS ALL R_PARENTIS
                | COUNT VARIABLE
        """

    def p_OPERATOR(self, p):
        """
            OPERATOR : LESS
                | MORE
                | EQUAL
                | NOT_EQUAL
                | MORE_EQ
                | LESS_EQ
                | BETWEEN
                | LIKE
                | IN
                | REGEX
        """
        return p

    def p_NEWID_C(self, p):
        """
            NEWID_C : NEWID L_PARENTIS R_PARENTIS
        """
        return p

    def p_TOP_C(self, p):
        """
            TOP_C : TOP NUMBER ARGS
        """
        return p

    def p_error(self, p):
        print("Error:  ", p)

    def build(self):
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def set_input(self, input_data):
        self.lexer.input(input_data)

    def get_tokens(self):
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            print(tok)

    def get_tokens_as_list(self):
        token_list = []
        start_quote = False
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            else:
                if tok.type == 'QUOTE':
                    start_quote = not start_quote

                if not start_quote:
                    if tok.type == 'QUOTE':
                        token_list.append('STRING_PHASE')
                    else:
                        token_list.append(tok.type)
        return token_list

    def parse(self, p):
        self.parser.parse(p)
