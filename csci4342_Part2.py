"""
Student Name: Keith Neill
Program Name: Interpreter Project Part 1
Description: This program reads a file with SFAscal code and displays the type of token associated with each lexeme. 
             This program displays the output as lexeme : token name. for example, the output “x : Identifier Token” tells the user that the lexeme, x, is an identifier token.  
"""

import sys
import re

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

# determine what type of token each lexeme is
for lexeme in lexemes:
    if lexeme in reserved_tokens_list:
        print(lexeme,": Reserved Token")
    elif lexeme in data_type_tokens_list:
        print(lexeme, ": Data Type Token")
    elif lexeme in boolean_tokens_list:
        print(lexeme, ": Boolean Token")
    elif lexeme in special_tokens_list:
        print(lexeme, ": Special Token")
    elif lexeme == ":=":
        print(lexeme, ": Assignment Token")
    elif lexeme in relation_tokens_list:
        print(lexeme, ": Relation Token")
    elif lexeme in addition_tokens_list:
        print(lexeme, ": Addition Token")
    elif lexeme in multiplication_tokens_list:
        print(lexeme, ": Multiplication Token")
    elif integer_type_token.fullmatch(lexeme):
        print(lexeme, ": Integer Token")
    elif identifier_token.fullmatch(lexeme):
        print(lexeme, ": Identifier Token")
    else:
        print(lexeme, ": Invalid")