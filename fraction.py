from __future__ import annotations


class Fraction:
    def __init__(self, numerator: int, denominator: int = 1, reduce: bool = True) -> None:
        if denominator < 0:
            self._numerator = -numerator
            self._denominator = -denominator
        else:
            self._numerator = numerator
            self._denominator = denominator

        if reduce and self.denominator != 0:
            self.reduce(True)

    def __add__(self, __o: object) -> Fraction:
        if isinstance(__o, Fraction):
            return Fraction.add(self, __o)

        if isinstance(__o, int):
            return self.__add__(Fraction(__o))

        return NotImplemented

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Fraction):
            return Fraction.are_equal(self, __o)

        if isinstance(__o, int):
            return self.__eq__(Fraction(__o))

        if isinstance(__o, float):
            return float(self) == __o

        return NotImplemented

    def __float__(self) -> float:
        return self.value

    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, Fraction):
            return self.__gt__(__o) or self.__eq__(__o)

        if isinstance(__o, int):
            return self.__ge__(Fraction(__o))

        if isinstance(__o, float):
            return float(self) >= __o

        return NotImplemented

    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, Fraction):
            common_a, common_b = Fraction.make_common(self, __o)
            return common_a.numerator > common_b.numerator

        if isinstance(__o, int):
            return self.__gt__(Fraction(__o))

        if isinstance(__o, float):
            return float(self) > __o

        return NotImplemented

    def __int__(self) -> int:
        if self.is_undefined:
            raise ValueError(
                'Cannot convert an undefined fraction to an integer')

        return self.numerator // self.denominator

    def __le__(self, __o: object) -> bool:
        if isinstance(__o, Fraction):
            return self.__lt__(__o) or self.__eq__(__o)

        if isinstance(__o, int):
            return self.__le__(Fraction(__o))

        if isinstance(__o, float):
            return float(self) <= __o

        return NotImplemented

    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, Fraction):
            common_a, common_b = Fraction.make_common(self, __o)
            return common_a.numerator < common_b.numerator

        if isinstance(__o, int):
            return self.__lt__(Fraction(__o))

        if isinstance(__o, float):
            return float(self) < __o

        return NotImplemented

    def __mul__(self, __o: object) -> Fraction:
        if isinstance(__o, Fraction):
            return Fraction.multiply(self, __o)

        if isinstance(__o, int):
            return self.__mul__(Fraction(__o))

        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.numerator}' if self.denominator == 1 else f'{self.numerator}/{self.denominator}'

    def __sub__(self, __o: object) -> Fraction:
        if isinstance(__o, Fraction):
            return Fraction.subtract(self, __o)

        if isinstance(__o, int):
            return self.__sub__(Fraction(__o))

        return NotImplemented

    def __truediv__(self, __o: object) -> Fraction:
        if isinstance(__o, Fraction):
            return Fraction.divide(self, __o)

        if isinstance(__o, int):
            return self.__truediv__(Fraction(__o))

        return NotImplemented

    def change_denominator(self, denominator: int, inplace: bool = False) -> Fraction | None:
        if not Fraction.is_valid_denominator(self, denominator):
            raise ValueError('Invalid denominator for this fraction')

        # TODO
        if inplace:
            pass
        else:
            pass

    def reduce(self, inplace: bool = False) -> Fraction | None:
        if inplace:
            from math import gcd
            gcd_ = gcd(self.numerator, self.denominator)

            self._numerator = self.numerator // gcd_
            self._denominator = self.denominator // gcd_
        else:
            return Fraction(self.numerator, self.denominator, True)

    @property
    def numerator(self) -> int:
        return self._numerator

    @property
    def denominator(self) -> int:
        return self._denominator

    @property
    def is_reduced(self) -> bool:
        return Fraction.are_equal(self, self.reduce(), True)

    @property
    def is_improper(self) -> bool:
        return self.numerator > self.denominator

    @property
    def is_undefined(self) -> bool:
        return self.denominator == 0

    @property
    def is_whole(self) -> bool:
        return self.reduce().denominator == 1

    @property
    def reciprocal(self) -> Fraction:
        return Fraction(self.denominator, self.numerator, False)

    @property
    def value(self) -> float:
        return float('nan') if self.is_undefined else self.numerator / self.denominator

    @staticmethod
    def add(__a: Fraction, __b: Fraction, reduce: bool = True) -> Fraction:
        if Fraction.has_common_denominator(__a, __b):
            return Fraction(__a.numerator + __b.numerator, __a.denominator, reduce)

        return Fraction.add(*Fraction.make_common(__a, __b), reduce)

    @staticmethod
    def are_equal(__a: Fraction, __b: Fraction, strict: bool = False) -> bool:
        if strict:
            return __a.numerator == __b.numerator and __a.denominator == __b.denominator and not __a.is_undefined

        return Fraction.are_equal(*Fraction.make_common(__a, __b), True)

    @staticmethod
    def divide(__a: Fraction, __b: Fraction, reduce: bool = True) -> Fraction:
        return Fraction.multiply(__a, __b.reciprocal, reduce)

    @staticmethod
    def has_common_denominator(__a: Fraction, __b: Fraction) -> bool:
        return __a.denominator == __b.denominator and __a.denominator != 0

    @staticmethod
    def is_valid_denominator(__a: Fraction, denominator: int) -> bool:
        ...  # TODO

    @staticmethod
    def lcd(__a: Fraction, __b: Fraction) -> int:
        from math import lcm
        return lcm(__a.denominator, __b.denominator)

    @staticmethod
    def make_common(__a: Fraction, __b: Fraction) -> tuple[Fraction, Fraction]:
        if Fraction.has_common_denominator(__a, __b):
            return __a, __b

        lcd_ = Fraction.lcd(__a, __b)
        return Fraction(__a.numerator * lcd_ // __a.denominator, lcd_, False), Fraction(__b.numerator * lcd_ // __b.denominator, lcd_, False)

    @staticmethod
    def multiply(__a: Fraction, __b: Fraction, reduce: bool = True) -> Fraction:
        return Fraction(__a.numerator * __b.numerator, __a.denominator * __b.denominator, reduce)

    @staticmethod
    def subtract(__a: Fraction, __b: Fraction, reduce: bool = True) -> Fraction:
        if Fraction.has_common_denominator(__a, __b):
            return Fraction(__a.numerator - __b.numerator, __a.denominator, reduce)

        return Fraction.subtract(*Fraction.make_common(__a, __b), reduce)


def main() -> None:
    frac = Fraction(1, 2)
    print(frac <= Fraction(1, 3))


if __name__ == '__main__':
    main()
