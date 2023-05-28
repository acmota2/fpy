from typing import List

def reset_generics():
    typeclass.generic_count = 0
    Num.generic_count = 0
    Eq.generic_count = 0
    Any_.generic_count = 0
    Ord.generic_count = 0

class singleton:
    def __init__(self, name: str, typename):
        self.name = name
        self.typename = typename

    def __str__(self):
        return self.typename

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __and__(self, other):
        if self == other or issubclass(type(self), type(other)):
            return self
        return None

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        return self.__and__(other)

    def __mod__(self, other):
        if isinstance(other, function_) and (t := (self & other.args[0])):
            x = other.args[1:]
            old = other.args[0]
            for i in range(len(x)):
                if x[i] == old:
                    x[i] = other
            if old == other.return_:
                other.return_ = old
            return (
                function_(name=other.name, args=x, return_=other.return_)
                if x 
                else other.return_
            )
        return None

    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)
    
    def __hash__(self):
        return hash(str(self))
    
    def retrieve_name_type(self):
        return [(self.name, self)]


class typeclass:
    generic_name = "t"
    generic_count = 0

    def __init__(self, name='', class_name='', generic=None):
        self.name = name
        self.class_name = class_name
        self.generic = generic \
            if generic \
            else f"{self.generic_name}{self.generic_count}"
        

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return f"{self.class_name}{' ' if self.class_name else ''}{self.generic}"

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        other_is_sub = issubclass(type(other), type(self))
        other_is_singleton = issubclass(type(other), singleton)
        other_is_function = issubclass(type(other), function_)
        if (type(self) != type(other) and (issubclass(type(other), composite) and other.check(type(self))))\
            or (other_is_sub and other_is_singleton) or (other_is_function and type(self) == Any_):
            return other
        if other_is_sub:
            other.generic = self.generic if self.generic < other.generic else other.generic
            return other
        if issubclass(type(self), type(other)):
            self.generic = self.generic if self.generic < other.generic else other.generic
            return self
        return None

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        return self.__and__(other)

    def __mod__(self, other):
        if isinstance(other, function_) and (new := (self & (old := other.args[0]))):
            x = other.args[1:]
            old = other.args[0]
            for i in range(len(x)):
                if x[i] == old:
                    x[i] = other
            if old == other.return_:
                other.return_ = old
            return (
                function_(name=other.name, args=x, return_=other.return_)
                if x 
                else other.return_
            )
        return None

    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)
    
    def __hash__(self):
        return hash(str(self))

    def retrieve_name_type(self):
        return [(self.name, self)]


class Any_(typeclass):
    def __init__(self, name='', generic=None):
        self.name = name
        self.generic = f"t{typeclass.generic_count}" if not generic else generic
        self.class_name = ''
    pass

class Eq(Any_):
    class_name = "Eq"
    generic_name = "t"
    generic_count = 0

    def __init__(self, name='', class_name=class_name, generic=None):
        self.name = name
        self.class_name = class_name
        self.generic = generic \
            if generic \
            else f"{self.generic_name}{typeclass.generic_count}"
    pass


class Ord(Eq):
    class_name = "Ord"
    generic_name = "t"
    generic_count = 0

    def __init__(self, name='', class_name=class_name, generic=None):
        self.name = name
        self.class_name = class_name
        self.generic = generic \
            if generic \
            else f"{self.generic_name}{typeclass.generic_count}"
        
    pass


class Num(Ord):
    class_name = "Num"
    generic_name = "t"
    generic_count = 0

    def __init__(self, name='', class_name=class_name, generic=None):
        self.name = name
        self.class_name = class_name
        self.generic = generic \
            if generic \
            else f"{self.generic_name}{typeclass.generic_count}"
        

    pass


class composite:
    def __init__(self, content):
        pass

    def __eq__(self, other):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        return str(self)

    def check(self, typeclass_: type) -> bool:
        if typeclass_ == Any_:
            return True
        if typeclass_ == Ord:
            return self._check_is_ord()
        if typeclass_ == Eq:
            return self._check_is_eq()
        return False

    def _check_is_ord(self):
        pass

    def _check_is_eq(self):
        pass

    def __and__(self, other):
        pass

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        return self.__and__(other)
    
    def __mod__(self, other):
        if isinstance(other, function_) and (new := self & (old := other.args[0])):
            x = other.args[1:]
            old = other.args[0]
            for i in range(len(x)):
                if x[i] == old:
                    x[i] = other
            if old == other.return_:
                other.return_ = old
            return (
                function_(name=other.name, args=x, return_=other.return_)
                if x 
                else other.return_
            )
        return None 

    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)



class int_(singleton, Num, Ord):
    def __init__(self, name='', typename="int"):
        self.name = name
        self.typename = typename
    pass


class bool_(singleton, Eq):
    def __init__(self, name='', typename="bool"):
        self.name = name
        self.typename = typename
    pass


class float_(singleton, Num, Ord):
    def __init__(self, name='', typename="float"):
        self.name = name
        self.typename = typename
    pass


class char_(singleton, Ord):
    def __init__(self, name='', typename="char"):
        self.name = name
        self.typename = typename
    pass


class list_(composite, Any_):
    content: Any_ | None
    name = '[]'

    def __init__(self, name='', content=Any_(), is_empty=True):
        self.name = name
        self.content = content
        self.is_empty = is_empty

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return f"[{str(self.content)}]" if self.content else "[]"

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        if isinstance(other, list_):
            return list_(content=self.content & other.content)
        if isinstance(other, typeclass) and self.check(type(other)):
            return self
        return None

    def _check_is_ord(self) -> bool_:
        if issubclass(type(self.content), composite):
            return self.content._check_is_ord()
        return issubclass(type(self.content), Ord)

    def _check_is_eq(self):
        if issubclass(type(self.content), composite):
            return self.content._check_is_eq()
        return issubclass(type(self.content), Eq)

    def __hash__(self):
        return hash(str(self))
    
    def retrieve_name_type(self):
        if self.name:
            return [(self.name, self)]
        return self.content.retrieve_name_type()

class htlist_(list_):
    def __init__(self, name='', content=Any_, tail=Any_, is_empty=False):
        t = content & tail.content if type(tail) != Any_ else content & tail
        self.name = name
        self.content = t
        self.tail = list_(content=t)
        self.is_empty = is_empty

    def __eq__(self, other):
        return str(self) == str(other)
    
    def __str__(self):
        return '[]' if self.is_empty else f'[{self.content}]'
    pass

class discrete_list(list_):
    def __init__(self, name='', content=[Any_], is_empty=False):
        self.name = name
        self.content = content
        self.is_empty = is_empty
    pass

class tuple_(composite, Any_):
    content: List[Any_] | None

    def __init__(self, name='', content=[], is_empty=True):
        self.name = name
        self.content = content
        self.is_empty = is_empty

    def __str__(self):
        return f"{*(self.content),}" if self.content else "()"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __and__(self, other):
        if isinstance(other, tuple_):
            zipped = [x & y for (x, y) in zip(self.content, other.content)]
            if len(self.content) != len(other.content) or not all(zipped):
                return None
            else:
                self.content = zipped
                return self
        if isinstance(other, typeclass) and self.check(type(other)):
            return self
        return None

    def _check_is_ord(self):
        is_ord = lambda c: (
            issubclass(type(c), composite) and c._check_is_ord()
        ) or issubclass(type(c), Ord)
        return all(map(is_ord, self.content))

    def _check_is_eq(self):
        is_eq = lambda c: (issubclass(type(c), composite) and c._check_is_eq()) or issubclass(type(c), Eq)
        return all(map(is_eq, self.content))
    
    def __hash__(self):
        return hash(str(self))
    
    def retrieve_name_type(self):
        if self.name:
            return [(self.name, self)]
        r = []
        for x in self.content:
            r.extend(x.retrieve_name_type())
        return r

class function_(Any_):
    def __init__(self, name='', return_=None, args=[]):
        self.name = name
        self.args = args
        self.return_ = return_

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        if len(self.args) >= 2:
            return f"{(*(self.args),)} -> {self.return_}"
        return f"({self.args[0]}) -> {self.return_}" if self.args else f"() -> {self.return_}"

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        is_function = isinstance(other, function_)
        if isinstance(other, Any_) and not is_function:
            return self
        if is_function:
            new_args = tuple_(content=self.args) & tuple_(content=other.args)
            new_return = self.return_ & other.return_
            return function_(name=f"{self.name}{other.name}", return_=new_return, args=new_args.content)\
                if new_args and new_return\
                else None
        return None

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        return self.__and__(other)

    def right_mod(self, other):
        if len(self.args) > 1 and other & self.args[1]:
            x = self.args[:]
            x.pop(1)
            old = self.args[1]
            for i in range(len(x)):
                if x[i] == old:
                    x[i] = other
            if old == self.return_:
                self.return_ = old
            return function_(name=self.name, args=x, return_=self.return_)
        return None

    def __mod__(self, other):
        if other & self.args[0]:
            x = self.args[1:]
            old = self.args[0]
            for i in range(len(x)):
                if x[i] == old:
                    x[i] = other
            if old == self.return_:
                self.return_ = old
            return (
                function_(name=self.name, args=x, return_=self.return_) 
                if x != []
                else self.return_
            )
        return other.__mod__(self)

    def __rmod__(self, other):
        return self.__mod__(other)
    
    def _imod__(self, other):
        return self.__mod__(other)
    
    def __hash__(self):
        return hash(str(self))

    def check_arguments(self) -> Any_:
        for arg in self.args:
            yield arg

    def retrieve_name_type(self):
        return [(self.name, self)]

# não me livrava mesmo duma travessia duma RoseTree pois não?
def flatmap_type(t) -> list[Any_]:
    types = []
    stack = [t]
    while stack != []:
        match t_ := stack.pop(0):
            case htlist_():
                stack = [t_.content, t_.tail] + stack
            case discrete_list() | tuple_():
                stack = [t_.content] + stack
            case list_():
                stack = [t_.content] + stack
            case int_() | char_() | bool_() | float_() |\
                Any_() | Num() | Eq() | Ord():
                types.append(t_)
    return types

if __name__ == '__main__':
    print(f"Showing int & Num a:", int_() & Num(generic='a'))
    print(f"Showing int & bool:", int_() & bool_())
    x = tuple_()
    x.content = [int_(), int_()]
    print(f"Showing (int, int) & Eq:", x & Eq())
    print(f"Showing Eq & (int, int):", Eq() & x)
    y = list_(content=int_())
    print(f"Showing [int] & Eq:", y & Eq())
    print(f"Showing Eq & [int]:", Eq() & y)
    z = function_(Num('a'), args=[Num(generic='a'), Num(generic='a')])
    w = function_(return_=int_(), args=[int_(), int_()])
    a = function_(return_=bool_(), args=[bool_(), bool_()])
    print(f"Showing ((Num a, Num a) -> Num a) & ((int, int) -> int):", z & w)
    print(f"Showing ((int, int) -> int) & ((Num a, Num a) -> Num a):", w & z)
    print(f"Showing {a} & {w}:", a & w)
    print(f"Showing {w} & {a}:", w & a)
    print(f"Showing {w} % int:", w % int_())
    print(f"Showing int % {w}:", int_() % w)
    print(f"Showing int % int:", int_() % int_())
    b = tuple_(content=[htlist_(head=bool_(), content=list_(content=bool_())), char_(), int_(), Num(generic='a')])
    print(f"Showing flatmap {b}, being the list a htlist:", flatmap_type(b))
