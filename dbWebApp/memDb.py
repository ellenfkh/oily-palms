## teeny tiny database, for proof of concept and unittests only

class Table:

    def __init__(self, debug=True):
        self.debug = debug
        self.table = dict()

    def __getitem__(self, key):
        value = self.table[key]
        return value

    def __setitem__(self, key, value):
        self.table[key] = value

