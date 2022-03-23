import socket
import socketserver
import time
class Socket_function():
    def sendeStr(self,komm_s, datenStr):
        datenBytes = bytes(datenStr, 'utf-8')
        komm_s.sendall(datenBytes)
        self.sendeTrennByte(komm_s)

    def sendeTrennByte(self,komm_s):
        trennByte = bytes([0])
        komm_s.sendall(trennByte)

    def empfangeStr(self,komm_s):

        weiter = True
        datenBytes = bytes()

        trennByte = bytes([0])

        while weiter:
            chunk = komm_s.recv(1)
            if chunk == trennByte or chunk == bytes([]):
                weiter = False
            else:
                datenBytes = datenBytes + chunk

        datenStr = str(datenBytes, 'utf-8')

        return datenStr
