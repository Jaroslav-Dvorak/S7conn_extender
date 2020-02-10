import snap7
from time import time, sleep
# from snap7.snap7types import areas

# TODO:
#     - config.ini
#     - connection handler
#     - paralelize

Areas = {
        'IB': 0x81,
        'QB': 0x82,
        'MB': 0x83,
        'DBB': 0x84,
        'CT': 0x1C,
        'TM': 0x1D,
        }

Connections = {
                # ("R_1", 1): ("10.40.1.1", 0, 1),
                ("R_2", 2): ("10.40.2.1", 0, 1),
                ("R_3", 3): ("10.40.3.1", 0, 1),
                ("R_4", 4): ("10.40.4.1", 0, 1),
                ("R_5", 5): ("10.40.5.1", 0, 1),
                ("R_6", 6): ("10.40.6.1", 0, 1),
                ("R_7", 7): ("10.40.7.1", 0, 1),
                # ("R_8", 8): ("10.40.8.1", 0, 1),
                # ("R_9", 9): ("10.40.9.1", 0, 1),
                # ("R_10", 10): ("10.40.10.1", 0, 1),
               }

# Snap7Server_con = ("10.32.65.3", 0, 2)
Snap7Server_con = ("10.0.0.3", 0, 2)
VirtPLC = snap7.client.Client()
VirtPLC.connect(*Snap7Server_con)


def db200_to_virtPLC(source_conn, virt_plc, db):
    plc = snap7.client.Client()
    plc.connect(*source_conn)

    data = plc.read_area(area=Areas["DBB"], dbnumber=200, start=0, size=49)
    virt_plc.write_area(area=Areas["DBB"], dbnumber=db, start=0, data=data)

    data = virt_plc.read_area(area=Areas["DBB"], dbnumber=db, start=50, size=1)
    plc.write_area(area=Areas["DBB"], dbnumber=200, start=50, data=data)
    # virt_plc.write_area(area=Areas["DBB"], dbnumber=db, start=50, data=bytes(chr(0), "utf-8"))
    plc.disconnect()
    plc.destroy()


while True:
    stime = time()
    for ID, conn in Connections.items():
        try:
            db200_to_virtPLC(conn, VirtPLC, ID[1])
        except Exception as e:
            pass
    # print("time:", time()-stime)
    sleep(1)
