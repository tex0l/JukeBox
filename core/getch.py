from __future__ import unicode_literals


class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        char = self.impl()
        if char == '\x03':
            raise KeyboardInterrupt
        elif char == '\x04':
            raise EOFError
        print(char)
        return char


class _GetchUnix:
    # noinspection PyUnresolvedReferences,PyUnresolvedReferences
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    # noinspection PyUnresolvedReferences
    def __init__(self):
        # noinspection PyUnresolvedReferences
        import msvcrt

    def __call__(self):
        # noinspection PyUnresolvedReferences
        import msvcrt

        return msvcrt.getch()


getch = _Getch()