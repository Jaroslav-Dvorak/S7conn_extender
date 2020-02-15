from time import time, sleep
# from snap7.snap7types import areas
import configparser
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
import snap7

Config = configparser.ConfigParser()
Config.read("config.ini")

PLCs = {}
for section in Config.sections():
    PLCs[section] = dict(Config[section])

VirtPLC_IP = PLCs.pop("VIRT_PLC")["ip"]


def address_parser(address, name):
    """
    splits S7 address into dict
    """
    address = address.split(".")
    outdict = {}
    if address[0].lower().startswith("db"):
        outdict[name+"_AREA"] = "DB"
        outdict[name+"_DB"] = int(address[0][2:])
        outdict[name+"_ADDR"] = int(address[1][3:])
        if "BYTE" in address[2]:
            outdict[name+"_SIZE"] = int(address[2].split()[2])
    return outdict


for PLC in PLCs:
    TYPE = PLCs[PLC].pop("type")
    IP = PLCs[PLC]["ip"]
    if TYPE == "1200" or TYPE == "1500":
        PLCs[PLC]["conntupple"] = (IP, 0, 1)
    elif TYPE == "300" or TYPE == "400":
        PLCs[PLC]["conntupple"] = (IP, 0, 2)
    elif TYPE.lower() == "logo":
        PLCs[PLC]["conntupple"] = (IP, 0, 0)

    transmit = ("phys_source", "virt_source", "virt_dest", "phys_dest")
    for a in transmit:
        PLCs[PLC].update(address_parser(PLCs[PLC].pop(a), a))

    PLCs[PLC]["conn_attempts"] = 3


Areas = {
        'I': 0x81,
        'Q': 0x82,
        'M': 0x83,
        'DB': 0x84,
        'CT': 0x1C,
        'TM': 0x1D,
        }


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.PIPE) == 0


VirtPLC = snap7.client.Client()
try:
    VirtPLC.connect(VirtPLC_IP, 0, 2)
except Exception as e:
    del e
    print("Virtual PLC server unavaible.")
    exit()


def online_checker():
    """
    Determines if PLC is avaible on network.
    """
    while True:
        for plc in PLCs.values():
            if plc["conn_attempts"] >= 3:
                if ping(plc["ip"]):
                    plc["conn_attempts"] = 0
        sleep(0.1)


def exchanger(params):
    """
    Connects to PLC and exchanges data between VirtPLC and Physical PLC.
    """
    plc = snap7.client.Client()
    plc.connect(*params["conntupple"])

    data = plc.read_area(area=Areas[params["phys_source_AREA"]],
                         dbnumber=params["phys_source_DB"],
                         start=params["phys_source_ADDR"],
                         size=params["phys_source_SIZE"])
    VirtPLC.write_area(area=Areas[params["virt_dest_AREA"]],
                       dbnumber=params["virt_dest_DB"],
                       start=params["virt_dest_ADDR"],
                       data=data)

    data = VirtPLC.read_area(area=Areas[params["virt_source_AREA"]],
                             dbnumber=params["virt_source_DB"],
                             start=params["virt_source_ADDR"],
                             size=params["virt_source_SIZE"])
    plc.write_area(area=Areas[params["phys_dest_AREA"]],
                   dbnumber=params["phys_dest_DB"],
                   start=params["phys_dest_ADDR"],
                   data=data)

    plc.disconnect()
    plc.destroy()


def exchanging():
    """
    Try to start exchane data, if failed three times - switch to online_checker.
    Prints time of one cycle of exchange all physical PLC configured.
    """
    while True:
        stime = time()
        for plc in PLCs.values():
            if plc["conn_attempts"] < 3:
                try:
                    exchanger(params=plc)
                except Exception as e:
                    plc["conn_attempts"] += 1
                else:
                    plc["conn_attempts"] = 0
        print("time:", time()-stime)
        sleep(0.5)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(exchanging)
        executor.submit(online_checker)
