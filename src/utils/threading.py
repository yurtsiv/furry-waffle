import threading

def set_interval(func, sec):
    """
    Execute the given function periodically on a separate thread
    """
    stopped = threading.Event()

    def func_wrapper():
        while not stopped.wait(sec):
            func()

    t = threading.Thread(target=func_wrapper)
    t.daemon = True
    t.start()

    return stopped