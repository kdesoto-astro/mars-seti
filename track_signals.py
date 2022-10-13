import urllib.request
import re
import sched, time
import sys

DSN_URL = "https://eyes.nasa.gov/dsn/data/dsn.xml"
VALID_STATIONS = ["MVN", "MEX"]

def parse_signal_xml(raw_string, name, valid_disks):
    """
    Parses the chunk of XML data to return signal
    objects for a given station.
    """
    parse_dish = raw_string.split("</dish>")
    parsed_time = re.findall(name + '" timeUTC="[0-9]+"', raw_string)[0]
    t = int(parsed_time.split('"')[-2])
    
    parsed_valid_dishes = []
    for d in parse_dish:
        parse_dish2 = d.split("<dish name=")
        
        for d2 in parse_dish2:
            if len(d2) < 10 or d2[1:4] != "DSS":
                continue
            if int(d2[4:6]) in valid_disks:
                parsed_valid_dishes.append(d2)
    freqs = []
    powers = []
    spacecrafts = []
    signal_types = []
    for link in parsed_valid_dishes:
        frequency_strings = re.findall('frequency="[0-9]+"', link)
        for f in frequency_strings:
            freqs.append(int(f[11:-1]))
        power_strings = re.findall('power="[0-9.-]+"', link)
        for f in power_strings:
            powers.append(float(f[7:-1]))
        space_strings = re.findall('spacecraft="[A-Z0-9]+"', link)
        for f in space_strings:
            spacecrafts.append(f[12:-1])
        signal_types.extend(re.findall('(?:up|down)Signal', link))
        
    return t, signal_types, freqs, powers, spacecrafts

    
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
        self.uplink_list.append(link_object)
        return True
    
    def add_downlink(self, link_object):
        """
        Adds downlink object to list if it's not
        the same as previous uplink signal.
        """
        self.downlink_list.append(link_object)
        return True
            
    def fetch_signals(self):
        """
        Fetches the current uplink/downlink status from the
        Deep Space Network stations. Adds new uplinks/downlinks as
        needed.
        """
        req = urllib.request.Request(DSN_URL)
        resp = urllib.request.urlopen(req)
        data = resp.read().decode("utf-8") 
        
        t, signal_types, freqs, powers, spacecrafts = parse_signal_xml(data, self.name, self.disks)

        for i in range(len(signal_types)):
            signal = Signal(t, freqs[i], powers[i], spacecrafts[i])
            if signal_types[i] == "upSignal":
                self.add_uplink(signal)
            else:
                self.add_downlink(signal)
    
    def log_signals(self):
        """
        Offloads signal lists to file for more
        permanent storage.
        """
        t0 = self.downlink_list[0].t
        tf = self.downlink_list[-1].t
        fn = "%s_%d_%d_down.csv" % (self.name, t0, tf)
        with open(fn, "a+") as f:
            for s in self.downlink_list:
                f.write("%d,%d,%f,%s\n" % (s.t, s.freq, s.power, s.spacecraft))
        t0_up = self.uplink_list[0].t
        tf_up = self.uplink_list[-1].t
        fn_up = "%s_%d_%d_up.csv" % (self.name, t0_up, tf_up)
        with open(fn_up, "a+") as f:
            for s in self.uplink_list:
                f.write("%d,%d,%f,%s\n" % (s.t, s.freq, s.power, s.spacecraft))
        self.uplink_list = []
        self.downlink_list = []
        
        
class CanberraStation(Station):
    def __init__(self):
        super().__init__("Canberra", [43, 34, 35, 36])
        
class GoldstoneStation(Station):
    def __init__(self):
        super().__init__("Goldstone", [14, 24, 25, 26])

class MadridStation(Station):
    def __init__(self):
        super().__init__("Madrid", [63, 65, 53, 54, 55, 56])
    
s = sched.scheduler(time.time, time.sleep)

def main_loop(sc, stream): 
    print("Running loop...")
    # do your stuff
    if len(stream.downlink_list) < 1000:
        stream.fetch_signals()
    else:
        stream.log_signals()

    sc.enter(10, 1, main_loop, (sc, stream))
    
station = sys.argv[1]

if station == "madrid":
    stream = MadridStation()
elif station == "canberra":
    stream = CanberraStation()
else:
    stream = GoldstoneStation()

s.enter(10, 1, main_loop, (s, stream))
s.run()


main()
    
    