from __future__ import absolute_import, division, print_function

from ..ServerManager import BidirectionalOSCServer, OSCMessage

class EspGrid:
    def __init__(self, address=("localhost", 5510)):

        self.server_address = address

        self.server = BidirectionalOSCServer()
        self.server.connect(self.server_address)

    #     self.server.addMsgHandler('/test', self.test)

    # def test(self, *args):
    #     print(args)
    #     return

    def set_clock_mode(self, value):
        message = OSCMessage("/esp/clockMode/s")
        message.append(int(value))
        return self.server.send(message)

    def get_clock_mode(self):
        self.server.send(OSCMessage("/esp/clockMode/q"))
        return self.server.receive("/esp/clockMode/r")

    # Tempo information

    def query(self):
        self.server.send(OSCMessage("/esp/clock/q"))
        return self.server.receive("/esp/clock/r")

    def get_tempo(self):
        """ Queries the EspGrid Server for tempo and return a list
            
            [is_running, tempo, seconds, nanoseconds, beat]
            
        """
        self.server.send(OSCMessage("/esp/tempo/q"))
        return self.server.receive("/esp/tempo/r")

    def toggle_tempo(self, flag):
        message = OSCMessage("/esp/beat/on")
        message.append(flag)
        return self.server.send(message)

    def start_tempo(self):
        return self.toggle_tempo(1)

    def stop_tempo(self):
        return self.toggle_tempo(0)

    def set_tempo(self, value):
        message = OSCMessage("/esp/beat/tempo")
        message.append(float(value))
        return self.server.send(message)

    def get_start_time(self):
        data = self.get_tempo()
        sec, nano = data[2], data[3]
        return float("{}.{}".format(sec, nano))

    # Subcription to immediate messages

    def subscribe(self):
        message = OSCMessage("/esp/subscribe")
        return self.server.send(message)

    def unsubscribe(self):
        message = OSCMessage("/esp/unsubscribe")
        return self.server.send(message)

    # Identification

    def set_name(self, name):
        message = OSCMessage("/esp/person/s")
        message.append(str(name))
        return self.server.send(message)

    def get_name(self):
        self.server.send(OSCMessage("/esp/person/q"))
        return self.server.receive("/esp/person/r")

    def set_machine_name(self, name):
        message = OSCMessage("/esp/machine/s")
        message.append(str(name))
        return self.server.send(message)

    def get_machine_name(self):
        self.server.send(OSCMessage("/esp/machine/q"))
        return self.server.receive("/esp/machine/r")

    # Sending messages
    def now(self, args):
        message = OSCMessage("/esp/msg/now")
        message.append(args)
        return self.server.send(message)

    def soon(self, args):
        message = OSCMessage("/esp/msg/soon")
        message.append(args)
        return self.server.send(message)

    def future(self, seconds, nanoseconds, args):
        message = OSCMessage("/esp/msg/future")
        message.append([seconds, nanosecons, args])
        return self.server.send(message)

    # Receiving
    def recv(self, pattern):
        return self.server.receive(pattern)

