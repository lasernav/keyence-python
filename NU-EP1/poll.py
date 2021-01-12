import logging
import sys
import time
import threading

import cpppo
logging.basicConfig(**cpppo.log_cfg)

from cpppo.server.enip import poll
from cpppo.server.enip.ab import powerflex_750_series as device

# Device IP in 1st arg, or 'localhost' (run: python -m cpppo.server.enip.poll_test)
hostname = sys.argv[1] if len(sys.argv) > 1 else 'localhost'

params = [
    ('@0x0001/0x0001/0x0007','SSTRING'), # Device name, should read: NU-EP1
    ('@0x0066/0x0001/0x0325', 'UINT'), # Current value of sensor
    ('@0x0066/0x0002/0x0325', 'UINT'),
    ('@0x0066/0x0003/0x0325', 'UINT'),
    ('@0x0066/0x0004/0x0325', 'UINT'),
    ('@0x0066/0x0005/0x0325', 'UINT'),
    ('@0x0066/0x0006/0x0325', 'UINT'),
    ('@0x0066/0x0007/0x0325', 'UINT'),
    ('@0x0066/0x0008/0x0325', 'UINT'),
    ('@0x0066/0x0009/0x0325', 'UINT'),
    ('@0x0066/0x000A/0x0325', 'UINT'),
    ('@0x0066/0x000B/0x0325', 'UINT'),
    ('@0x0066/0x000C/0x0325', 'UINT'),
    ('@0x0066/0x000D/0x0325', 'UINT'),
    ('@0x0066/0x000E/0x0325', 'UINT'),
    ('@0x0066/0x000F/0x0325', 'UINT'),
    ('@0x0066/0x0010/0x0325', 'UINT'),
    ('@0x0066/0x0000/0x0064', 'UINT'), #'WORD') ,
    ('@0x0066/0x0000/0x0065', 'UINT'), #'WORD')
    ('@0x0066/0x0000/0x0090', 'UINT'),
    ('@0x0066/0x0000/0x0091', 'UINT'),
    ('@0x0066/0x0000/0x0092', 'UINT'),
    ('@0x0066/0x0000/0x0093', 'UINT'),
    ('@0x0066/0x0000/0x0094', 'UINT'),
    ('@0x0066/0x0000/0x0095', 'UINT'),
    ('@0x0066/0x0000/0x0096', 'UINT'),
    ('@0x0066/0x0000/0x0097', 'UINT'),
    ('@0x0066/0x0000/0x0098', 'UINT'),
    ('@0x0066/0x0000/0x0099', 'UINT'),
    ('@0x0066/0x0000/0x009A', 'UINT'),
    ('@0x0066/0x0000/0x009B', 'UINT'),
    ('@0x0066/0x0000/0x009C', 'UINT'),
    ('@0x0066/0x0000/0x009D', 'UINT'),
    ('@0x0066/0x0000/0x009E', 'UINT'),
    ('@0x0066/0x0000/0x009F', 'UINT')
]

def decodeKey(str):
    if str[:2] == "0x":
        return int(str[2:], base=16)
    else:
        return int(str)

def failure(exc):
    failure.string.append(str(exc))

failure.string = []

def process(par, val):
    process.values[par] = val

process.done = False
process.values = {}

poller = threading.Thread(
    target=poll.poll, kwargs={
        'proxy_class':  device,
        'address':      (hostname, 44818),
        'cycle':        0.01,
        'timeout':      0.2,
        'process':      process,
        'failure':      failure,
        'params':       params,
    })

poller.start()

# Monitor the process.values {} and failure.string [] (updated in another Thread)
try:
    while True:
        found = False
        ids = [-1] * 16
        raw_ranges = [-1] * 16
        while process.values:
            found = True
            par, val = process.values.popitem()
            key = par[0].replace("@", "")
            keys = key.split("/")
            #print(keys)
            if val is None:
                continue
            if len(keys) == 3:
                classId = decodeKey(keys[0])
                instanceId = decodeKey(keys[1])
                attributeId = decodeKey(keys[2])
                #print("%s %s %s == %r" % (classId, instanceId, attributeId, val))

                #IDs of connected modules
                if classId == 0x0066 and instanceId == 0x0000:
                    id = attributeId - 0x0090
                    if id >= 0 and id < 0xF:
                        ids[id] = val[0]

                #ranges
                if classId == 0x0066 and attributeId == 0x0325:
                    raw_ranges[instanceId] = val[0]


        if found:
            print("STOP %s" % (time.ctime()))
            #print(ids)
            #print(raw_ranges)

            ranges = []
            for i in range(0, 16):
                id = ids[i]
                if id > 0:
                    ranges.append(raw_ranges[id])
                else:
                    ranges.append(None)

            print(ranges)

        while failure.string:
            exc = failure.string.pop( 0 )
            print("%s: %s" %(time.ctime(), exc))

        # time.sleep(0.1)
finally:
    process.done = True
    poller.join()
