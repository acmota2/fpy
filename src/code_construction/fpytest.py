'''fpy
# functional

fdef foldl(_,acc,[]) { acc }
fdef foldl(f,acc,[h|t]) {
    foldl(f,f(acc,h),t)
}

fdef foldr(_,acc,[]) { acc }
fdef foldr(f,acc,[h|t]) {
    let { acc2 = foldr(f,acc,t) }
    f(acc2,h)
}

fdef map(_,[]) { [] }
fdef map(f,[h|t]) {
    [ f(h) | map(f,t) ]
}

#fdef map_mal2(_,[]) { [] }
#fdef map_mal2(_,1) { [] }
#fdef map_mal2(f,[h|t]) {
#    [ f(h) | map(f,t) ]
#}
#
#fdef map_mal(_) { [] }
#fdef map_mal(f,[h|t]) {
#    [ f(h) | map_mal(f,t) ]
#}

fdef filter(_,[]) { [] }
fdef filter(f,[h|t]) {
    [?..?] {
        f(h): filter(f,t),
        else: [ h | filter(f,t) ]
    }
}


# se der p ->
fdef filter(_: (a)->bool, []: [a]) -> [a] { [] }
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

fdef [.](f,g,a) {
    (f . g)(a)
}

# lists

fdef [++]([],_) { [] }
fdef [++]([h|t]: [a], l: [a]) {
    [h | t ++ l]
}
'''