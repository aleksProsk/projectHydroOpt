>>> class A(object):
...     def set(self,x): self.__x = x
...     def get(self): return self.__x

>>> class B(A):
...     def __init__(self, x): super().set(x)
...     def incr(self): super().set(super().get()+1)
...
>>> b = B(0)
>>> b.get()
0
>>> b.incr()
>>> b.get()
1

