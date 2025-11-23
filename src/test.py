

class A:
    
    a = 10
    
    
a1 = A()
a2 = A()


a1.__class__.a = 11


print(a2.a)
    
dir(a1)
