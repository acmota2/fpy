class lambda_builder:
    def __init__(self, args=[], expression=None):
        self.args = args
        self.expression = expression

    def __str__(self):
        return f"lambda {self.args}: {self.expression}"
