class ffunction:
    def __init__(self, nome, args, declareCode, returnCode):
        self.nome = nome
        self.code = [(args, declareCode, returnCode)]
    def addDefinition(self, args, declareCode, returnCode):
        self.code.append((args, declareCode, returnCode))
    def buildString(self):
        s = f"""\
def {self.nome}(*___t):
    if len(___t) == 1:
        ___t = ___t[0]
    match ___t:"""
        for a, d, r in self.code:
            s += f"""
        case {a}:"""
        
            if not d is None:
                s += f"""
            {d}"""
            s+=f"""
            return {r}"""
        return s




# x = ffunction("foldr", "(_,acc,[])", None, "acc")
# x.addDefinition("(f,acc,(h, *t))", "acc2 = foldr(f, acc, t)", "f(h,acc2)")
# print(x.buildString())