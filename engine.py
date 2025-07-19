from math import log, exp

class Value:

    def __init__(self, data, _children = ()):
        self.data = data
        self._prev = set(_children)

        self.grad = 0
        self._backward = lambda : None

    def __repr__(self):
        return f"data = {self.data}"

    # Operation definitions
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __neg__(self):
        out = Value(-self.data, (self,))
        def _backward():
            self.grad += -out.grad
        out._backward = _backward
        return out

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data**other.data, (self, other))
        def _backward():
            self.grad += other.data * self.data ** (other.data - 1) * out.grad
            other.grad += self.data ** other.data * log(other.data) * out.grad
        out._backward = _backward
        return out

    def __truediv__(self, other):
        return self * (other ** -1)

    def exp(self):
        out = Value(exp(self.data), (self,))
        def _backward():
            self.grad += out * out.grad
        out._backward = _backward
        return out

    def log(self):
        out = Value(log(self.data), (self,))
        def _backward():
            self.grad += (self.data ** -1) * out.grad
        out._backward = _backward
        return out

    def __rmul__(self, other):
        return self * other

    # backward method
    def backward(self):
        nodes = []  # Will contain each node in topological order
        visited = set()
        def build(v):
            nodes.append(v)
            if v not in visited:
                visited.add(v)
                for u in v._prev: build(u)
        build(self)
        for v in nodes:
            v._grad = 0.0

        for v in nodes:
            v._backward()
