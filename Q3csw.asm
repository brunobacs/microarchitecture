 goto main
 wb 0
r ww 0
a ww 59231
b ww 10
c ww 59231
d ww 1

main add x, a
     sub x, c
     jz x, igual
     add y, c
     mov y, a
     sub y, c
     add y, d
     mov y, r
     goto final
igual add y, b
      mov y, c
final halt