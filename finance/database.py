from tinydb import TinyDB

def get(name):
    return TinyDB('db/' + name + '.json')
