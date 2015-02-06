from __future__ import unicode_literals
import signal


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def nonBlockingRawInput(prompt='', timeout=20):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = raw_input(prompt)
        signal.alarm(0)
        return text
    except AlarmException:
        print '\nSkipping...'
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''