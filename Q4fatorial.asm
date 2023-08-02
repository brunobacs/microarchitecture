goto main
 wb 0
r ww 0
b ww 10
u ww 1

main add x, b
     add y, b 

loop sub y, u 
     jz y final 
     mov y, r 
     mult x, r 
     goto loop

final mov x, r
halt