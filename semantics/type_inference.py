import errors as err

from typing import List

class singleton:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

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
        self = self.__and__(other)

    def __mod__(self, other):
        if isinstance(other, function_) and (new := (self & (old := other.args[0]))):
            for arg in other.args:
                if arg == old:
                    arg = new
            other.args.pop(-1)
            return other if other.args else other.return_
        return None
    
    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)


class typeclass:
    generic_name = "t"
    generic_count = 0
    name = ""

    def __init__(self, generic=f"{generic_name}{generic_count}"):
        self.name = self.name
        self.generic = generic
        typeclass.generic_count += 1

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return f"{self.name}{' ' if self.name else ''}{self.generic}"

    def __repr__(self):
        return str(self)

    def __and__(self, other):
        if (type(self) != type(other) and (issubclass(type(other), composite) and other.check(type(self))))\
            or issubclass(type(other), type(self)):
            return other
        if self == other or issubclass(type(self), type(other)):
            self.generic = self.generic if self.generic > other.generic else other.generic
            return self
        return None

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        self = self.__and__(other)

    def __mod__(self, other):
        if isinstance(other, function_) and (new := (self & (old := other.args[0]))):
            for arg in other.args:
                if arg == old:
                    arg = new
            other.args.pop(-1)
            return other if other.args else other.return_
        return None
    
    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)


class Any_(typeclass):
    pass


class Eq(Any_):
    name = "Eq"
    generic_name = "t"
    generic_count = 0

    def __init__(self, generic=f"{generic_name}{generic_count}"):
        self.name = self.name
        self.generic = generic
        Eq.generic_count += 1
    pass


class Ord(Eq):
    name = "Ord"
    generic_name = "t"
    generic_count = 0

    def __init__(self, generic=f"{generic_name}{generic_count}"):
        self.name = self.name
        self.generic = generic
        Ord.generic_count += 1

    pass


class Num(Ord):
    name = "Num"
    generic_name = "t"
    generic_count = 0

    def __init__(self, generic=f"{generic_name}{generic_count}"):
        self.name = self.name
        self.generic = generic
        Num.generic_count += 1

    pass


class composite:
    def __init__(self, name, content):
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
            for arg in other.args:
                if arg == old:
                    arg = new
            other.args.pop(-1)
            return other
        return None 
    
    def __rmod__(self, other):
        return self.__mod__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)


class int_(singleton, Num, Ord):
    def __init__(self, name="int"):
        self.name = name
    pass


class bool_(singleton, Eq):
    def __init__(self, name="bool"):
        self.name = name
    pass


class float_(singleton, Num, Ord):
    def __init__(self, name="float"):
        self.name = name
    pass


class char_(singleton, Ord):
    def __init__(self, name="char"):
        self.name = name
    pass


class list_(composite, Any_):
    content: Any_ | None
    name = '[]'

    def __init__(self, name=name, content=Any_()):
        self.name = list_.name
        self.content = content

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
        print(issubclass(type(self.content), Ord))
        return issubclass(type(self.content), Ord)

    def _check_is_eq(self):
        if issubclass(type(self.content), composite):
            return self.content._check_is_eq()
        return issubclass(type(self.content), Eq)


class tuple_(composite, Any_):
    name = "()"
    content: List[Any_] | None

    def __init__(self, name="()", content=[]):
        self.name = name
        self.content = content

    def __str__(self):
        return f"{*(self.content),}" if self.content else "()"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.content == other.content

    def __and__(self, other):
        if isinstance(other, tuple_):
            zipped = [x & y for (x, y) in zip(self.content, other.content)]
            if len(self.content) != len(other.content) and not all(zipped):
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


class function_(Any_):
    def __init__(self, name, return_, args=None):
        self.name = 'function'
        self.args = args
        self.return_ = return_

    def __eq__(self, other):
        return self.return_ == other.return_ and self.args == other.args

    def __str__(self):
        if len(self.args) > 2:
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
            return function_(f"{self.name}{other.name}", new_return, args=new_args.content)\
                if new_args and new_return\
                else None
        return None

    def __rand__(self, other):
        return self.__and__(other)

    def __iand__(self, other):
        self = self.__and__(other)

    def right_mod(self, other):
        if len(self.args) > 2 and (new := (other & (old := self.args[2]))):
            self.args.pop(-2)
            for arg in self.args:
                if arg == old:
                    arg = new
            return self
        return None

    def __mod__(self, other):
        if isinstance(other, function_) and (new := (other & (old := self.args[0]))):
            for arg in self.args:
                if arg == old:
                    arg = new
            self.args.pop(-1)
            return self if self.args else self.return_
        return other % self

    def __rmod__(self, other):
        return self.__mod__(other)
    
    def _imod__(self, other):
        return self.__mod__(other)

    def check_arguments(self) -> Any_:
        for arg in self.args:
            yield arg


if __name__ == '__main__':
    print(f"Showing int & bool:", int_() & bool_())
    x = tuple_()
    x.content = [int_(), int_()]
    print(f"Showing (int, int) & Eq:", x & Eq())
    print(f"Showing Eq & (int, int):", Eq() & x)
    y = list_(content=int_())
    print(f"Showing [int] & Eq:", y & Eq())
    print(f"Showing Eq & [int]:", Eq() & y)
    z = function_('[+]', Num('a'), args=[Num('a'), Num('a')])
    w = function_('div', int_(), args=[int_(), int_()])
    a = function_('and', bool_(), args=[bool_(), bool_()])
    print(f"Showing ((Num a, Num a) -> Num a) & ((int, int) -> int):", z & w)
    print(f"Showing ((int, int) -> int) & ((Num a, Num a) -> Num a):", w & z)
    print(f"Showing {a} & {w}:", a & w)
    print(f"Showing {w} & {a}:", w & a)
    print(f"Showing {w} % int:", w % int_())
    print(f"Showing int % {w}:", int_() % w)
    print(f"Showing int % int:", int_() % int_())
