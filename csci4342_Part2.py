"""
Student Name: Keith Neill
Program Name: Interpreter Project Part 2
Description: This program reads a file with SFAscal code and displays the type of token associated with each lexeme. 
             This program displays the output as lexeme : token name. for example, the output “x : Identifier Token” tells the user that the lexeme, x, is an identifier token.  
"""

import sys
import re

# <identifier>
def identifier(i):
    if lexeme_tokens[i] == "Identifier Token":
        # if lexeme is an identifier, consume it by incrementing i by 1 and return i
        i = i+1
        return i
    else:
        print("Error: expected an identifier token, got", lexeme_tokens[i], "instead. '",lexemes[i],"' is not a valid identifier.")
        sys.exit(1)

# <factor>
def factor(i):

    # if "(<expression>)"
    if lexemes[i] == "(":
        i = i+1 # consume (
        i = expression(i)
        if lexemes[i] == ")":
            i = i+1 # consume )
            return i
        else:
            print("Error: Expected ')' after expression.")
            sys.exit(1)

    if lexeme_tokens[i] == "Integer Token" or lexeme_tokens[i] == "Boolean Token":
        
        i = i+1 # <constant>
    
    elif lexemes[i] == "not":
        
        i = i+1 # consume "not"
        i = factor(i)
    elif lexeme_tokens[i] == "Identifier Token":
        i = identifier(i)
    else:
        print("Error: ", lexemes[i], "cannot be a factor")
        sys.exit(1)

    return i

# <term>
def term(i):
    i = factor(i)
    if lexeme_tokens[i] == "Multiplication Token":
        multiply_more_factors = True
    else:
        multiply_more_factors = False
    
    while multiply_more_factors:
        i = i+1 # consume multiplication lexeme
        i = factor(i)
        if lexeme_tokens[i] != "Multiplication Token":
            multiply_more_factors = False
    
    return i

# <simple expression>
def simple_expression(i):
    i = term(i)
    if lexeme_tokens[i] == "Addition Token":
        add_more_terms = True
    else:
        add_more_terms = False
        
    while add_more_terms:
        i = i+1 # consume addition lexeme
        i = term(i)
        if lexeme_tokens[i] != "Addition Token":
            add_more_terms = False
        
    return i


# <expression>
def expression(i):
    i = simple_expression(i)
    if lexeme_tokens[i] == "Relation Token":
        i = i+1 # consume lexeme with relation token
        i = simple_expression(i)
    return i

# <assignment statement>
def assignment_statement(i):
    i = identifier(i)
    if lexeme_tokens[i] == "Assignment Token":
        i = i+1
    else:
        print("Error: Expected Assignment Token, got", lexeme_tokens[i], "instead.")
        sys.exit(1)

    i = expression(i)
    
    return i


# <read statement>
def read_statement(i):
    i = i+1 # consume "read"
    i = i+1 # consume (
    i = identifier(i)
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after read statement")
        sys.exit(1)
    
    return i

# <write statement>
def write_statement(i):
    i = i+1 # consume "write"
    i = i+1 # consume (
    i = expression(i) # <output value>
    if lexemes[i] == ")":
        i = i+1 # consume )
    else:
        print("Error: ')' is expected after write statement")
        sys.exit()
    return i

# <simple statement>
def simple_statement(i):
    
    if lexeme_tokens[i] == "Identifier Token" and lexeme_tokens[i+1] == "Assignment Token":
       i = assignment_statement(i)
    elif lexeme_tokens[i] == "Identifier Token":
        i = identifier(i) # <procedure statement>
    elif lexemes[i] == "read":
        i = read_statement(i)
    elif lexemes[i] == "write":
        i = write_statement(i)
    else:
        print("Error: ",lexemes[i],"is not recognised as a statement.")
        sys.exit(1)
       
    return i


# <if statement>
def if_statement(i):
    i = i+1 # consume "if"
    i = expression(i)
    if lexemes[i] == "then":
        i = i+1 # consume then
    else:
        print("Error: Expected 'then' after if statenent.")
        sys.exit(1)
    i = statement(i)
    if lexemes[i] == "else":
        i = i+1 # consume else
        i = statement(i)
    return i

# <while statement>
def while_statement(i):
    i = i+1 # consume while
    i = expression(i)
    if lexemes[i] == "do":
        i = i+1 # consume do
    else:
        print("Error: Expected 'do' after exopression in while statement.")
        sys.exit(1)
    i = statement(i)
    return i

# <structured statenebt>
def structured_statement(i):
    if lexemes[i] == "begin":
        i = compound_statement(i)
    elif lexemes[i] == "if":
        i = if_statement(i)
    elif lexemes[i] == "while":
        i = while_statement(i)
    else:
        print("Error: ",lexemes[i], " is not recognised as a structured statement.")
    return i

# <statement>
def statement(i):
    
    if lexeme_tokens[i] == "Identifier Token" or lexemes[i] == "read" or lexemes[i] == "write":
        i = simple_statement(i)
    elif lexemes[i] == "begin" or lexemes[i] == "if" or lexemes[i] == "while":
        i = structured_statement(i)
    elif lexemes[i] == "end" or lexemes[i] == ";":
        return i # <empty statement>
    else:
        print("Error: ", lexemes[i], "is not the start of a valid statement.")
        sys.exit(i)

    return i

# <compound statement>
def compound_statement(i):
    if lexemes[i] == "begin":
        i = i+1 # consume "begin"
        
    else:
        print("Error: Expected lexene 'begin', got", lexemes[i], "instead")
        sys.exit(1)

    i = statement(i)
    
    if lexemes[i] == ";":
       more_statements = True
    else:
        more_statements = False

    while more_statements:
        i = i+1 # consume ;
        i = statement(i)
        if lexemes[i] == "end" or lexemes[i] != ";":
            more_statements = False

    if lexemes[i] != "end" and (lexeme_tokens[i] == "Identifier Token" or lexeme_tokens[i] == "Reserved Token"):
        print("Error: Expected ';' in between statements")
        sys.exit(1)
    elif lexemes[i] != "end":
        print("Expected 'end' after compound statement.")
        sys.exit(1)
    else:
        i = i + 1 # consume end

    return i

# <statement part>
def statement_part(i):
    i = compound_statement(i)
    return i

#  <procedure block>
def procedure_block(i):
    i = variable_declarition_part(i)
    i = statement_part(i)

    return i

# <procedure declaration>
def procedure_declaration(i):
    i = i+1 # consume "procedure"
    i = identifier(i)
    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexemes[i], "instead")
        sys.exit(1)

    i = procedure_block(i)

    return i

# <procedure declaration part>
def procedure_declaration_part(i):
    if lexemes[i] == "procedure":
        more_procedure_declarations = True
    else:
        more_procedure_declarations = False

    while more_procedure_declarations:
        i = procedure_declaration(i)
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexemes[i], "instead")
            sys.exit(1)
        if lexemes[i] != "procedure":
            more_procedure_declarations = False
    return i
        

# <simple type>
def simple_type(i):
    if lexeme_tokens[i] == "Data Type Token":
        i = i+1 # consume data type
    else:
        print("Error: Expected a Data Type Token, got a ", lexeme_tokens[i], " instead. Lexeme ", lexemes[i], " is not a Data Type Token.")
        sys.exit(1)
    return i

# <type>
def type(i):
    i = simple_type(i)
    return i

#<variable declaration>
def variable_declaration(i):
       
    i = identifier(i)

    if lexemes[i] == "," and lexeme_tokens[i+1] == "Identifier Token":
        more_identifiers = True
    else:
        more_identifiers = False
    
    while more_identifiers:
        if lexemes[i] != ",":
            print("Error: A ',' is expected, got lexeme ", lexemes[i], "instead.")
            sys.exit(1)
        
        i = i+1 # consume ","
        i = identifier(i)

        if lexemes[i] != "," and lexeme_tokens[i+1] != "Identifier Token":
            more_identifiers = False
    
    if lexemes[i] == ":":
        i = i+1 # consume the ":" lexeme
    else:
        print("Error: Expect a ':', got",lexemes[i], "instead.")
        sys.exit(1)

    i = type(i)
    
    return i

# <variable declaration part>
def variable_declarition_part(i):
    if lexemes[i] == "var":
        i = i+1 # consume "var"
    else:
        # if the current lexeme isn't i, go back to block() function. <variable declaration part> -> empty string
        return i
    
    i = variable_declaration(i)

    if lexemes[i] == ";":
        i = i+1 # consume ";"
    else:
        print("Error: Expected a ';', got", lexeme[i], "instead")
        sys.exit(1)

    if lexeme_tokens[i] == "Identifier Token":
        more_variable_declaritions = True
    else:
        more_variable_declaritions = False
    
    while more_variable_declaritions:
        
        i = variable_declaration(i)
        if lexemes[i] == ";":
            i = i+1 # consume ";"
        else:
            print("Error: Expected a ';', got", lexeme[i], "instead")
            sys.exit(1)
        if lexeme_tokens[i] != "Identifier Token":
            more_variable_declaritions = False
        
    return i
    

# <block>
def block(i):
    
    i = variable_declarition_part(i)
    i = procedure_declaration_part(i)
    i = statement_part(i)
    return i


# <program>
def program(i):
    if lexemes[i] == "program":
        i = i+1 # consumed input "program" increment i by 1
        i = identifier(i)
        if lexemes[i] == ";":
            i = i+1
        else:
            print("Error: ';' is expected. Fornd'", lexemes[i], "'instead.")
            sys.exit(1)
        
        i = block(i)

        if i > len(lexemes) - 1:
            print("Error: Expect '.' after last 'end'.")
        elif lexemes[i] != "." or i < len(lexemes) - 1:
            print("Error: There cannot be anything after the last 'end' in the program.")
        else:
            print("Parse successful.")

    else:
        print("Error: expected 'program', found'" ,lexemes[i], "'instead")
        sys.exit(1)
        



if len(sys.argv) != 2:
    print("Invalid number of arguments. You must specify a file for the input.")
    sys.exit(1)

input_file_name = sys.argv[1]

# read lexeams from the file into a list
try:
    with open(input_file_name, 'r') as f:
        lexemes = f.read().split()
# when the file does not exist or is not in the directory of the program file
except:
    print("Error: The input file does not exist in the same directory as this program.")
    sys.exit(1)

# define each type of tokens
reserved_tokens_list = {"program" , "var", "procedure", "begin", "end", "if", "then", "else", "while", "do", "read", "write", "not", "array", "of"}
data_type_tokens_list = {"integer", "boolean"}
boolean_tokens_list = {"true", "false"}
special_tokens_list = {"(", ")", "[", "]", ".", ",", ";", ":", ".."}
relation_tokens_list = {"=", "<>", "<", "<=", ">=", ">"}
addition_tokens_list = {"+", "-", "or"}
multiplication_tokens_list = {"*", "div", "and"}
integer_type_token = re.compile("[0-9]+") # any number at any length with digits from 0 - 9
identifier_token = re.compile("^[A-Za-z]([A-Za-z]|[0-9])*") # must begin with a capital or lower case letter. Can end with letter or digit. Can be as long as needed
lexeme_tokens = []

# determine what type of token each lexeme is
for lexeme in lexemes:
    if lexeme in reserved_tokens_list:
        lexeme_tokens.append("Reserved Token")
    elif lexeme in data_type_tokens_list:
        lexeme_tokens.append("Data Type Token")
    elif lexeme in boolean_tokens_list:
        lexeme_tokens.append("Boolean Token")
    elif lexeme in special_tokens_list:
        lexeme_tokens.append("Special Token")
    elif lexeme == ":=":
        lexeme_tokens.append("Assignment Token")
    elif lexeme in relation_tokens_list:
        lexeme_tokens.append("Relation Token")
    elif lexeme in addition_tokens_list:
        lexeme_tokens.append("Addition Token")
    elif lexeme in multiplication_tokens_list:
        lexeme_tokens.append("Multiplication Token")
    elif integer_type_token.fullmatch(lexeme):
        lexeme_tokens.append("Integer Token")
    elif identifier_token.fullmatch(lexeme):
        lexeme_tokens.append("Identifier Token")
    else:
        print(lexeme, "is not associated with a valid token.")
        sys.exit(1)

# time to put the input through the grammar using the tokens and the lexemes list
i = 0 # start at position 0 in the lists
program(i)
