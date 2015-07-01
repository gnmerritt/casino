from twisted.python import log

from poker.arena import net_arena


class ArenaHolder(object):
    """Holds handles to running poker matches (arenas)"""
    def __init__(self):
        self.matches = {}
        self.ended = {}

    def get_or_create(self, match_key):
        if match_key in self.ended:
            return None
        if match_key in self.matches:
            return ArenaWrapper(self.matches[match_key])
        else:
            return ArenaWrapper(self.__start_match(match_key))

    def cleanup(self, key):
        del self.matches[key]
        self.ended[key] = True

    def __start_match(self, key):
        def cleanup(args):
            self.cleanup(key)
        match = net_arena.TwistedNLHEArena()
        match.after_match.addBoth(cleanup)
        self.matches[key] = match
        return match


class ArenaWrapper(object):
    def __init__(self, match):
        self.match = match

    def bot_said(self, bot, line):
        log.msg("{b}@{m} :: {l}".format(b=bot, m=self.match, l=line))
        try:
            self.match.bot_said(bot, line)
        except:
            log.err()

    def add_bot(self, bot, bot_connection):
        try:
            self.match.add_bot(bot, bot_connection)
        except:
            log.err()
