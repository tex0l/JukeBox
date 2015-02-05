from __future__ import unicode_literals
import os
import ConfigParser
import logging
import re


class Config:
    """
    The Config class uses the python library ConfigParser to read and write the config file
    """

    def __init__(self):
        """
        Initializes the Config object:
        It tries to read a file located in the same directory named jukebox.conf
        If not found, it generates a default one
        Else it reads it and pick the sections dictionary each one as a single attribute of the Config object
        Finally it prints the config read or generated
        """
        self.config_file = os.path.join(os.path.dirname(__file__), "jukebox.conf")
        self.Config = ConfigParser.SafeConfigParser()
        print "reading config file..."
        self.Config.read(self.config_file)
        if self.Config.sections() == []:
            print "config file is empty"
            self.generate()
        try:
            self.network, self.paths, self.variables, self.lcd, self.log = self.get_sections()
        except ConfigParser.NoSectionError:
            print "config file is incomplete, regenerating"
            os.remove(self.config_file)
            self.generate()
            self.network, self.paths, self.variables, self.lcd, self.log = self.get_sections()
        self.print_config()
    def get_sections(self):
        return (self.ConfigSectionMap('Network'),
                self.ConfigSectionMap('Paths'),
                self.ConfigSectionMap('Variables'),
                self.ConfigSectionMap('LCD'),
                self.ConfigSectionMap('log'))
    def print_config(self):
        """
        a print method
        """
        print "Network options :"
        print self.network
        print "Paths options :"
        print self.paths
        print "Miscellaneous variables :"
        print self.variables
        print "Log options :"
        print self.log

    def generate(self):
        """
        Generates a default config file:
        Works on a standard computer, must have the requirements installed though such as MPD, mutagen, ...
        It opens the non-existing file in writing mode, it adds a section with
        Config.add_section() method, and a value with Config.set() method both to the Config object in RAM
        Then it writes the config in RAM into the file well-formatted, and closes the file.
        """
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
        self.Config.set('LCD', 'lcdd_host', 'localhost')
        self.Config.set('LCD', 'lcdd_port', '13666')
        self.Config.add_section('log')
        self.Config.set('log', 'format', "%%(asctime)s %%(levelname)s %%(message)s")
        self.Config.set('log', 'path', "/var/log/jukebox.log")
        self.Config.set('log', 'level', '20')
        self.Config.write(cfgfile)
        cfgfile.close()
    def ConfigSectionMap(self, section):
        """
        It is a modified version of a method found on the Internet
        Basically it reads a section a gets the values in the appropriate type (integer, boolean or string)
        It is not pretty, but it works
        """
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.getint(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not an integer
                pass
            try:
                dict1[option] = self.Config.getboolean(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not a boolean
                pass
            try:
                dict1[option] = self.Config.get(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not a string (!?)
                print("exception on %s!" % option)
                logging.error("Unknown option in config file, skipping")

        return dict1