
def log(msg, task=-1, debug=False):
    task_str = '[TASK ' + str(task) + ']: ' if task != -1 else ''
    print(task_str + msg)
