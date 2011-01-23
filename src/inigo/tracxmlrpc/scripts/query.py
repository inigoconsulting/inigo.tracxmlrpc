from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC
from inigo.tracxmlrpc.scripts.common import indent, colored, get_auth
import getpass
import keyring
from argparse import ArgumentParser
BASE="https://dev.inigo-tech.com/trac/%(project)s"

ALL_TRACS=['startifact', 'clkss', 'nordicbet']

KEYRING_SERVICE='inigo.tracxmlrpc.scripts'

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('project', default=None, nargs='?', metavar='project', help='Project Name')
    parser.add_argument('-u', '--username', dest='username',
                help='Your trac login username')
    parser.add_argument('-p', '--password', dest='password',
                help='Your trac login password')
    return parser

def main():
    parser = get_parser()
    parser.add_argument('ticket_id', default=None, nargs="?", metavar='ticket_id')
    parser.add_argument('-m', '--only-mine', dest='filter_owner', action='store_true',
            help='Show only my tickets')

    args = parser.parse_args()

    user, passwd = get_auth(args.username, args.password)

    if args.project is None:
        render_all(user, passwd, args, ALL_TRACS)
    elif args.ticket_id is None:
        render_list(user, passwd, args)
    else:
        render_view(user, passwd, args)

def sort_tickets(tickets):
    tickets.sort(key=lambda x: x.id, reverse=True)
    def sortfunc(a, b):
        if a.priority.lower() == 'critical':
            return 1
        if a.priority.lower() == 'major' and b.priority.lower() == 'minor':
            return 1
        return -1
    tickets.sort(cmp=sortfunc)
    return tickets

def render_list(user, passwd, args):
    tickets = sort_tickets(ticket_list(user, passwd, args))

    for ticket in tickets:
        color = 'default'
        bold = False
        if ticket.priority.lower() == 'critical':
            color = 'red'
            bold = True
        print colored('#%-5d| %s' % (ticket.id, ticket.summary), color, bold)


def render_all(user, passwd, args, tracs):
    all_tickets = []
    for trac in tracs:
        args.project = trac
        tickets = ticket_list(user, passwd, args)
        for ticket in tickets:
            ticket.project = trac
        all_tickets += tickets

    all_tickets = sort_tickets(all_tickets)

    for ticket in all_tickets:
        color = 'default'
        bold = False
        if ticket.priority.lower() == 'critical':
            color = 'red'
            bold = True
        elif ticket.priority.lower() == 'major':
            color = 'yellow'
        print colored('%s|#%-5d| %s' % (ticket.project.ljust(13), ticket.id, ticket.summary), color, bold)


def ticket_list(user, passwd, args):

    result = []

    conf = TracConfig(BASE % dict(project=args.project), 
                    user, passwd)
    ticketrpc = TracTicketXMLRPC(conf)

    if args.filter_owner:
        tickets = ticketrpc.query(owner=user)
        # XXX: bad 
        tickets = tickets + ticketrpc.query('cc~=%s@inigo-tech.com' % user,
                                            'owner!=%s' % user)
    else:
        tickets = ticketrpc.query()

    return tickets

def render_view(user, passwd, args):
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
