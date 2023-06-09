'''fpy
# functional

fdef curry(f,a,b) {
    f((a,b))
}

fdef uncurry(f,(a,b)) {
    f(a,b)
}

# Da erro
# fdef bla(n: int) {
#     n + 1.1
# }

fdef normalmap(_,[]) { [] }
fdef normalmap(f,[h|t]) {
        [ f(h) | f `normalmap` t ]
}

fdef [<>](_,[]) { [] }
fdef [<>](f,[h|t]) {
        [ f(h) | f <> t ]
}

fdef inSort([]) { [] }
fdef inSort([x]) { [x] }
fdef inSort([h|t]) {
  insertOrd(h, inSort(t))
}

fdef insertOrd(x, []) { [x] }
fdef insertOrd(x, [h|t]) {
  [?..?] {
    h < x: [h | insertOrd(x, t)],
    else: [h | [x | t] ]
  }
}

'''