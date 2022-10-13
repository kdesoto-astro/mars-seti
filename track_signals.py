import urllib.request

DSN_URL = "https://eyes.nasa.gov/dsn/data/dsn.xml"
VALID_STATIONS = ["MVN", "MEX"]

def parse_signal_xml(raw_string, valid_disks):
    """
    Parses the chunk of XML data to return signal
    objects for a given station.
    """
    parse_dish = raw_string.split("</dish>")
    
    parsed_valid_dishes = []
    for d in parse_dish:
        parse_dish2 = d.split("<dish name=")
        
        for d2 in parse_dish2:
            if len(d2) < 10 or d2[1:4] != "DSS":
                continue
            print(d2[1:6])
            if int(d2[4:6]) in valid_disks:
                parsed_valid_dishes.append(d2)
    
    print(parsed_valid_dishes)
    
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
    def __init__(self, name, disk_list):
        """
        Initializes the Station object, which tracks signal
        information for one of the three DSN stations (Canberra, 
        Madrid, and Goldstone). 
        """
        self.name = name
        self.uplink_list = []
        self.downlink_list = []
        self.disks = disk_list
        
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
            
    def fetch_signals(self):
        """
        Fetches the current uplink/downlink status from the
        Deep Space Network stations. Adds new uplinks/downlinks as
        needed.
        """
        req = urllib.request.Request(DSN_URL)
        resp = urllib.request.urlopen(req)
        data = resp.read().decode("utf-8") 
        
        signals = parse_signal_xml(data, self.disks)
        
        print(signals)
    
    def log_signals(self):
        """
        Offloads signal lists to file for more
        permanent storage.
        """
        pass
        
class CanberraStation(Station):
    def __init__(self):
        super().__init__("Canberra", [43, 34, 35, 36])
        
class GoldstoneStation(Station):
    def __init__(self):
        super().__init__("Goldstone", [14, 24, 25, 26])

class MadridStation(Station):
    def __init__(self):
        super().__init__("Madrid", [63, 65, 53, 54, 55, 56])
        
def main():
    canberra_stream = CanberraStation()
    canberra_stream.fetch_signals()

main()
    
    