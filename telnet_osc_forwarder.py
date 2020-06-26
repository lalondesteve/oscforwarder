#!/usr/bin/env python3

from datetime import datetime
from pythonosc import udp_client
import socketserver

class TelnetOSC(socketserver.BaseRequestHandler):
    def osc_message(self, message, ip):
        header = '/d3/showcontrol/'
        client = udp_client.SimpleUDPClient(ip, 12346)
        try:
            extension, data = message.split()
            header = header + extension.decode('utf8')
            data = int(data)
            client.send_message(header, data)
        except Exception as e:
            print(e)
            data = None
        return data

    def setup(self):
        now = datetime.now()
        print(now, ':', self.client_address[0], 'Connected!')

    def handle(self):
        while True:
            try:
                data = self.request.recv(128)
            except Exception as e:
                print(e)
                data = None
            if data and data is not '':
                print(data)
                message = self.osc_message(data.strip(), self.client_address[0])
                now = datetime.now()
                print(now, message)
            else:
                now = datetime.now()
                print(str(now), ':', self.client_address[0], 'Disconnected')
                break


class ServeOscTCP(object):
    def start(self):
        server = socketserver.ThreadingTCPServer(('', 12345), TelnetOSC)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
        finally:
            server.server_close()


if __name__ == '__main__':
    s = ServeOscTCP()
    s.start()
