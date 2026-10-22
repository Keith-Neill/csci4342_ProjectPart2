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

# <program>
def program(i):
    if lexemes[i] == "program":
        i = i+1 # consumed input "program" increment i
        print(i)
        i = identifier(i)
        print(i)
        if lexemes[i] == ";":
            i = i+1
        else:
            print("Error: ';' is expected. Fornd'", lexemes[i], "'instead.")
            sys.exit(1)
        print(i)
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
        print(lexeme,": Reserved Token")
        lexeme_tokens.append("Reserved Token")
    elif lexeme in data_type_tokens_list:
        print(lexeme, ": Data Type Token")
        lexeme_tokens.append("Date Type Token")
    elif lexeme in boolean_tokens_list:
        print(lexeme, ": Boolean Token")
        lexeme_tokens.append("Boolean Token")
    elif lexeme in special_tokens_list:
        print(lexeme, ": Special Token")
        lexeme_tokens.append("Special Token")
    elif lexeme == ":=":
        print(lexeme, ": Assignment Token")
        lexeme_tokens.append("Assignment Token")
    elif lexeme in relation_tokens_list:
        print(lexeme, ": Relation Token")
        lexeme_tokens.append("Relation Token")
    elif lexeme in addition_tokens_list:
        print(lexeme, ": Addition Token")
        lexeme_tokens.append("Addition Token")
    elif lexeme in multiplication_tokens_list:
        print(lexeme, ": Multiplication Token")
        lexeme_tokens.append("Multiplication Token")
    elif integer_type_token.fullmatch(lexeme):
        print(lexeme, ": Integer Token")
        lexeme_tokens.append("Integer Token")
    elif identifier_token.fullmatch(lexeme):
        print(lexeme, ": Identifier Token")
        lexeme_tokens.append("Identifier Token")
    else:
        print(lexeme, ": Invalid")

#print(lexeme_tokens)

# time to put the input through the grammar using the tokens and the lexemes list
i = 0
print(i)
program(i)
