import xmlrpclib
import getpass
import sys
import os
import tempfile

from urlparse import urlparse

class TracError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class TracConfig(object):

    def __init__(self, uri, username, password):
        parsed = urlparse(uri)
        uridata = dict(parsed._asdict())
        uridata.update({'username': username, 'password': password,
                        'hostname': parsed.hostname})
        self.uri = uri
        self.uridata = uridata

    def get_uristring(self):
        uri = '%(scheme)s://%(username)s:%(password)s@%(hostname)s%(path)s'
        return uri % (self.uridata)

    def get_xmlrpc_uri(self):
        return '%s/login/xmlrpc' % self.get_uristring()

class TracTicket(object):
    def __init__(self, config, id_, time_created, time_changed, data):
        self.config = config
        self.id = id_
        self.time_created = time_created 
        self.time_changed = time_changed
        self.data = data

    @property
    def url(self):
        return "%s/ticket/%s" % (self.config.uri, self.id)

    def __getattr__(self, key):
        if key in self.data:
            return self.data.get(key, None)
        raise AttributeError

    @property
    def comments(self):
        rpc = TracTicketXMLRPC(self.config)
        changelogs = rpc.changelog(self.id)
        for c in changelogs:
            if isinstance(c, TracComment):
                yield c

    def update(self, message, **options):
        rpc = TracTicketXMLRPC(self.config)
        rpc.update(self.id, message, **options)

    def available_actions(self):
        rpc = TracTicketXMLRPC(self.config)
        return rpc.available_actions(self.ticket_id)
        

class TracChangeLog(object):
    def __init__(self, config, time, author, oldvalue, value, field):
        self.field = field
        self.config = config
        self.time = time
        self.author = author
        self.oldvalue = oldvalue
        self.value = value

class TracComment(object):
    def __init__(self, config, time, author, id, comment):
        self.config = config
        self.time = time
        self.author = author
        if not id:
            self.id = 0
        else:
            self.id = int(id)

        self.comment = comment


def changelog_factory(config, time, author, field, oldvalue, newvalue, permanent):
    if field == 'comment' and newvalue:
        return TracComment(config, time, author, oldvalue, newvalue)
    else:
        return TracChangeLog(config, time, author, oldvalue, newvalue,
                    field=field)

class TracTicketXMLRPC(object):
    # Facade

    def __init__(self, config):
        self.config = config
        self._conn = xmlrpclib.ServerProxy(self.config.get_xmlrpc_uri())

    def components(self):
        try:
            return self._conn.ticket.component.getAll()
        except xmlrpclib.ProtocolError,e:
            raise TracError(e.errcode,e.errmsg)

    def available_actions(self, ticket_id):
        return self._conn.ticket.getActions(ticket_id)

    def milestones(self):
        return self._conn.ticket.milestone.getAll()

    def create(self, summary, description='', **options):
        ticket_id = self._conn.ticket.create(summary, description, options,
                                        True)
        return ticket_id

    def get(self, ticket_id):
        ticket = self._conn.ticket.get(ticket_id)
        return TracTicket(self.config, *ticket)

    def changelog(self, ticket_id):
        changelogs = self._conn.ticket.changeLog(ticket_id)
        return [changelog_factory(self.config, *cl) for cl in changelogs]

    def update(self, ticket_id, comment, **options):
        ticket = self._conn.ticket.update(ticket_id, comment, options, True)
        return TracTicket(self.config, *ticket)

    def query(self, *strfilters, **optfilters):
        filterlist = []

        # check if theres a 'status' in the query
        if not 'status' in ''.join(strfilters):
            if not 'status' in optfilters.keys():
                filterlist.append('status!=closed')

        for filter in strfilters:
            filterlist.append(filter)

        for key, value in optfilters.iteritems():
            if hasattr(value, '__iter__'):
                value = '|'.join(value)
            filterlist.append('%s=%s' % (key, value))

        if filterlist:
            filterstring = '%s' % '&'.join(filterlist)
            query = self._conn.ticket.query(filterstring)
        else:
            query = self._conn.ticket.query()

        multicall = xmlrpclib.MultiCall(self._conn)
        for ticket in query:
           multicall.ticket.get(ticket)
        return [TracTicket(self.config, *ticket) for ticket in multicall()]

