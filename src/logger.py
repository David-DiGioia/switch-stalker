import datetime

log_file = None


def init_logger():
    global log_file
    date = str(datetime.datetime.now()).replace(':', '.')
    log_file = open('..\\log\\' + date + '.txt', 'w')


def close_logger():
    log_file.close()


def log(msg, task=-1, debug=False):
    task_str = '[TASK ' + str(task) + ']: ' if task != -1 else ''
    log_msg = str(datetime.datetime.now()) + ' ' + task_str + msg
    print(log_msg)
    log_file.write(log_msg)
