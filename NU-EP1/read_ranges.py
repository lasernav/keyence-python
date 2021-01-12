import sys
from cpppo.server.enip.get_attribute import proxy_simple

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

via = proxy_simple( hostname )
with via:
    result = via.read( params )
    values = enumerate(result)
    for key, val in values:
        print(key, val)

