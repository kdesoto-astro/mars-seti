import urllib

DSN_URL = "https://eyes.nasa.gov/dsn/data/dsn.xml"

class Signal:
    def __init__(self, t, freq, power, spacecraft):
        """
        Adds an uplink or downlink signal object.
        """
        self.t = t # in milliseconds
        self.freq = freq # in Hz
        self.power = power # in dBm
        self.spacecraft = spacecraft
    
class Station:
    def __init__(self, name):
        """
        Initializes the Station object, which tracks signal
        information for one of the three DSN stations (Canberra, 
        Madrid, and Goldstone). 
        """
        self.name = name
        self.uplink_list = []
        self.downlink_list = []
        
    def add_uplink(self, link_object):
        """
        Adds uplink object to list if it's not
        the same as previous uplink signal.
        """
        prev_uplink = self.uplink_list[-1]
        if (prev_uplink.spacecraft != link_object.spacecraft) or \
        (prev_uplink.freq != link_object.freq) or \
        (prev_uplink.power != link_object.power):
            self.uplink_list.append(link_object)
    
    def add_downlink(self, link_object):
        """
        Adds downlink object to list if it's not
        the same as previous uplink signal.
        """
        prev_downlink = self.downlink_list[-1]
        if (prev_downlink.spacecraft != link_object.spacecraft) or \
        (prev_downlink.freq != link_object.freq) or \
        (prev_downlink.power != link_object.power):
            self.downlink_list.append(link_object)
        
class CanberraStation(Station):
    def __init__(self):
        super().__init__(self, "Canberra")
        
class GoldstoneStation(Station):
    def __init__(self):
        super().__init__(self, "Goldstone")

class MadridStation(Station):
    def __init__(self):
        super().__init__(self, "Madrid")
        
        
def fetch_signals():
    """
    Fetches the current uplink/downlink status from the
    Deep Space Network stations.
    """
    pass