from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Map():
    def __init__(self):
        self.map = {"l": "list",
                    "q": "quit",
                    "h": "help",
                    "a": "a",
                    "b": "b",
                    "c": "c",
                    "d": "d",
                    "1": "1",
                    "2": "2",
                    "3": "3",
                    "4": "4",
                    "5": "5",
                    "6": "6",
                    "7": "7",
                    "8": "8",
                    "9": "9",
                    "0": "10",
                    "e": "11",
                    "f": "12",
                    "g": "13",
                    "i": "14",
                    "k": "15",
                    "m": "16",
                    "n": "17",
                    "o": "18",
                    "r": "19",
                    "s": "20"}

    def find(self, char):
        try:
            return self.map[char]
        except KeyError:
            return ""