import re

exp_open_history_handler_pattern = r'<([\d\w_-]*)>'
exp_admin_strings_handler_pattern = r'^/(\w*)'
exp_user_list_handler_pattern = r'([\d\w_-]*);'
exp_message_handler_pattern = r'^/(\w*) ([\d\w_-]*) ([\d\w_-]*) (.*)'
exp_message_to_all_handler_pattern = r'/all ([\d\w_-]*) (.*)'
connected_user_handler_pattern = r'/connected ([\d\w_-]*)'

def exp_open_history_handler(mes):
    # pattern = r'<([\d\w_-]*)>'
    pattern = re.compile(exp_open_history_handler_pattern)
    name = pattern.search(mes)
    # if name is None:
    #     return None
    # else:
    #     return name.groups()[0]
    return None if name is None else name.groups()[0]

def exp_admin_strings_handler(line):
    # pattern = r'^/(\w*)'
    pattern = re.compile(exp_admin_strings_handler_pattern)
    cmd = pattern.search(line)
    # return None if cmd is None else cmd.groups()[0]
    return cmd.groups()[0]

def exp_user_list_handler(line):
    # pattern = r'([\d\w_-]*);'
    pattern = re.compile(exp_user_list_handler_pattern)

    # return users list from command
    return pattern.findall(line)

def exp_message_handler(line):
    pattern = r'^/(\w*) ([\d\w_-]*) ([\d\w_-]*) (.*)'
    pattern = re.compile(exp_message_handler_pattern)

    # return list of [cmd, whome_user, from_user, message]
    return pattern.search(line).groups()

def exp_message_to_all_handler(line):
    # pattern = r'/all ([\d\w_-]*) (.*)'
    pattern = re.compile(exp_message_to_all_handler_pattern)

    # return message string
    return pattern.search(line).groups()

def connected_user_handler(line):
    # pattern = r'/connected ([\d\w_-]*)'
    pattern = re.compile(connected_user_handler_pattern)

    # return connected user nickname
    return pattern.search(line).group(1)