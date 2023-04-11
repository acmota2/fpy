class func:
    def __init__(self, type=None, name=None, args=None, body=None):
        self._arg_list = []
        match type:
            case 'func':
                self.name = name
                self.args = args
                self.body = body
            case _:
                print('Error on func')

    # sanity checking :shrug:
    def add_arg(self, arg):
        self._arg_list.append(arg)

    def get_arg(self):
        self._arg_list.pop()
