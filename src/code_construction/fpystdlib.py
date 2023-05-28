from typing import Any, Callable

add =       "lambda x, y: x + y"
sub =       "lambda x, y: x - y"
mul =       "lambda x, y: x * y"
frac =      "lambda x, y: x / y"
div =       "lambda x, y: x // y"
mod =       "lambda x, y: x % y"
ppow =      "lambda x, y: x**y"
gt =        "lambda x, y: x > y"
lt =        "lambda x, y: x < y"
gte =       "lambda x, y: x >= y"
lte =       "lambda x, y: x <= y"
eq =        "lambda x, y: x == y"
neq =       "lambda x, y: x != y"
aand =      "lambda x, y: x and y"
oor =       "lambda x, y: x or y"
nnot =      "lambda x: not x"
from_int =  "lambda x: float(x)"

"""fpy
alias string = [char]

# __builtin__
fdef not(x: bool) -> bool {
    undefined
}

fdef compose(f: (b) -> c, g: (a) -> b, a: a) -> c {
    f(g(a))
}

# __builtin__
fdef from_int(x: int) -> float {
    undefined
}

fdef foldl(_: (b,a) -> b, acc: b, []: [a]) -> b { acc }
fdef foldl(f,acc,[h|t]) {
    foldl(f,f(acc,h),t)
}

fdef foldr(_: (a,b) -> b, acc: b, []: [a]) -> b { acc }
fdef foldr(f,acc,[h|t]) {
    f(h,foldr(f,acc,t))
}

fdef concatenate([],l) { l }
fdef concatenate(l,[]) { l }
fdef concatenate([h|t], l) {
    [h | concatenate(t, l)]
}

fdef func_prod(f: (a) -> c, g: (b) -> d, (a,b): (a,b)) -> (c,d) {
    (f(a), g(b))
}

fdef map_(_: (a) -> b, []: [a]) -> [b] { [] }
fdef map_(f, [h|t]) {
    [f(h) | map_(f,t)]
}

fdef filter_(_: (a) -> bool, []: [a]) { [] }
fdef filter_(f,[h|t]) {
    [?..?] {
        f(h): [h | filter_(f,t)],
        else: filter_(f,t)
    }
}

fdef concat([]) { [] }
fdef concat([[h|t]|t2]) {
    [h | t ++ concat(t2)]
}
"""
