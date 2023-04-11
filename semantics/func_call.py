class func_call:
    def __init__(self, type=None, args=None):
        if type == 'func_call':
            self.type = type
            self.args = args
            self.id = None
        else:
            print('Error on func_call')

    def add_arg(self, arg):
        self.args.append(arg)

    def add_id(self, id):
        self.id = id
