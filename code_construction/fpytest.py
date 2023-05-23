'''fpy
# functional

fdef foldl(_,acc,[]) { acc }
fdef foldl(f,acc,[h|t]) {
    foldl(f,f(acc,h),t)
}

fdef foldr(_,acc,[]) { acc }
fdef foldr(f,acc,[h|t]) {
    let { _ = foldr(f,acc,t) }
    f(acc,h)
}

fdef map(_,[]) { [] }
fdef map(f,[h|t]) {
    [ f(h) | map(f,t) ]
}

fdef filter(_,[]: Eq) -> [a] { [] }
fdef filter(f,[h|t]) {
    [?..?] {
        f(h): filter(f,t),
        else: [ h | filter(f,t) ]
    }
}

fdef curry(f,a,b) {
    f((a,b))
}

fdef uncurry(f,(a,b)) {
    f(a,b)
}

fdef [.](f,g,a) {
    f . g
}

# lists

fdef [++]([],_) { [] }
fdef [++]([h|t]: [a], l: [a]) {
    [h | t ++ l]
}
'''