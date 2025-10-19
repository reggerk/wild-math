# Originally contributed by Renato Gerk.

"""RatPlus, infinite-precision, real numbers. Division by zero included."""

from decimal import Decimal
import math
import numbers
import operator
from RatPlus import RatPlus

__all__ = ['Dihedron']

class Dihedron(numbers.Number):

    __slots__ = ('_u', '_i', '_j', '_k')

    # We're immutable, so use __new__ not __init__
    def __new__(cls, u=RatPlus(0,1), i=None, j=None, k=None, *, _normalize=True):
        """Constructs a Dihedron.
        Takes a string like '3/2' or '1.5', another Dihedron instance, a
        numerator/denominator pair, a float, or a complex.
        Examples
        --------
        >>> Dihedron(10, -8)
        Dihedron(RatPlus(10, 1), RatPlus(-8, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron(Dihedron(1, 7), 5)
        Dihedron(RatPlus(1, 1), RatPlus(12, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron(Dihedron(1, 7), Dihedron(2, 3))
        Dihedron(RatPlus(3, 1), RatPlus(10, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('314')
        Dihedron(RatPlus(314, 1), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('-35/4')
        Dihedron(RatPlus(-35, 4), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('3.1415') # conversion from numeric string
        Dihedron(RatPlus(6283, 2000), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('-47e-2') # string may include a decimal exponent
        Dihedron(RatPlus(-47, 100), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron(1.47)  # direct construction from float (exact conversion)
        Dihedron(RatPlus(6620291452234629, 4503599627370496), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron(2.25)
        Dihedron(RatPlus(9, 4), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron(Decimal('1.47'))
        Dihedron(RatPlus(147, 100), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('3/0')
        Dihedron(RatPlus(1, 0), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('-5/0')
        Dihedron(RatPlus(-1, 0), RatPlus(0, 1), RatPlus(0, 1), RatPlus(0, 1))
        >>> Dihedron('-5-3j')
        Dihedron(RatPlus(-5, 1), RatPlus(-3, 1), RatPlus(0, 1), RatPlus(0, 1))
        """
        self = super(Dihedron, cls).__new__(cls)

        if k is None:
            if j is None:
                if i is None:
                    if type(u) is complex:
                        self._u = RatPlus(u.real)
                        self._i = RatPlus(u.imag)
                        self._j = RatPlus()
                        self._k = RatPlus()
                    else:
                        self._u = RatPlus(u)
                        self._i = RatPlus()
                        self._j = RatPlus()
                        self._k = RatPlus()
                else:
                    self._u = RatPlus(u)
                    self._i = RatPlus(i)
                    self._j = RatPlus()
                    self._k = RatPlus()
            else:
                self._u = RatPlus(u)
                self._i = RatPlus(i)
                self._j = RatPlus(j)
                self._k = RatPlus()
        else:
            self._u = RatPlus(u)
            self._i = RatPlus(i)
            self._j = RatPlus(j)
            self._k = RatPlus(k)

        return self

    @classmethod
    def from_float(cls, f):
        """Converts a finite float to a dihedron number, exactly.
        Beware that Dihedron.from_float(0.3) != Dihedron(RatPlus(3, 10)).
        """
        if isinstance(f, numbers.Integral):
            return cls(f)
        elif not isinstance(f, float):
            raise TypeError("%s.from_float() only takes floats, not %r (%s)" %
                            (cls.__name__, f, type(f).__name__))
        return cls(*f.as_integer_ratio())

    @classmethod
    def from_decimal(cls, dec):
        """Converts a finite Decimal instance to a dihedron number, exactly."""
        from decimal import Decimal
        if isinstance(dec, numbers.Integral):
            dec = Decimal(int(dec))
        elif not isinstance(dec, Decimal):
            raise TypeError(
                "%s.from_decimal() only takes Decimals, not %r (%s)" %
                (cls.__name__, dec, type(dec).__name__))
        return cls(*dec.as_integer_ratio())

    def as_integer_ratio(self):
        """Return the integer ratio as a tuple.
        Return a tuple of two integers, whose ratio is equal to the
        RatPlus and with a positive denominator.
        """
        return (self._u._numerator, self._u._denominator)

    def limit_denominator(self, max_denominator=1000000):
        """Closest Dihedron to self with denominator at most max_denominator.
        >>> Dihedron(RatPlus('3.141592653589793')).limit_denominator(10)
        Dihedron(RatPlus(22, 7))
        >>> Dihedron(RatPlus('3.141592653589793')).limit_denominator(100)
        Dihedron(RatPlus(311, 99))
        >>> Dihedron(RatPlus(4321, 8765)).limit_denominator(10000)
        Dihedron(RatPlus(4321, 8765))
        """

        if max_denominator < 1:
            raise ValueError("max_denominator should be at least 1")

        u = RatPlus(_u).limit_denominator(max_denominator)
        i = RatPlus(_i).limit_denominator(max_denominator)
        j = RatPlus(_j).limit_denominator(max_denominator)
        k = RatPlus(_k).limit_denominator(max_denominator)

        return Dihedron(u, i, j, k)

    @property
    def u(a):
        return a._u

    @property
    def i(a):
        return a._i

    @property
    def j(a):
        return a._j

    @property
    def k(a):
        return a._k

    @property
    def numerator(a):
        return a._u._numerator

    @property
    def denominator(a):
        return a._u._denominator

    def __repr__(self):
        """repr(self)"""
        return '%s(%s, %s, %s, %s)' % (self.__class__.__name__,
                                       self._u, self._i, self._j, self._k)

    def __str__(self):
        """str(self)"""
        return '%s+(%s)i+(%s)j+(%s)k' % (str(self._u), str(self._i), str(self._j), str(self._k))

    def _operator_fallbacks(monomorphic_operator, fallback_operator):

        def forward(a, b):
            if isinstance(b, (int, Dihedron)):
                return monomorphic_operator(a, b)
            elif isinstance(b, float):
                return fallback_operator(float(a), b)
            elif isinstance(b, complex):
                return fallback_operator(complex(a), b)
            else:
                return NotImplemented

        forward.__name__ = '__' + fallback_operator.__name__ + '__'
        forward.__doc__ = monomorphic_operator.__doc__

        def reverse(b, a):
            if isinstance(a, numbers.Rational):
                # Includes ints.
                return monomorphic_operator(a, b)
            elif isinstance(a, numbers.Real):
                return fallback_operator(float(a), float(b))
            elif isinstance(a, numbers.Complex):
                return fallback_operator(complex(a), complex(b))
            else:
                return NotImplemented

        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
        reverse.__doc__ = monomorphic_operator.__doc__

        return forward, reverse

    def _add(a, b):
        """a + b"""
        return Dihedron(a._u + b._u,
                        a._i + b._i,
                        a._j + b._j,
                        a._k + b._k)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(a, b):
        """a - b"""
        return Dihedron(a._u - b._u,
                        a._i - b._i,
                        a._j - b._j,
                        a._k - b._k)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(a, b):
        """a * b"""
        return Dihedron(a._u * b._u - a._i * b._i + a._j * b._j + a._k * b._k,
                        a._u * b._i + a._i * b._u - a._j * b._k + a._k * b._j,
                        a._u * b._j - a._i * b._k + a._j * b._u + a._k * b._i,
                        a._u * b._k + a._i * b._j - a._j * b._i + a._k * b._u)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _div(a, b):
        """a / b"""
        if isinstance(b, (numbers.Rational, float)):
            return Dihedron(a._u / b,
                            a._i / b,
                            a._j / b,
                            a._k / b)
        elif isinstance(b, Dihedron):
            return Dihedron((a * b.conjugate()) / b.quadrance())
        else:
            return NotImplemented

    __truediv__, __rtruediv__ = _operator_fallbacks(_div, operator.truediv)

    def _floordiv(a, b):
        """a // b"""
        if isinstance(b, (numbers.Rational, float)):
            return Dihedron(a._u // b,
                            a._i // b,
                            a._j // b,
                            a._k // b)
        elif isinstance(b, Dihedron):
            return Dihedron((a * b.conjugate()) // b.quadrance())
        else:
            return NotImplemented

    __floordiv__, __rfloordiv__ = _operator_fallbacks(_floordiv, operator.floordiv)

    def _divmod(a, b):
        """(a // b, a % b)"""
        return NotImplemented

    __divmod__, __rdivmod__ = _operator_fallbacks(_divmod, divmod)

    def _mod(a, b):
        """a % b"""
        return NotImplemented

    __mod__, __rmod__ = _operator_fallbacks(_mod, operator.mod)

    def __pow__(a, b):
        """a ** b
        If b is not an integer, the result will be a float or complex
        since roots are generally irrational. If b is an integer, the
        result will be rational.
        """
        if isinstance(b, numbers.Rational):
            if b.denominator == 1:
                power = b.numerator
                if power == 0:
                    return Dihedron(1)
                elif power == 1:
                    return a
                elif power > 1:
                    return a * (a ** (power - 1))
                else:
                    return 1 / (a ** abs(power))
            elif b.denominator == 0:
                if a == 0:
                    return NotImplementedError  # 0 ^ INFINITY
                else:
                    return a * b
            else:
                # A fractional power will generally produce an
                # irrational number.
                return float(a) ** float(b)
        else:
            return float(a) ** b

    def __rpow__(b, a):
        """a ** b"""
        if b._u._denominator == 1 and b._u._numerator >= 0:
            # If a is an int, keep it that way if possible.
            return a ** b._u._numerator

        if isinstance(a, numbers.Rational):
            return RatPlus(a.numerator, a.denominator) ** b._u

        if b._u._denominator == 1:
            return a ** b._u._numerator

        return a ** float(b)

    def __pos__(a):
        """+a: Coerces a subclass instance to Dihedron"""
        return Dihedron(a._u, a._i, a._j, a._k)

    def __neg__(a):
        """-a"""
        return Dihedron(-a._u, -a._i, -a._j, -a._k)

    def __abs__(a):
        """abs(a)"""
        return Dihedron(abs(a._u), abs(a._i), abs(a._j), abs(a._k))

    def __trunc__(a):
        """trunc(a)"""
        return Dihedron(trunc(a._u), trunc(a._i), trunc(a._j), trunc(a._k))

    def __floor__(a):
        """math.floor(a)"""
        return Dihedron(math.floor(a._u), math.floor(a._i), math.floor(a._j), math.floor(a._k))

    def __ceil__(a):
        """math.ceil(a)"""
        # The negations cleverly convince floordiv to return the ceiling.
        return Dihedron(math.ceil(a._u), math.ceil(a._i), math.ceil(a._j), math.ceil(a._k))

    def __round__(self, ndigits=None):
        """round(self, ndigits)
        Rounds half toward even.
        """
        return Dihedron(round(self._u, ndigits), round(self._i, ndigits), round(self._j, ndigits), round(self._k, ndigits))

    def __hash__(self):
        """hash(self)"""
        return hash((self._u, self._i, self._j, self._k))

    def __eq__(a, b):
        """a == b"""
        return a._u == b._u and a._i == b._i and a._j == b._j and a._k == b._k

    def _richcmp(self, other, op):
        """Helper for comparison operators, for internal use only.
        Implement comparison between a Dihedron instance `self`, and
        either another Dihedron instance or a float `other`.  If
        `other` is not a Dihedron instance or a float, return
        NotImplemented. `op` should be one of the six standard
        comparison operators.
        """
        # convert other to a Dihedron instance where reasonable.
        if isinstance(other, numbers.Rational):
            return op(self._u._numerator * other.denominator,
                      self._u._denominator * other.numerator)
        if isinstance(other, float):
            if math.isnan(other) or math.isinf(other):
                return op(0.0, other)
            else:
                return op(self, self.from_float(other))
        else:
            return NotImplemented

    def __lt__(a, b):
        """a < b"""
        return a._richcmp(b, operator.lt)

    def __gt__(a, b):
        """a > b"""
        return a._richcmp(b, operator.gt)

    def __le__(a, b):
        """a <= b"""
        return a._richcmp(b, operator.le)

    def __ge__(a, b):
        """a >= b"""
        return a._richcmp(b, operator.ge)

    def __bool__(a):
        """a != 0"""
        # bpo-39274: Use bool() because (a._numerator != 0) can return an
        # object which is not a bool.
        return bool(a._u) and bool(a._i) and bool(a._j) and bool(a._k)

    # support for pickling, copy, and deepcopy

    def __reduce__(self):
        return (self.__class__, (str(self),))

    def __copy__(self):
        if type(self) == Dihedron:
            return self     # I'm immutable; therefore I am my own clone
        return self.__class__(self._u, self._i, self._j, self._k)

    def __deepcopy__(self, memo):
        if type(self) == Dihedron:
            return self     # My components are also immutable
        return self.__class__(self._u, self._i, self._j, self._k)

    def mediant(a, b):
        """mediant(a, b)"""
        return Dihedron(RatPlus.mediant(a._u, b._u),
                        RatPlus.mediant(a._i, b._i),
                        RatPlus.mediant(a._j, b._j),
                        RatPlus.mediant(a._k, b._k))

    def quadrance(self):
        """quadrance(self)"""
        #"""
        return RatPlus(self._u.quadrance() +
                       self._i.quadrance() -
                       self._j.quadrance() -
                       self._k.quadrance())
        #"""
        #return (self * self.conjugate())._u

    def conjugate(self):
        """conjugate(self)"""
        return Dihedron(self._u, -self._i, -self._j, -self._k)
