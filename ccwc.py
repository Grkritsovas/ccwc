#!/usr/bin/env python
import sys
import fileinput
import re

def byte_count(input_data):
    #if the input_data is from stdin(pipe) the try will throw an error and the code in the except close will execute
    try:
        #open file in read + binary mode
        with open(input_data, 'rb') as f:
            res = 0
            #reading the f one byte at a time while the returned value is a non-empty byte
            #the walrus operator(':=') is used to assign the value to byte like so: byte = f.read(1) and at the same
            #returns the value being assigned.The TLDR for the walrus operator: It’s an operator used in assignment expressions,
            #which can return the value being assigned, unlike traditional assignment statements. See more on:
            #https://realpython.com/python-walrus-operator/#:~:text=Each%20new%20version%20of%20Python,known%20as%20the%20walrus%20operator.
            while byte := f.read(1):
                res += 1

            return res
    except:
        #byte_count when we take the input_data from the pipe can be calculated from the length of the encoded input_data
        #the reason we also add the line_count is cause the '\n' characters are not included in the encoded form of input_data
        #but they should still be calculated to accurately depict how many bytes the input represents.
        byte_count = len(input_data.encode()) + line_count(input_data)
        return byte_count

def line_count(input_data):
    try:
        res = 0
        with open(input_data, 'rb') as f:
            # for i in f -> i is the line in f. so we add +1 for each line in our file.
            for line in f:
                res += 1

        return res
    except:
        res = 0
        for line in input_data.splitlines():
            res += 1

        return res
    
def word_count(input_data):
    try:
        res = 0
        #open the file in normal text mode for read (would be the same to use open(input_data,'r'))
        with open(input_data, 'rt') as f:
            #f.read() reads the whole file. Splitting it on spaces gives us the amound of words.
            read_data = f.read()
            words = read_data.split()
            res = len(words)
        return res
    except:
        words = input_data.split()
        return len(words)

def char_count(input_data):
    try:
        res = 0
        with open(input_data, 'rt') as f:
            read_data = f.read()
            res = len(read_data)
        #the length of read_data doesn't take account of the '\n' as characters, so we add them by calling the line_count
        return res + line_count(input_data)
    except:
        return len(input_data) + line_count(input_data)

def main():
    try:
        input_data = ''
          
        inp_from_pipe = False
        # Returns True if input is from pipe
        if not sys.stdin.isatty():
            input_data = sys.stdin.read()
            inp_from_pipe = True
        else:
            input_data = sys.argv[-1]
            
            if '.' not in input_data:
                print('Invalid file input. Type ccwc -h if you would like help on the proper syntax for ccwc')
                exit()
            #providing the help tool for how to use the ccwc command line tool
            if sys.argv[0] == 'ccwc.py' and sys.argv[1] == '-h':
                print('')
                print('CCWC helptool:')
                print('')
                print('If you are trying to input data from a pipe use this syntax for windows("for unix use cat instead of type"):')
                print('--If you want to find the line_count, word_count as well as the byte_count for the input:')
                print('----type file_name.txt | ccwc')
                print('--If you want only the byte_count, line_count,word_count or character_count use these respectfully:')
                print('----type file_name.txt | ccwc -c/-l/-w/-m')
                print('If you are trying to input data from a file:')
                print('--If you want to find the line_count, word_count as well as the byte_count for the input file:')
                print('----ccwc file_name_or_path.txt')
                print('--If you want only the byte_count, line_count,word_count or character_count use these respectfully:')
                print('----ccwc -c/-l/-w/-m file_name_or_path.txt')
                exit()

        if inp_from_pipe and len(sys.argv) > 2:
            print('Improper use of the command line tool. Type ccwc -h if you would like help on the proper syntax for ccwc')
            exit()

        if len(sys.argv) > 3:
            #There is no reason for more than 3 characters for the use off ccwc, so in that case we refer to the help tool
            print('Improper use of the command line tool. Type ccwc -h if you would like help on the proper syntax for ccwc')
            exit()

        #if inp is form pipe, then the length of the sys.argv which is the typed command line after the pipe, should be
        #equal to 2 : | ccwc -c, cause if no command is specified the length is 1, since there is one less arguement
        #than in the file input method of input, the name-path of the file.
        if len(sys.argv) > 2 or (inp_from_pipe and len(sys.argv) == 2):               
            cmd = sys.argv[1]

            if cmd == '-c':
                print(byte_count(input_data))
            elif cmd == '-l':
                print(line_count(input_data))
            elif cmd == '-w':
                print(word_count(input_data))
            elif cmd == '-m':
                print(char_count(input_data))          
            else:
                print('Error: Missing command-line arguments. Please provide one of those commands: -c / -l /-w /-m')
        else:
            if len(sys.argv) > 1 and inp_from_pipe:
                print('Improper use of the command line tool. Type ccwc -h if you would like help on the proper syntax for ccwc')
                exit()

            print(line_count(input_data), word_count(input_data), byte_count(input_data))
    #catches any unexpected errors      
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()