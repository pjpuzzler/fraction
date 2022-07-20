from __future__ import annotations


class Fraction:
    def __init__(self, numerator: int, denominator: int = 1, reduce: bool = False) -> None:
        if denominator == 0:
            raise ValueError('Denominator cannot be zero')

        if denominator < 0:
            self._numerator = -numerator
            self._denominator = -denominator
        else:
            self._numerator = numerator
            self._denominator = denominator

        if reduce:
            self.reduce(True)

    def __abs__(self) -> Fraction:
        return Fraction(abs(self.numerator), self.denominator)

    def __add__(self, other: object) -> Fraction:
        if isinstance(other, Fraction):
            return Fraction.add(self, other)

        if isinstance(other, int):
            return self.__add__(Fraction(other))

        return NotImplemented

    def __bool__(self) -> bool:
        return self.numerator != 0

    def __ceil__(self) -> int:
        from math import ceil
        return ceil(self.__float__())

    def __divmod__(self, other: object) -> tuple[int, Fraction]:
        if isinstance(other, Fraction) or isinstance(other, int):
            return self.__floordiv__(other), self.__mod__(other)

        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            return Fraction.are_equal(self, other)

        if isinstance(other, int):
            return self.__eq__(Fraction(other))

        if isinstance(other, float):
            return self.__float__() == other

        return NotImplemented

    def __float__(self) -> float:
        return self.value

    def __floor__(self) -> int:
        from math import floor
        return floor(self.__float__())

    def __floordiv__(self, other: object) -> int:
        if isinstance(other, Fraction) or isinstance(other, int):
            return self.__truediv__(other).whole_part

        return NotImplemented

    def __ge__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            return self.__gt__(other) or self.__eq__(other)

        if isinstance(other, int):
            return self.__ge__(Fraction(other))

        if isinstance(other, float):
            return self.__float__() >= other

        return NotImplemented

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            a, b = Fraction.make_common(self, other)
            return a.numerator > b.numerator

        if isinstance(other, int):
            return self.__gt__(Fraction(other))

        if isinstance(other, float):
            return self.__float__() > other

        return NotImplemented

    def __int__(self) -> int:
        return self.whole_part

    def __le__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            return self.__lt__(other) or self.__eq__(other)

        if isinstance(other, int):
            return self.__le__(Fraction(other))

        if isinstance(other, float):
            return self.__float__() <= other

        return NotImplemented

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Fraction):
            a, b = Fraction.make_common(self, other)
            return a.numerator < b.numerator

        if isinstance(other, int):
            return self.__lt__(Fraction(other))

        if isinstance(other, float):
            return self.__float__() < other

        return NotImplemented

    def __mod__(self, other: object) -> Fraction:
        if isinstance(other, Fraction) or isinstance(other, int):
            return self.__sub__(other.__mul__(self.__floordiv__(other)))

        return NotImplemented

    def __mul__(self, other: object) -> Fraction:
        if isinstance(other, Fraction):
            return Fraction.multiply(self, other)

        if isinstance(other, int):
            return self.__mul__(Fraction(other))

        return NotImplemented

    def __neg__(self) -> Fraction:
        return Fraction(-self.numerator, self.denominator)

    def __pos__(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    def __pow__(self, other: object) -> Fraction | float:
        if isinstance(other, int):
            return Fraction(self.numerator ** other, self.denominator ** other)

        if isinstance(other, Fraction):
            return self.value ** other.value

        return NotImplemented

    def __radd__(self, other: object) -> Fraction:
        return self.__add__(other)

    def __rdivmod__(self, other: object) -> tuple[int, Fraction]:
        if isinstance(other, int):
            return divmod(Fraction(other), self)

        return NotImplemented

    def __repr__(self) -> str:
        return self.fraction_str

    def __rfloordiv__(self, other: object) -> int:
        if isinstance(other, int):
            return Fraction(other) // self

        return NotImplemented

    def __rmod__(self, other: object) -> Fraction:
        if isinstance(other, int):
            return Fraction(other) % self

        return NotImplemented

    def __rmul__(self, other: object) -> Fraction:
        return self.__mul__(other)

    def __round__(self, ndigits: int | None = None) -> int:
        return round(self.__float__(), ndigits)

    def __rpow__(self, other: object) -> float:
        if isinstance(other, int):
            return Fraction(other) ** self

        return NotImplemented

    def __rsub__(self, other: object) -> Fraction:
        if isinstance(other, int):
            return Fraction(other) - self

        return NotImplemented

    def __rtruediv__(self, other: object) -> Fraction:
        if isinstance(other, int):
            return Fraction(other) / self

        return NotImplemented

    def __sub__(self, other: object) -> Fraction:
        if isinstance(other, Fraction):
            return Fraction.subtract(self, other)

        if isinstance(other, int):
            return self.__sub__(Fraction(other))

        return NotImplemented

    def __truediv__(self, other: object) -> Fraction:
        if isinstance(other, Fraction):
            return Fraction.divide(self, other)

        if isinstance(other, int):
            return self.__truediv__(Fraction(other))

        return NotImplemented

    def __trunc__(self) -> int:
        return self.whole_part

    def change_denominator(self, denominator: int, inplace: bool = False) -> Fraction | None:
        if not Fraction.is_valid_denominator(self, denominator):
            raise ValueError('Invalid denominator for this fraction')

        if inplace:
            self._numerator = self.numerator * denominator // self.denominator
            self._denominator = denominator
        else:
            return Fraction(self.numerator * denominator // self.denominator, denominator)

    def reduce(self, inplace: bool = False) -> Fraction | None:
        if inplace:
            from math import gcd
            gcd_ = gcd(self.numerator, self.denominator)

            self._numerator = self.numerator // gcd_
            self._denominator = self.denominator // gcd_
        else:
            return Fraction(self.numerator, self.denominator, True)

    @property
    def denominator(self) -> int:
        return self._denominator

    @property
    def fraction_str(self) -> str:
        return f'{self.numerator}' if self.is_whole else f'{self.numerator}/{self.denominator}'

    @property
    def fractional_part(self) -> Fraction:
        return Fraction(self.numerator % self.denominator, self.denominator)

    @property
    def is_reduced(self) -> bool:
        return Fraction.are_equal(self, self.reduce(), True)

    @property
    def is_improper(self) -> bool:
        return self.numerator > self.denominator

    @property
    def is_whole(self) -> bool:
        return self.numerator % self.denominator == 0

    @property
    def mixed_number_str(self) -> str:
        return f'{self.whole_part} {self.fractional_part}' if self.is_improper else f'{self.fractional_part}'

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def reciprocal(self) -> Fraction:
        return Fraction(self.denominator, self.numerator)

    @property
    def value(self) -> float:
        return self.numerator / self.denominator

    @property
    def whole_part(self) -> int:
        if self.numerator < 0:
            return -(-self.numerator // self.denominator)
        return self.numerator // self.denominator

    @classmethod
    def from_string(cls, fraction_str: str, reduce: bool = False) -> Fraction:
        parts = fraction_str.split()
        if len(parts) == 1:
            fraction_parts = parts[0].split('/')
            if len(fraction_parts) != 2:
                raise ValueError('Invalid fraction string')

            try:
                return cls(int(fraction_parts[0]), int(fraction_parts[1]), reduce)
            except ValueError:
                raise ValueError('Invalid fraction string')

        if len(parts) == 2:
            try:
                return cls.from_mixed_number(int(parts[0]), cls.from_string(parts[1]), reduce)
            except ValueError:
                raise ValueError('Invalid fraction string')

        raise ValueError('Invalid fraction string')

    @classmethod
    def from_mixed_number(cls, whole_part: int, fractional_part: Fraction, reduce: bool = False) -> Fraction:
        return Fraction(whole_part * fractional_part.denominator + fractional_part.numerator, fractional_part.denominator, reduce)

    @staticmethod
    def add(a: Fraction, b: Fraction, reduce: bool = False) -> Fraction:
        if Fraction.has_common_denominator(a, b):
            return Fraction(a.numerator + b.numerator, a.denominator, reduce)

        return Fraction.add(*Fraction.make_common(a, b), reduce)

    @staticmethod
    def are_equal(a: Fraction, b: Fraction, strict: bool = False) -> bool:
        if strict:
            return a.numerator == b.numerator and a.denominator == b.denominator

        return Fraction.are_equal(*Fraction.make_common(a, b), True)

    @staticmethod
    def divide(a: Fraction, b: Fraction, reduce: bool = False) -> Fraction:
        return Fraction.multiply(a, b.reciprocal, reduce)

    @staticmethod
    def has_common_denominator(a: Fraction, b: Fraction) -> bool:
        return a.denominator == b.denominator

    @staticmethod
    def is_valid_denominator(a: Fraction, denominator: int) -> bool:
        return a.numerator * denominator % a.denominator == 0

    @staticmethod
    def lcd(a: Fraction, b: Fraction) -> int:
        from math import lcm
        return lcm(a.denominator, b.denominator)

    @staticmethod
    def make_common(a: Fraction, b: Fraction) -> tuple[Fraction, Fraction]:
        if Fraction.has_common_denominator(a, b):
            return a, b

        lcd_ = Fraction.lcd(a, b)
        return Fraction(a.numerator * lcd_ // a.denominator, lcd_), Fraction(b.numerator * lcd_ // b.denominator, lcd_)

    @staticmethod
    def multiply(a: Fraction, b: Fraction, reduce: bool = False) -> Fraction:
        return Fraction(a.numerator * b.numerator, a.denominator * b.denominator, reduce)

    @staticmethod
    def subtract(a: Fraction, b: Fraction, reduce: bool = False) -> Fraction:
        if Fraction.has_common_denominator(a, b):
            return Fraction(a.numerator - b.numerator, a.denominator, reduce)

        return Fraction.subtract(*Fraction.make_common(a, b), reduce)


def main() -> None:
    frac = Fraction.from_string('4/8')
    print(frac.is_reduced)


if __name__ == '__main__':
    main()

# float constructor
