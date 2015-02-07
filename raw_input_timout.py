from __future__ import unicode_literals
import signal


class AlarmException(Exception):
    pass


# noinspection PyUnusedLocal,PyUnusedLocal
def alarm_handler(signum, frame):
    raise AlarmException


def non_blocking_raw_input(prompt='', timeout=20):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(timeout)
    try:
        text = raw_input(prompt)
        signal.alarm(0)
        return text
    except AlarmException:
        print '\nSkipping...'
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''