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

    def __start_match(self, key):
        match = net_arena.TwistedNLHEArena()
        self.matches[key] = match
        return match


class ArenaWrapper(object):
    def __init__(self, match):
        self.match = match

    def tell(self, bot, line):
        log.msg("{b}@{m} :: {l}".format(b=bot, m=self.match, l=line))
        self.match.tell_bot(bot, [line])

    def add_bot(self, bot, bot_connection):
        log.msg("adding bot {}".format(bot))
        try:
            self.match.add_bot(bot, bot_connection)
        except:
            log.err()
