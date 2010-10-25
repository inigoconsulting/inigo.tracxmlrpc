import sys
import os
import tempfile

from argparse import ArgumentParser

def indent(text):
    result = []
    for l in text.split('\n'):
        result.append('  | ' + l)
    return '\n'.join(result)

def editor_input(message):
    ignorestart = '--This line, and those below, will be ignored--'
    tmp = tempfile.mktemp(suffix='.tmp',prefix='tracrpc')
    f = open(tmp,'w')
    f.write('\n\n%s\n\n%s' % (ignorestart,message))
    f.close()

    os.system('%s %s' % (os.environ['EDITOR'],tmp))
    out = open(tmp).readlines()

    ignoreindex = out.index('%s\n' % ignorestart)
    out = out[0:ignoreindex]

    os.unlink(tmp)
    return ''.join(out)

def selection_input(message,options):
    input = -1
    print message
    while not input in range(0,len(options)):
         count = 0
         for item in options:
             print "  %s. %s" % (count,item)
             count += 1
         try:
            input = int(raw_input(">> "))
         except: pass
    return options[input]

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('project', metavar='project', help='Project Name')
    parser.add_argument('-u', '--username', dest='username', 
                help='Your trac login username')
    parser.add_argument('-p', '--password', dest='password',
                help='Your trac login password')
    return parser
