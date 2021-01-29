import sys
sys.dont_write_bytecode = True


def logger(func):

    def wrapper(*args, **kwargs):
        print('working on {}'.format(func.__name__))
        res = func(*args, **kwargs)
        return res
    return wrapper
