import sys
sys.path.insert(0, '/home/ahmer/Ahmer/Techknox/Python_Exercises/IoT-Gateway-V2/coapthon/')
from coapthon.server.coap import CoAP
from coapserver import CoAPServer


        
ip = "192.168.10.4"
port = 5683
multicast=False

coap = CoAPServer(ip,port,multicast)
coap.main_2()
if KeyboardInterrupt:
    print "BYE!!!"
    exit(0)


