from __future__ import unicode_literals
import os
import ConfigParser

class Config():

    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "jukebox.conf")
        self.Config = ConfigParser.ConfigParser()
        print "reading config file..."
        self.Config.read(self.config_file)
        if self.Config.sections() == []:
            print "config file is empty"
            self.generate()
        self.network = self.ConfigSectionMap('Network')
        self.paths = self.ConfigSectionMap('Paths')
        self.variables = self.ConfigSectionMap('Variables')
        self.lcd = self.ConfigSectionMap('LCD')
        self.print_config()

    def print_config(self):
        print "Network options :"
        print self.network
        print "Paths options :"
        print self.paths
        print "Miscellaneous variables :"
        print self.variables
    def generate(self):
        print "writing config file..."
        cfgfile = open(self.config_file, 'w')
        self.Config.add_section('Network')
        self.Config.set('Network', 'mpd_host', 'localhost')
        self.Config.set('Network', 'mpd_port', '6600')
        self.Config.add_section('Paths')
        self.Config.set('Paths', 'music_dir', 'Music')
        self.Config.set('Paths', 'index_dir', 'Import')
        self.Config.set('Paths', 'mpd_conf_file', '/etc/mpd.conf')
        self.Config.add_section('Variables')
        #indexation au demarrage ?
        self.Config.set('Variables', 'index', 'True')
        self.Config.set('Variables', 'index_timeout', '5')
        #amount of musics in queue before timeout is activated
        self.Config.set('Variables', 'add_timeout', '30')
        self.Config.set('Variables', 'nb_music', '5')
        self.Config.add_section('LCD')
        self.Config.set('LCD', 'type', 'dummy')
        self.Config.set('LCD', 'LCDd_host', 'localhost')
        self.Config.set('LCD', 'LCDd_port', '13666')
        self.Config.write(cfgfile)
        cfgfile.close()
    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.getint(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                try:
                    dict1[option] = self.Config.getboolean(section, option)
                except:
                    try:
                        dict1[option] = self.Config.get(section, option)
                    except:
                        print("exception on %s!" % option)

        return dict1