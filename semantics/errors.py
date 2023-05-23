red_bold = lambda x: f'\x1b[1;31m{x}\x1b[0;0m'
yellow_bold = lambda x: f'\x1b[1;33m{x}\x1b[0;0m'
cian_bold = lambda x: f'\x1b[1;36m{x}\x1b[0;0m'

detuple = lambda x: f'{x[0]}:{x[1]}'

class argument_error(Exception):
    def __init__(
        self,
        fname,
        previous_type,
        current_type,
        line_info_prev,
        line_info_cur
        ):
        self.fname = fname
        self.previous_type = previous_type
        self.current_type = current_type
        self.line_info_prev = line_info_prev
        self.line_info_cur = line_info_cur

    def __str__(self):
        return f'''Error defining {cian_bold(self.fname)}:
    Found two conflicting definitions:
        Definition 1: {yellow_bold(self.previous_type)} on lines {detuple(self.line_info_prev)}
        Definition 2: {red_bold(self.current_type)} on lines {detuple(self.line_info_cur)}
        '''

    def __repr__(self):
        return str(self)

class type_error(Exception):
    ...

class class_name_error(Exception):
    ...

class name_already_defined(Exception):
    ...
