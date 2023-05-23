class list_builder:
    def __init__(self, head=None, actual_list=[]):
        self.head = head
        self.actual_list = actual_list

    def __str__(self):
        if self.head:
            return f"[{self.head}] + {self.actual_list}"
        return str(self.actual_list)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.head == other.head and self.actual_list == other.actual_list
