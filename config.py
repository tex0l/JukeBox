from __future__ import unicode_literals
import ConfigParser

class Config():

    def __init__(self):
        self.config_file = "/etc/jukebox.ini"
        self.Config = ConfigParser.ConfigParser()
        print "\nreading config file..."
        self.Config.read(self.config_file)
        if self.Config.sections() == []:
            self.generate()
        self.network = self.ConfigSectionMap('Network')
        self.paths = self.ConfigSectionMap('Paths')
        self.variables = self.ConfigSectionMap('Variables')
        print self.network
        print self.paths
        print self.variables

        print self.network
    def generate(self):
        cfgfile = open(self.config_file, 'w')
        self.Config.add_section('Network')
        self.Config.set('Network', 'host', '127.0.0.1')
        self.Config.set('Network', 'port', 6600)
        self.Config.add_section('Paths')
        self.Config.set('Paths', 'music_dir', 'Music')
        self.Config.set('Paths', 'index_dir', 'Import')
        self.Config.set('Paths', 'mpd_conf_file', '/etc/mpd.conf')
        self.Config.add_section('Variables')
        self.Config.set('Variables', 'index', True)
        self.Config.set('Variables', 'lcd', '2x40')
        self.Config.set('Variables', 'timeout', 30)
        self.Config.set('Variables', 'nb_music', 5)
        self.Config.write(cfgfile)
        cfgfile.close()
        print self.Config
    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1