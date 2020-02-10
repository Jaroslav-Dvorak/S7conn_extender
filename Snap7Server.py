import time
import logging
import snap7
import sys
import os

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

tcpport = 102


def mainloop():
    server = snap7.server.Server()
    size = 100
    # DBdata1 = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # DBdata2 = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # DBdata3 = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # PAdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # TMdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # CTdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()
    # Mdata = (snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)()

    # server.register_area(snap7.snap7types.srvAreaDB, 1, DBdata)
    # server.register_area(snap7.snap7types.srvAreaPA, 1, PAdata)
    # server.register_area(snap7.snap7types.srvAreaTM, 1, TMdata)
    # server.register_area(snap7.snap7types.srvAreaCT, 1, CTdata)
    # server.register_area(snap7.snap7types.srvAreaMK, 1, Mdata)
    db_data = []
    for db_num in range(1, 65):
        db_data.append((snap7.snap7types.wordlen_to_ctypes[snap7.snap7types.S7WLByte] * size)())
        server.register_area(snap7.snap7types.srvAreaDB, db_num, db_data[db_num-1])

    os.system("net stop s7oiehsx64")
    server.start(tcpport=tcpport)
    os.system("net start s7oiehsx64")

    while True:
        while True:
            event = server.pick_event()
            if event:
                logger.info(server.event_text(event))
            else:
                break
        time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        snap7.common.load_library(sys.argv[1])
    mainloop()
