from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import reg_exp_handler as re_handle

class Chat(LineReceiver):
    '''created for every user and implement him'''

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "REGISTER"
        self.current_chat = "common"

    def connectionMade(self):
        '''setting up few properies about connected user'''

        self._peer = self.transport.getPeer()
        self._client = self.transport.client
        print(self._peer)

    def connectionLost(self, reason):
        '''removing user from the users list'''

        if self.name in self.users:
            del self.users[self.name]

    def dataReceived(self, data):
        '''handler for received data. It matching to pattern and then process'''

        data = data.decode("utf-8")
        if data.startswith('/register '):
            self.handle_GETNAME(data)
        elif data.startswith('/users'):
            self.send_user_list()
        elif data.startswith('/message '):
            self.send_message_user(data)
        elif data.startswith('/all '):
            self.send_massages_all(data)

    def handle_GETNAME(self, line):
        '''registration handler'''

        line = line.strip().split(' ')
        if len(line) > 2:
            self.sendLine('Error with nickname. Choose another'.encode())
            return

        if line[1] in self.users:
            self.sendLine("This name was taken. Please, choose another".encode())
            return

        self.name = line[1]
        self.users[self.name] = self
        self.state = "CHAT"
        self.sendLine("/welcome".encode())

        # sending all users request about adding new user
        for user in self.users:
            if user != self.name:
                self.users[user].sendLine('/connected {}'.format(self.name).encode())

    def _make_timestamp(self, message):
        '''setting up timestamp to message'''

        from time import ctime
        current_time = ctime().split(" ")
        current_time_out = "{}".format(current_time[3])
        return "{}-<{}> {}".format(current_time_out, self.name, message)

    def send_user_list(self):
        '''sending user list for request'''

        send_string = '/user_list {};'.format(';'.join(self.users))
        self.sendLine(send_string.encode())

    def send_message_user(self, line):
        '''parsing message with pattern /message [whome] [from] [message] and sending it'''

        result_tuple = re_handle.exp_message_handler(line)
        whome_user_nickname = result_tuple[1]
        from_user_nickname = result_tuple[2]
        message = '/message {} {} {}'.format(whome_user_nickname, from_user_nickname, result_tuple[3])
        if whome_user_nickname in self.users:
            self.current_chat = self.users[whome_user_nickname]
            self.current_chat.sendLine(message.encode())
            self.current_chat = "common"

    def send_massages_all(self, data):
        '''sending message for all users in common chat'''

        for name in self.users:
            if name != self.name:
                self.users[name].sendLine(data.strip().encode())

class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)

reactor.listenTCP(9090, ChatFactory())
reactor.run()


# from twisted.internet.protocol import Factory
# from twisted.protocols.basic import LineReceiver
# from twisted.internet import reactor
#
# class Chat(LineReceiver):
#     def __init__(self, users):
#         self.users = users
#         self.name = None
#         self.state = "REGISTER"
#         self.current_chat = "common"
#
#     def connectionMade(self):
#         print("user connected")
#         # self.sendLine("What is your name?".encode())
#     def dataReceived(self, line):
#         if line.decode("utf-8") == "/users":
#             pass
#         elif line.decode("utf-8").startswith("/message "):
#             pass
#         elif line.decode("utf-8").startswith("/register "):
#             self.sendLine('/welcome'.encode())
#         else:
#             self.sendLine(line)
#
# class ChatFactory(Factory):
#     def __init__(self):
#         self.users = {}
#
#     def buildProtocol(self, addr):
#         return Chat(self.users)
#
# reactor.listenTCP(9090, ChatFactory())
# reactor.run()