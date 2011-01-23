import sys
import os
import tempfile

from argparse import ArgumentParser
import keyring

COLOR_MAP = {
   'red': 31,
   'green': 32,
   'yellow': 33,
   'blue': 34,
   'purple': 35,
   'white': 1
}

KEYRING_SERVICE='inigo.tracxmlrpc.scripts'

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

def get_auth(user, passwd):
    if not user:
        username = raw_input('Username: ')
    if not passwd:
        passwd = keyring.get_password(KEYRING_SERVICE, user)
        if passwd is None:
            passwd = getpass.getpass('Password: ')
            keyring.set_password(KEYRING_SERVICE, user, passwd)
    return user, passwd

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

def colored(text, color='default', bold=False):
    b = 0
    if bold:
       b = 1
    if color != 'default':
        c = COLOR_MAP[color]
        return '\x1b[%(bold)s;%(color)sm%(text)s\x1b[0m' % dict(
                                                          bold=b,
                                                          color=c,
                                                          text=text)
    elif bold:
        return '\x1b[%(bold)s;%(text)s\x1b[0m' % dict(bold=b, text=text)

    else:
        return text
