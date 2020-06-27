#!/usr/bin/env python3

from datetime import datetime
from pythonosc import udp_client
import socketserver

# Define constants
INPORT = 12345      # TCP receive port
OUTPORT = 12346     # osc send port

# TODO: logging, args?

class TelnetOSC(socketserver.BaseRequestHandler):
    # handler to convert message to osc
    def osc_message(self, message, ip):
        # build /d3/showcontrol osc message
        header = '/d3/showcontrol/'
        client = udp_client.SimpleUDPClient(ip, OUTPORT)
        try:
            extension, data = message.split()
            header = header + extension
            data = int(data)
            # send message back to the client
            client.send_message(header, data)
        except Exception as e:
            print(e)

    def setup(self):
        self.client = self.client_address[0]
        self.now = datetime.now()

    def handle(self):
        # receive message, parse and pass it to osc_message
        while True:
            try:
                # short messages are expected
                data_bytes = self.request.recv(128)
                data = data_bytes.decode('utf8')
            except Exception as e:
                print(e)
                data = None
            if data and data is not '':
                # sanity check before parsing
                self.osc_message(data.strip(), self.client)
            print(self.now, ':', self.client, "'" + data + "'")
            break


class ServeOscTCP(object):
    # Run threaded server with TelnetOSC handler
    def start(self):
        server = socketserver.ThreadingTCPServer(('', INPORT), TelnetOSC)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            # this is probably redundant with the finally clause
            server.server_close()
        finally:
            server.server_close()


if __name__ == '__main__':
    s = ServeOscTCP()
    s.start()
