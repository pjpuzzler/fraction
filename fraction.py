from __future__ import annotations


class Fraction:
    def __init__(self, numerator: int, denominator: int = 1, reduce: bool = True) -> None:
        if denominator == 0:
            raise ValueError('Denominator cannot be zero')

        if denominator < 0:
            self._numerator = -numerator
            self._denominator = -denominator
        else:
            self._numerator = numerator
            self._denominator = denominator

        self._is_reduced = False
        self._is_reduced = self.reduce(
            True) if reduce else Fraction.are_equal(self, self.reduce(), True)

    def add__(self, other: object) -> Fraction:
        if isinstance(other, Fraction):
            return Fraction.add(self, other)

        if isinstance(other, int):
            return self.add__(Fraction(other))

        return NotImplemented

    def bool__(self) -> bool:
        return self.numerator != 0

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

    def __pow__(self, power: object) -> Fraction:
        if isinstance(power, int):
            return Fraction(self.numerator ** power, self.denominator ** power, False)

        return NotImplemented

    def __repr__(self) -> str:
        return self.fraction_str

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

    def change_denominator(self, denominator: int, inplace: bool = False) -> Fraction | None:
        if not Fraction.is_valid_denominator(self, denominator):
            raise ValueError('Invalid denominator for this fraction')

        # TODO
        if inplace:
            pass
        else:
            pass

    def reduce(self, inplace: bool = False) -> Fraction | bool:
        if inplace:
            if self.is_reduced:
                return True

            from math import gcd
            gcd_ = gcd(self.numerator, self.denominator)

            self._numerator = self.numerator // gcd_
            self._denominator = self.denominator // gcd_
            self._is_reduced = True
            return gcd_ == 1
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
        return Fraction(self.numerator % self.denominator, self.denominator, False)

    @property
    def is_reduced(self) -> bool:
        return self._is_reduced

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
        return Fraction(self.denominator, self.numerator, False)

    @property
    def value(self) -> float:
        return self.numerator / self.denominator

    @property
    def whole_part(self) -> int:
        return self.numerator // self.denominator

    @classmethod
    def from_string(cls, fraction_str: str) -> Fraction:
        ...

    @classmethod
    def from_mixed_number(cls, whole_part: int, fractional_part: Fraction) -> Fraction:
        return Fraction(whole_part * fractional_part.denominator + fractional_part.numerator, fractional_part.denominator)

    @staticmethod
    def add(a: Fraction, b: Fraction, reduce: bool = True) -> Fraction:
        if Fraction.has_common_denominator(a, b):
            return Fraction(a.numerator + b.numerator, a.denominator, reduce)

        return Fraction.add(*Fraction.make_common(a, b), reduce)

    @staticmethod
    def are_equal(a: Fraction, b: Fraction, strict: bool = False) -> bool:
        if strict:
            return a.numerator == b.numerator and a.denominator == b.denominator

        return Fraction.are_equal(*Fraction.make_common(a, b), True)

    @staticmethod
    def divide(a: Fraction, b: Fraction, reduce: bool = True) -> Fraction:
        return Fraction.multiply(a, b.reciprocal, reduce)

    @staticmethod
    def has_common_denominator(a: Fraction, b: Fraction) -> bool:
        return a.denominator == b.denominator

    @staticmethod
    def is_valid_denominator(a: Fraction, denominator: int) -> bool:
        ...  # TODO

    @staticmethod
    def lcd(a: Fraction, b: Fraction) -> int:
        from math import lcm
        return lcm(a.denominator, b.denominator)

    @staticmethod
    def make_common(a: Fraction, b: Fraction) -> tuple[Fraction, Fraction]:
        if Fraction.has_common_denominator(a, b):
            return a, b

        lcd_ = Fraction.lcd(a, b)
        return Fraction(a.numerator * lcd_ // a.denominator, lcd_, False), Fraction(b.numerator * lcd_ // b.denominator, lcd_, False)

    @staticmethod
    def multiply(a: Fraction, b: Fraction, reduce: bool = True) -> Fraction:
        return Fraction(a.numerator * b.numerator, a.denominator * b.denominator, reduce)

    @staticmethod
    def subtract(a: Fraction, b: Fraction, reduce: bool = True) -> Fraction:
        if Fraction.has_common_denominator(a, b):
            return Fraction(a.numerator - b.numerator, a.denominator, reduce)

        return Fraction.subtract(*Fraction.make_common(a, b), reduce)


def main() -> None:
    print(Fraction(1, 2) ** 2)


if __name__ == '__main__':
    main()
