from __future__ import unicode_literals
import os
import ConfigParser
import logging


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
        self.config = ConfigParser.SafeConfigParser()
        print "reading config file..."
        self.config.read(self.config_file)
        if not self.config.sections():
            print "config file is empty"
            self.generate()
        try:
            self.network, self.paths, self.variables, self.lcd, self.log = self.get_sections()
        except ConfigParser.NoSectionError:
            print "config file is incomplete, regenerating"
            os.remove(self.config_file)
            self.generate()
            self.network, self.paths, self.variables, self.lcd, self.log = self.get_sections()
        logging.debug(self.stringify_config())
        
    def get_sections(self):
        return (self.config_section_map('Network'),
                self.config_section_map('Paths'),
                self.config_section_map('Variables'),
                self.config_section_map('LCD'),
                self.config_section_map('log'))
    
    def stringify_config(self):
        """
        a print method
        """
        result = "Network options :"
        result += str(self.network)
        result += "Paths options :"
        result += str(self.paths)
        result += "Miscellaneous variables :"
        result += str(self.variables)
        result += "Log options :"
        result += str(self.log)
        return result

    def generate(self):
        """
        Generates a default config file:
        Works on a standard computer, must have the requirements installed though such as MPD, mutagen, ...
        It opens the non-existing file in writing mode, it adds a section with
        config.add_section() method, and a value with config.set() method both to the config object in RAM
        Then it writes the config in RAM into the file well-formatted, and closes the file.
        """
        print "writing config file..."
        cfgfile = open(self.config_file, 'w')
        self.config.add_section('Network')
        self.config.set('Network', 'mpd_host', 'localhost')
        self.config.set('Network', 'mpd_port', '6600')
        self.config.add_section('Paths')
        self.config.set('Paths', 'music_dir', 'Music')
        self.config.set('Paths', 'index_dir', 'Import')
        self.config.set('Paths', 'mpd_conf_file', '/etc/mpd.conf')
        self.config.add_section('Variables')
        #indexation au demarrage ?
        self.config.set('Variables', 'index', 'True')
        self.config.set('Variables', 'index_timeout', '5')
        #amount of musics in queue before timeout is activated
        self.config.set('Variables', 'add_timeout', '30')
        self.config.set('Variables', 'nb_music', '5')
        self.config.add_section('LCD')
        self.config.set('LCD', 'type', '2x40')
        self.config.set('LCD', 'lcdd_host', 'localhost')
        self.config.set('LCD', 'lcdd_port', '13666')
        self.config.add_section('log')
        self.config.set('log', 'format', "%%(asctime)s %%(levelname)s %%(message)s")
        self.config.set('log', 'path', "/var/log/jukebox.log")
        self.config.set('log', 'level', '20')
        self.config.write(cfgfile)
        cfgfile.close()
        
    def config_section_map(self, section):
        """
        It is a modified version of a method found on the Internet
        Basically it reads a section a gets the values in the appropriate type (integer, boolean or string)
        It is not pretty, but it works
        """
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.getint(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not an integer
                pass
            try:
                dict1[option] = self.config.getboolean(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not a boolean
                pass
            try:
                dict1[option] = self.config.get(section, option)
                logging.debug("Found an option : %s" % dict1[option])
                continue
            except:
                #The option (or attribute) is not a string (!?)
                print("exception on %s!" % option)
                logging.error("Unknown option in config file, skipping")

        return dict1