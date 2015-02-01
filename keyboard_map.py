from __future__ import unicode_literals
class Map():
    def __init__(self):
        self.map = {}
        self.map["l"] = "list"
        self.map["q"] = "quit"
        self.map["h"] = "help"
        self.map["a"] = "a"
        self.map["b"] = "b"
        self.map["c"] = "c"
        self.map["d"] = "d"
        self.map["1"] = "1"
        self.map["2"] = "2"
        self.map["3"] = "3"
        self.map["4"] = "4"
        self.map["5"] = "5"
        self.map["6"] = "6"
        self.map["7"] = "7"
        self.map["8"] = "8"
        self.map["9"] = "9"
        self.map["0"] = "10"
        self.map["e"] = "11"
        self.map["f"] = "12"
        self.map["g"] = "13"
        self.map["i"] = "14"
        self.map["k"] = "15"
        self.map["m"] = "16"
        self.map["n"] = "17"
        self.map["o"] = "18"
        self.map["r"] = "19"
        self.map["s"] = "20"

    def find(self, char):
        try:
            return self.map[char]
        except KeyError:
            return ""