 goto main
 wb 0
r ww 0 
b ww 5 
e ww 2 
u ww 1
main add y, e
     add x, u 
loop jz y, final
     mult x, b 
     sub y, u 
     goto loop
final mov x, r
halt