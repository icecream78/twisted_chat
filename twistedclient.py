"""
Simple socket client using Twisted.
Eli Bendersky (eliben@gmail.com)
This code is in the public domain
"""
import struct

from twisted.internet.protocol import Protocol, ClientFactory

class SocketClientProtocol(Protocol):

    def dataReceived(self, data):
        self.factory.got_msg(data)
        # print('this we take {}'.format(data.decode('utf-8')))

    def connectionMade(self):
        self.factory.clientReady(self)


class SocketClientFactory(ClientFactory):
    """ Created with callbacks for connection and receiving.
        send_msg can be used to send messages when connected.
    """
    protocol = SocketClientProtocol

    def __init__(
            self,
            connect_success_callback,
            connect_fail_callback,
            recv_callback):
        self.connect_success_callback = connect_success_callback
        self.connect_fail_callback = connect_fail_callback
        self.recv_callback = recv_callback
        self.client = None

    def clientConnectionFailed(self, connector, reason):
        self.connect_fail_callback(reason)

    def clientReady(self, client):
        self.client = client
        self.connect_success_callback()

    def got_msg(self, msg):
        print("Receaving")
        print(msg.decode("utf-8"))
        self.recv_callback(msg.decode("utf-8").strip())


    def send_msg(self, msg):
        if self.client:
            # self.client.sendString(msg.encode())
            self.client.transport.write('{}\n'.format(msg).encode())

# from twisted.internet import reactor
#
# reactor.listenTCP(9090, SocketClientFactory())
# reactor.run()


# """
# Simple socket client using Twisted.
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
# """
# import struct
#
# from twisted.internet.protocol import Protocol, ClientFactory
# from twisted.protocols.basic import IntNStringReceiver
#
#
# class SocketClientProtocol(Protocol):
#     """ The protocol is based on twisted.protocols.basic
#         IntNStringReceiver, with little-endian 32-bit
#         length prefix.
#     """
#     # structFormat = "<L"
#     # prefixLength = struct.calcsize(structFormat)
#
#     def dataReceived(self, data):
#         self.factory.got_msg(data)
#         print('Receive {}'.format(data.decode('utf-8')))
#         # print('this we take {}'.format(data.decode('utf-8')))
#
#     def connectionMade(self):
#         self.factory.clientReady(self)
#         # self.factory.send_msg('echo'.encode())
#         self.transport.write('echo'.encode())
#
# class SocketClientFactory(ClientFactory):
#     """ Created with callbacks for connection and receiving.
#         send_msg can be used to send messages when connected.
#     """
#     protocol = SocketClientProtocol
#
#     # def __init__(
#     #         self,
#     #         connect_success_callback,
#     #         connect_fail_callback,
#     #         recv_callback):
#     #     self.connect_success_callback = connect_success_callback
#     #     self.connect_fail_callback = connect_fail_callback
#     #     self.recv_callback = recv_callback
#     #     self.client = None
#
#     def clientConnectionFailed(self, connector, reason):
#         # self.connect_fail_callback(reason)
#         pass
#
#     def clientReady(self, client):
#         self.client = client
#         # self.connect_success_callback()
#
#     def got_msg(self, msg):
#         # self.recv_callback(msg.decode("utf-8").strip())
#         print(msg.decode("utf-8"))
#
#     def send_msg(self, msg):
#         if self.client:
#             # self.client.sendString(msg.encode())
#             self.client.transport.write('{}\n'.format(msg).encode())
#
# from twisted.internet import reactor
#
# reactor.connectTCP('localhost', 9090, SocketClientFactory())
# reactor.run()
