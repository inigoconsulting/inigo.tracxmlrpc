from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC
from inigo.tracxmlrpc.scripts.common import get_parser
import getpass
BASE="https://dev.inigo-tech.com/trac/%(project)s"

import re

def indent(text):
    result = []
    for l in text.split('\n'):
        result.append('  | ' + l)
    return '\n'.join(result)

def main():
    parser = get_parser()
    parser.add_argument('ticket_id', metavar='ticket_id',
            type=int,
            help='Ticket ID')

    args = parser.parse_args()

    if args.username:
        user = args.username
    else:
        user = raw_input('Username: ')
    if args.password:
        passwd = args.password
    else:
        passwd = getpass.getpass('Password: ')


    conf = TracConfig(BASE % dict(project=args.project), 
                    user, passwd)

    ticketrpc = TracTicketXMLRPC(conf)

    ticket = ticketrpc.get(args.ticket_id)

    print """
========= #%(id)s =========
URL: %(url)s
Summary: %(summary)s""" % dict(id=ticket.id,
                                url=ticket.url,
                                summary=ticket.summary)

    if ticket.description:
        print """Description:

%(description)s
""" % dict(description=indent(ticket.description))
    print "Estimated Hours: %(estimatedhours)s" % dict(
                        estimatedhours=ticket.estimatedhours)

    comments = ticket.comments
    if comments:
        print "\n---- Comments ----"

    for comment in comments:
        print """
Comment #%(id)s by %(author)s:

%(value)s""" % dict(id=comment.id, author=comment.author,
                    value=indent(comment.comment))

    print ""
    

if __name__ == '__main__':
    main()
