from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QDesktopWidget, QInputDialog, QListWidgetItem
from PyQt5.QtGui import QKeySequence

from twistedclient import SocketClientFactory
import reg_exp_handler
# import project_form_qt5_new
import project_form_new

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090

class MainForm(QWidget, project_form_new.Ui_Form):
    def __init__(self, reactor, parent=None):
        QWidget.__init__(self, parent)
        self.reactor = reactor
        self.create_client()
        self.make_connections()
        self.state = "REGISTER"
        self.text_right = 'right'
        self.text_left = 'left'
        self.text_center = 'center'
        self.users = {}
        self.name = ''
        self.current_chat = 'Common chat'
        self.init_UI()
        self.show()

    def init_UI(self):
        self.setupUi(self)
        self.center()
        self.register_handlers()
        self._start_up_creation()

    def _start_up_creation(self):
        #create common chat at the begining

        self.users_list.addItem('Common chat')
        self.users_list.setCurrentRow(0)
        self.users['Common chat'] = open('Common chat.txt', 'a')

        self.message_edit.setPlaceholderText("Enter a message....")
        self.message_edit.setMaxLength(5)

    def register_handlers(self):
        '''register all form hendlers that interact with form elements'''

        self.send_btn.clicked.connect(self.send_message)
        self.users_list.currentRowChanged.connect(self.open_history)
        self.refreshBtn.clicked.connect(self.refresh_user_list)

        self.shortcut = QKeySequence("Ctrl+Return")
        self.send_btn.setShortcut(self.shortcut)

    def create_client(self):
        self.client = SocketClientFactory(
            self.on_client_connect_success,
            self.on_client_connect_fail,
            self.on_client_receive)

    def make_connections(self):
        self.connection = self.reactor.connectTCP(SERVER_HOST, SERVER_PORT, self.client)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, "Message", "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
            self.reactor.stop()
            for user in self.users:
                f = self.users[user]
                f.close()
        else:
            QCloseEvent.ignore()

    def check_name(self):
        text, ok = QInputDialog.getText(self, "Handling chat name", "Enter a nickname")
        if ok:
            self.client.send_msg('/register {}'.format(text))
            self.name = text

    def register_name(self):
        self.state = 'CHAT'
        self.user_nickname_field.setText(self.name)
        self.user_status_field.setText("Online")
        self.add_message('We registered in chat', self.text_center, self.current_chat)
        self.client.send_msg('/users')
        self.show()

    def on_client_connect_success(self):
        # print('Connected to server. Sending...')
        # self.client.send_msg('hello')
        # self.add_message('hello', self.left)
        self.check_name()

    def on_client_connect_fail(self, reason):
        print('Connection failed: %s' % reason.getErrorMessage())

    def on_client_receive(self, msg):
        print(msg)
        if msg.startswith('/'):
            cmd = reg_exp_handler.exp_admin_strings_handler(msg)
            self.admin_strings_handler(cmd, msg)
        # else:
            # self.add_message(msg, self.text_left)
            # self._append_user_history(msg, 'recv', self.current_chat)

    def admin_strings_handler(self, cmd, msg):
        '''received messages handler'''

        # checking registration
        if self.state == 'REGISTER':
            if cmd == 'welcome':
                self.register_name()
            else:
                self.name = ''
                self.check_name()

        # getting user list and appending new users
        if cmd == 'user_list':
            users = reg_exp_handler.exp_user_list_handler(msg)

            # need to solve problem with appending users
            # self.users_list.clear()
            # self.users_list.addItem('Common chat')


            for name in users:
                if name not in self.users:
                    self.users[name] = self._create_file_history(name)
                    self.users_list.addItem(name)

        # getting private message
        if cmd == 'message':
            result = reg_exp_handler.exp_message_handler(msg)
            whome_user_nickname = result[1]
            from_user_nickname = result[2]
            message = result[3]

            # test appending timestamp to message
            message = self._make_timestamp(from_user_nickname, message)

            self._append_user_history(message, 'recv', from_user_nickname)
            # self.add_message(message, self.text_left, from_user_nickname)

        if cmd == 'all':
            result = reg_exp_handler.exp_message_to_all_handler(msg)
            from_user_nickname = result[0]
            message = result[1]
            # test appending timestamp to message
            message = self._make_timestamp(from_user_nickname, message)
            self._append_user_history(message, 'recv', 'Common chat')

        if cmd == 'connected':
            user_nickname = reg_exp_handler.connected_user_handler(msg)
            self.users[user_nickname] = self._create_file_history(user_nickname)
            self.users_list.addItem(user_nickname)

    def _create_file_history(self, name):
        f_name = '{}.txt'.format(name)
        f = open(f_name, 'a')
        # f.close()
        return f

    def _append_user_history(self, line, handler, user):
        if handler == 'recv':
            align = self.text_left
        else:
            align = self.text_right

        # user = self.current_chat if user == self.current_chat else user
        # getting file associated with user and append it
        file = self.users[user]
        file.write(line + '\n')

        # add message to history
        self.add_message(line, align, user)

    def _make_timestamp(self, user, message):
        from time import ctime
        current_time = ctime().split(" ")
        current_time_out = "{}".format(current_time[4])
        return "{}-<{}> {}".format(current_time_out, user, message)

    def send_message(self):
        from time import ctime

        # send message
        if self.current_chat == 'Common chat':
            message = '/all {} {}'.format(self.name, self.message_edit.text())
            self.client.send_msg(message)
        else:
            message = '/message {} {} {}'.format(self.current_chat, self.name, self.message_edit.text())
            self.client.send_msg(message)

        # adding time stamp
        current_time = ctime().split(" ")
        current_time_out = "{}".format(current_time[3])
        message = "{}-<{}> {}".format(current_time_out, self.name, self.message_edit.text())
        self._append_user_history(message, 'send', self.current_chat)

        # form work
        self.message_edit.setText('')

    def open_history(self, n_row):

        self.current_chat = self.users_list.item(n_row).text()
        self.message_list.clear()
        file = self.users[self.current_chat]
        file.close()
        file = open(file.name, 'r')

        for mes in file:
            mes = mes.strip()
            name = reg_exp_handler.exp_open_history_handler(mes)

            if name is None:
                continue

            aligment = self.text_right if name == self.name else self.text_left
            self.add_message(mes, aligment, self.current_chat)
        file.close()
        self.users[self.current_chat] = open(file.name, 'a')

    def add_message(self, message, aligment, chat):
        if chat != self.current_chat:
            return

        aligments = {'left':0x0001, 'right':0x0002, 'center':0x0004}
        item = QListWidgetItem(message)
        item.setTextAlignment(aligments[aligment])
        self.message_list.addItem(item)

    def refresh_user_list(self):
        self.client.send_msg('/users')

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    import qt5reactor
    qt5reactor.install()

    from twisted.internet import reactor

    main_window = MainForm(reactor)
    main_window.show()
    reactor.run()