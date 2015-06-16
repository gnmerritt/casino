from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import internet, service
from twisted.python import log

from factory import PokerFactory


class PokerService(service.Service):
    def startService(self):
        log.msg("PokerService service started")


class Options(usage.Options):
    optParameters = [
        ['port', 'p', 5154, 'The port number to listen on.'],
        ['iface', None, 'localhost', 'The interface to listen on.'],
    ]


class PokerServiceMaker(object):
    implements(service.IServiceMaker, IPlugin)

    tapname = "casino"
    description = "Casino for AI Poker"
    options = Options

    def makeService(self, options):
        top_service = service.MultiService()

        poker_service = PokerService()
        poker_service.setServiceParent(top_service)

        factory = PokerFactory(poker_service)
        tcp_service = internet.TCPServer(int(options['port']), factory,
                                         interface=options['iface'])

        tcp_service.setServiceParent(top_service)

        return top_service


service_maker = PokerServiceMaker()
