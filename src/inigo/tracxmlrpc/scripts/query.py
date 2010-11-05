from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC
from inigo.tracxmlrpc.scripts.common import get_parser, indent, colored
import getpass
BASE="https://dev.inigo-tech.com/trac/%(project)s"

def main():
    parser = get_parser()
    parser.add_argument('ticket_id', default=None, nargs="?", metavar='ticket_id')
    parser.add_argument('-m', '--only-mine', dest='filter_owner', action='store_true',
            help='Show only my tickets')

    args = parser.parse_args()

    if args.username:
        user = args.username
    else:
        user = raw_input('Username: ')
    if args.password:
        passwd = args.password
    else:
        passwd = getpass.getpass('Password: ')

    if args.ticket_id is None:
        render_list(user, passwd, args)
    else:
        render_view(user, passwd, args)

def render_list(user, passwd, args):
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

    for ticket in sorted(tickets, key=lambda x: x.id, reverse=True):
        color = 'default'
        bold = False
        if ticket.priority.lower() == 'critical':
            color = 'red'
            bold = True
        print colored('#%s\t| %s' % (ticket.id, ticket.summary), color, bold)


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
