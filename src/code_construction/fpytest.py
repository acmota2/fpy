'''fpy
# functional

fdef curry(f,a,b) {
    f((a,b))
}

fdef uncurry(f,(a,b)) {
    f(a,b)
}


let bla2 = 73

fdef bla(cenas) {
    let {
        x = fdef([_|t]) { foldr([+], 0, t) }
    }
    bla2 + x([1,2,3]) * cenas
}

fdef normalmap(_,[]) { [] }
fdef normalmap(f,[h|t]) {
        [ f(h) | f `normalmap` t ]
}

fdef [<>](_,[]) { [] }
fdef [<>](f,[h|t]) {
        [ f(h) | f <> t ]
}

'''