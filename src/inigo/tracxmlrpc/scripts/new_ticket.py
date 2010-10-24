#!/usr/bin/env python

import xmlrpclib
import getpass
import sys
import os
import tempfile

from inigo.tracxmlrpc.scripts.common import (editor_input, selection_input,
                                            get_parser)
from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC

def main():

    parser = get_parser()
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
    
    components = ticket_server.components()
    #components = [field['options'] for field in fields if field['name']=='component'][0]
    milestones = ticket_server.milestones()

    summary = raw_input("Summary: ")
    estimatedhours = raw_input("Estimated hours: ")
    component = selection_input("Select component: ",components)
    milestone = selection_input("Select milestone: ",milestones)
    description = editor_input("Please enter a description above")
    
    print "\n\n====================\n"
    print "Summary : %s" % summary
    print "Estimated Hours: %s" % estimatedhours
    print "Component: %s" % component
    print "Milestone: %s" % milestone
    print "Description\t:\n\n%s" % ("     %s" % description.replace('\n','\n     '))
    
    proceed = raw_input("Is this correct? (y/n)")
    if proceed.strip().lower()[0] != 'y':
       return
    
    #propertykeys = ['status', 'totalhours', 'description', 'reporter', 'cc', 'milestone', 'component', 'summary', 'hours', 'owner', 'internal', 'billable', 'keywords', 'estimatedhours', 'type', 'priority']
    
    tid = ticket_server.create(summary,description, 
                                component=component,
                                estimatedhours=estimatedhours)

    ticket = ticket_server.get(tid)

    print ticket.data
    print "\nTicket created at %s/ticket/%s" % (BASE % dict(project=project),tid)

if __name__ == "__main__":
   main()
