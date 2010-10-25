from inigo.tracxmlrpc.rpc import TracConfig, TracTicketXMLRPC
from inigo.tracxmlrpc.scripts.common import get_parser
import getpass
BASE="https://dev.inigo-tech.com/trac/%(project)s"

def main():
    parser = get_parser()
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
        print '#%s\t| %s' % (ticket.id, ticket.summary)
    

if __name__ == '__main__':
    main()
