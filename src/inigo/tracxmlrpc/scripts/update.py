#!/usr/bin/env python

import xmlrpclib
import getpass
import sys
import os
import tempfile

from inigo.tracxmlrpc.scripts.common import (editor_input, selection_input,
                                            get_parser, indent)
from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC

def action_keys(actions):
    for action in actions:
        yield action[0]
#    for action in actions:
#        if action[3]:
#            for name, value, options in action[3]:
#                for opt in options:
#                    yield '%s:%s' % (action[0], opt)
#        else:
#            yield '%s' % action[0]
#

def main():

    parser = get_parser()
    parser.add_argument('ticket_id', metavar='ticket_id',
            type=int,
            help='Ticket ID')
    parser.add_argument('-a', '--action', dest='action',
            help='Action on ticket')
    args = parser.parse_args()

    BASE="https://dev.inigo-tech.com/trac/%(project)s"
    project = args.project
    
    if args.username:
        user = args.username
    else:
        user = raw_input("Username: ")

    if args.password:
        passwd = args.password
    else:
        passwd = getpass.getpass("Password: ")

    conf = TracConfig(BASE % dict(project=project), user, passwd)
    ticket_server = TracTicketXMLRPC(conf)

    ticket = ticket_server.get(args.ticket_id)

    print "URL: %s" % (ticket.url)
    print "Summary: %s" % (ticket.summary)
 
    available_actions = list(action_keys(ticket_server.available_actions(
                                        args.ticket_id)))
    if args.action and (args.action not in available_actions):
        print 'Invalid action "%s". Available actions are : %s' % (args.action,
                                ' , '.join(available_actions))
        return 1
 
    components = ticket_server.components()
    #components = [field['options'] for field in fields if field['name']=='component'][0]
    milestones = ticket_server.milestones()

    hours = raw_input("Effective hours: ")
    comment = editor_input("Please enter a comment above")
    
    print "\n\n====================\n"
    print "URL: %s" % ticket.url
    print "Summary : %s" % ticket.summary
    print "Effective Hours: %s" % hours
    print "Comment\t:\n%s" % (indent(comment))
    
    proceed = raw_input("Is this correct? (y/n)")
    if proceed.strip().lower()[0] != 'y':
       return
    
    #propertykeys = ['status', 'totalhours', 'description', 'reporter', 'cc', 'milestone', 'component', 'summary', 'hours', 'owner', 'internal', 'billable', 'keywords', 'estimatedhours', 'type', 'priority']
    if args.action:
        ticket.update(comment, hours=hours, action=args.action)
    else:
        ticket.update(comment, hours=hours)

    print "\nTicket %s updated" % ticket.url

if __name__ == "__main__":
   main()
