import socket
from threading import Thread
import sys
import math
import time

from struct import pack
from struct import unpack

global soldat_localport
global soldat_server
global prx

soldat_localport = 23073
soldat_server = "217.182.78.135:23080"
prx = "51.254.44.184:10874"
useproxy = True

global alive
global tmr
global cp1to2time
global cp2to3time
global cp3to4time
global besttime
global besttime2
global besttime3
global difftime2
global difftime3


besttime = 13.0
besttime2 = 30.0
besttime3 = 50.0
cp1to2time = None
cp2to3time = None
cp3to4time = None
difftime = 0.0
difftime2 = 0.0
difftime3 = 0.0

tmr = None
alive = False

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
if useproxy:
    try:
        import socks
        s2 = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
    except:
        print ("PySocks is not installed, remote proxy feature is disabled.")
        print ("To install it, use 'pip3 install PySocks'")
        useproxy = False    
else:
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class PacketID:
    bullet = b"\x05"
    chat = b"\x06"
    keepalive = b"\x1F"
    votekick = b"\x2F"
    changeteam = b"\x3F"
    move = b"\x2A"
    dead = b"\x2B"
    special = b"\x40"
    pingserver = b"\x69"

def ConnectedServer():
    return ((soldat_server.split(":")[0],int(soldat_server.split(":")[1])))

def calchash(pkt):
    Sum = 0xA3 * 33 + 2
    for i in range(0,len(pkt)):
        Sum = (Sum * 33) + pkt[i]
    return Sum & 0xFFFF

def WorldText(screen ,layer , text, delay, color, scale, x, y):
    packet = PacketID.special
    packet += screen
    packet += layer.to_bytes(1, byteorder = "little")
    packet += delay.to_bytes(4, byteorder = "little")
    packet += pack("f", scale)
    packet += pack("I",color)
    packet += pack("f", x)
    packet += pack("f", y)
    packet += text
    packet += b"\x00"
    crc = calchash(packet).to_bytes(2, byteorder = "little")
    return PacketID.special + crc + packet[1:]

def Client2Server():
    global alive

    s1.bind(("localhost", 23666))
    print ("[+] Client listener ready on localhost port 23666")
    while True:
        data,addr = s1.recvfrom(12000)
        if data != "":
            if data[:1] == PacketID.move:
                alive = True             
                s2.sendto(data,ConnectedServer())               
            elif data[:1] == PacketID.dead:
                alive = False     
                s2.sendto(data,ConnectedServer())
            else:
                try:
                    s2.sendto(data, ConnectedServer())
                except Exception as e:
                    print ("[-] Proxy failure",e)

def DrawSplitUI():
    global currentmap
    global cp1to2time
    global cp2to3time
    global cp3to4time
    global difftime
    global besttime

    global difftime2
    global besttime2

    global difftime3
    global besttime3
    global tmr


    f = open("proxycfg.ini", "r")
    lines = f.readlines()
    f.close()
    color1 = lines[0].strip().split(" = ")[1].strip()
    color2 = lines[1].strip().split(" = ")[1].strip()
    color3 = lines[2].strip().split(" = ")[1].strip()
    bgcolor1 = lines[3].strip().split(" = ")[1].strip()
    bgcolor2 = lines[4].strip().split(" = ")[1].strip()
    rowcolor1 = lines[5].strip().split(" = ")[1].strip()
    rowcolor2 = lines[6].strip().split(" = ")[1].strip()
    anchorX = float(lines[7].strip().split(" = ")[1].strip())
    anchorY = float(lines[8].strip().split(" = ")[1].strip())
    bganchorX1 = float(lines[9].strip().split(" = ")[1].strip())
    bganchorY1 = float(lines[10].strip().split(" = ")[1].strip())
    bgscale1 = float(lines[11].strip().split(" = ")[1].strip())
    bganchorX2 = float(lines[12].strip().split(" = ")[1].strip())
    bganchorY2 = float(lines[13].strip().split(" = ")[1].strip())
    bgscale2 = float(lines[14].strip().split(" = ")[1].strip())
    rowanchorX1 = float(lines[15].strip().split(" = ")[1].strip())
    rowanchorY1 = float(lines[16].strip().split(" = ")[1].strip())
    rowscale1 = float(lines[17].strip().split(" = ")[1].strip())
    rowanchorX2 = float(lines[18].strip().split(" = ")[1].strip())
    rowanchorY2 = float(lines[19].strip().split(" = ")[1].strip())
    rowscale2 = float(lines[20].strip().split(" = ")[1].strip())
    mapname = lines[21].strip().split(" = ")[1].strip()

    if (cp1to2time != None) and (cp1to2time != 0.0):
        if besttime != cp1to2time:
            difftime = round(cp1to2time - besttime, 3)
    if (cp1to2time != None) and (cp1to2time != 0.0) and cp1to2time < besttime:
        besttime = cp1to2time
    if (cp2to3time != None) and (cp2to3time != 0.0):
        if besttime2 != cp2to3time:
            difftime2 = round(cp2to3time - besttime2, 3)
    if (cp2to3time != None) and (cp2to3time != 0.0) and cp2to3time < besttime2:
        besttime2 = cp2to3time
    if (cp3to4time != None) and (cp3to4time != 0.0):
        if besttime3 != cp3to4time:
            difftime3 = round(cp3to4time - besttime3, 3)
    if (cp3to4time != None) and (cp3to4time != 0.0) and cp3to4time < besttime3:
        besttime3 = cp3to4time

    wtext0 = WorldText(b"\x01", 21, bytes("Runmode livesplit", "ascii"), 1000, int(color1,0), 0.08, anchorX, anchorY+13)
    wtext1 = WorldText(b"\x01", 22, bytes(" "*6+mapname, "ascii"), 1000, int(color2,0), 0.05, anchorX, anchorY+27)
    wtext2 = WorldText(b"\x01", 23, bytes("      cp 1 -> cp 2:     " +str(cp1to2time), "ascii"), 1000, int(color3,0), 0.06, anchorX, anchorY+40)
    wtext4 = WorldText(b"\x01", 25, bytes("      cp 2 -> cp 3:     " +str(cp2to3time), "ascii"), 1000, int(color3,0), 0.06, anchorX, anchorY+65)
    wtext6 = WorldText(b"\x01", 27, bytes("      cp 3 -> cp 4:     " +str(cp3to4time), "ascii"), 1000, int(color3,0), 0.06, anchorX, anchorY+90)
    if (difftime > 0):
        wtext3 = WorldText(b"\x01", 24, bytes(" "*40+"+" +str(difftime), "ascii"), 1000, 0xFF0000, 0.05, anchorX, anchorY+50)
    else:
        wtext3 = WorldText(b"\x01", 24, bytes(" "*41 +str(difftime), "ascii"), 1000, 0x00FF00, 0.05, anchorX, anchorY+50)
    if (difftime2 > 0):
        wtext5 = WorldText(b"\x01", 26, bytes(" "*40+"+" +str(difftime2), "ascii"), 1000, 0xFF0000, 0.05, anchorX, anchorY+75)
    else:
        wtext5 = WorldText(b"\x01", 26, bytes(" "*41 +str(difftime2), "ascii"), 1000, 0x00FF00, 0.05, anchorX, anchorY+75)
    if (difftime3 > 0):
        wtext7 = WorldText(b"\x01", 28, bytes(" "*40+"+" +str(difftime3), "ascii"), 1000, 0xFF0000, 0.05, anchorX, anchorY+100)
    else:
        wtext7 = WorldText(b"\x01", 28, bytes(" "*41 +str(difftime3), "ascii"), 1000, 0x00FF00, 0.05, anchorX, anchorY+100)
    wtext8 = WorldText(b"\x01", 15, bytes(".", "ascii"), 1000, int(bgcolor1,0), bgscale1, anchorX+bganchorX1, anchorY+bganchorY1)
    wtext9 = WorldText(b"\x01", 16, bytes(".", "ascii"), 1000, int(bgcolor2,0), bgscale2, anchorX+bganchorX2, anchorY+bganchorY2)
    wtext10 = WorldText(b"\x01", 17, bytes("=", "ascii"), 1000, int(rowcolor1,0), rowscale1, anchorX+rowanchorX1, anchorY+rowanchorY1)
    wtext11 = WorldText(b"\x01", 18, bytes("=", "ascii"), 1000, int(rowcolor2,0), rowscale2, anchorX+rowanchorX2, anchorY+rowanchorY2)
    if cp1to2time == None:
        wtext12 = WorldText(b"\x01", 29, bytes("Baseline times are not set\ncomplete a run to calibrate", "ascii"), 1000, 0xFF0000, 0.07, anchorX-15, anchorY+125)
        s1.sendto(wtext12, ('localhost', soldat_localport))
    for i in range(12):
        eval("s1.sendto(wtext"+ str(i) +", ('localhost', soldat_localport))")

def WorldTextLoop():
    while True:
        DrawSplitUI()
        time.sleep(0.1)

def ProcessCheckpointData(data):
    global tmr
    global alive
    global cp1to2time
    global cp2to3time
    global cp3to4time

    if (alive == False) and (tmr != None):                            # Reset timer on run restart
        tmr = None
    if (alive == False):
        cp1to2time = 0.0
        cp2to3time = 0.0
        cp3to4time = 0.0

    if (data[:4][3:] == b"\x02"):                                     # 01 screen space, 02 world space
        if (data[:17][13:] == b"\x00\xff\x00\x00"):                   # Active color (green)
            if (data[:26][25:] == b"\x31"):                           # Checkpoint number in ascii
                if (tmr == None):
                    tmr = time.perf_counter()                         # Start the timer
                    
            elif (data[:26][25:] == b"\x32"):                         # Reached cp2
                if (cp1to2time == 0.0 and (tmr != None)):
                    cp1to2time = round((time.perf_counter() - tmr), 3)

            elif (data[:26][25:] == b"\x33"):                         # Reached cp3
                if (cp1to2time != 0.0 and (tmr != None) and cp2to3time == 0.0):
                    cp2to3time = round((time.perf_counter() - tmr), 3)
                    
            elif (data[:26][25:] == b"\x34"):                         # Reached cp4
                if (cp2to3time != 0.0 and (tmr != None)):
                    cp3to4time = round((time.perf_counter() - tmr), 3)
                    tmr = None                                        # End of run, assuming it's a 4 lap map at most

def Server2Client():
    if useproxy:
        try:
            s2.set_proxy(socks.SOCKS5, prx.split(":")[0],int(prx.split(":")[1]))
            print ("[+] Waiting for proxy to connect...")
            s2.sendto(PacketID.pingserver + b"\x00",ConnectedServer())
            t0 = time.perf_counter()
            print ("[+] Pinging...")
            data, addr = s2.recvfrom(20)
            t1 = round((time.perf_counter() - t0) * 1000)
            print ("[+]", t1, "ms")
            print ("[+] Proxy is ready.")
            print ("Copy here: soldat://localhost:23666")
            while True:
                data,addr = s2.recvfrom(12000)
                if (data[:1] == PacketID.special):
                    ProcessCheckpointData(data)
                    s1.sendto(data, ("localhost", soldat_localport))
                else:
                    s1.sendto(data, ("localhost", soldat_localport))
        except Exception as e:
            print ("[-] Proxy failure",e)
            sys.exit()
    else:
        print ("Copy here: soldat://localhost:23666")
        s2.sendto(PacketID.pingserver + b"\x00",ConnectedServer())
        while True:
            data,addr = s2.recvfrom(12000)
            if (data[:1] == PacketID.special):
                ProcessCheckpointData(data)
                s1.sendto(data, ("localhost", soldat_localport))
            else:
                s1.sendto(data, ("localhost", soldat_localport))

Socket1Thread = Thread(target=Client2Server, daemon=True)
Socket2Thread = Thread(target=Server2Client)
WorldTextThread = Thread(target=WorldTextLoop, daemon=True)

Socket1Thread.start()
Socket2Thread.start()
WorldTextThread.start()