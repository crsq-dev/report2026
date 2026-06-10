""" Fixed point arithmetic module.
    Fixed point value class that provides basic arithmetic operations.
    The value is held as a signed integer, with the number of bits and fraction bits specified.
    """

class SValue:
    """ A signed fixed point value class.
    This class represents a fixed point value with a specified number of bits and fraction bits.
    The value is stored as a signed integer, and the arithmetic operations are performed on this integer.
    The number of bits and fraction bits are used to determine the range and precision of the value.
    The class provides methods for addition, subtraction, multiplication, division, and square root.
    """
    def __init__(self, num_bits: int, num_frac_bits: int, mantissa: int = 0):
        self._num_bits = num_bits
        self._num_frac_bits = num_frac_bits
        hm = (1 << (num_bits - 1)) - 1
        if mantissa < -hm or mantissa >= hm:
            raise ValueError(f"SValue {mantissa} exceeds the range of {num_bits} bits.")
        self._mantissa = int(mantissa)
    
    def __repr__(self):
        return f"SValue(num_bits={self._num_bits}, num_frac_bits={self._num_frac_bits}, mantissa={self._mantissa})"
    
    def float_value(self):
        return self._mantissa / (1 << self._num_frac_bits)
    
    def mantissa(self):
        return self._mantissa
    
    def __add__(self, other) -> 'SValue':
        if not isinstance(other, SValue):
            raise TypeError("Addition is only supported between FixedPointValue instances.")
        if self._num_bits != other._num_bits or self._num_frac_bits != other._num_frac_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits and fraction bits for addition.")
        
        result_mantissa = self._mantissa + other._mantissa
        return SValue(self._num_bits, self._num_frac_bits, result_mantissa)
    
    def __sub__(self, other) -> 'SValue':
        if not isinstance(other, SValue):
            raise TypeError("Subtraction is only supported between FixedPointValue instances.")
        if self._num_bits != other._num_bits or self._num_frac_bits != other._num_frac_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits and fraction bits for subtraction.")
        
        result_mantissa = self._mantissa - other._mantissa
        return SValue(self._num_bits, self._num_frac_bits, result_mantissa)
    
    def abs(self) -> 'UValue':
        return UValue(self._num_bits, self._num_frac_bits, abs(self._mantissa))
    
    def __truediv__(self, other) -> 'SValue':
        if not isinstance(other, SValue):
            raise TypeError("Division is only supported between Value instances.")
        if self._num_bits != other._num_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits for division.")
        
        result_mantissa = self._mantissa // other._mantissa
        result_num_bits = self._num_bits
        result_num_frac_bits = self._num_frac_bits - other._num_frac_bits
        return SValue(result_num_bits, result_num_frac_bits, result_mantissa)
    
    def __mul__(self, other) -> 'SValue':
        if not isinstance(other, SValue):
            raise TypeError("Multiplication is only supported between FixedPointValue instances.")
        
        result_mantissa = self._mantissa * other._mantissa
        result_num_bits = self._num_bits + other._num_bits
        result_num_frac_bits = self._num_frac_bits + other._num_frac_bits
        return SValue(result_num_bits, result_num_frac_bits, result_mantissa)
    
    def square(self) -> 'UValue':
        result_mantissa = self._mantissa * self._mantissa
        result_num_bits = self._num_bits * 2
        result_num_frac_bits = self._num_frac_bits * 2
        return UValue(result_num_bits, result_num_frac_bits, result_mantissa)

    def sqrt(self) -> 'SValue':
        if self._mantissa < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        if self._num_bits % 2 != 0 or self._num_frac_bits % 2 != 0:
            raise ValueError("Number of bits and fraction bits must be even for square root.")
        if self._num_bits < 2:
            raise ValueError("Number of bits must be at least 2 for square root.")
        
        result_mantissa = int(self._mantissa ** 0.5)
        result_num_bits = self._num_bits // 2
        result_num_frac_bits = self._num_frac_bits // 2
        return SValue(result_num_bits, result_num_frac_bits, result_mantissa)

class UValue:
    """ An unsigned fixed point value class.
    This class represents a fixed point value with a specified number of bits and fraction bits.
    The value is stored as an unsigned integer, and the arithmetic operations are performed on this integer.
    The number of bits and fraction bits are used to determine the range and precision of the value.
    The class provides methods for addition, subtraction, multiplication, division, and square root.
    """
    def __init__(self, num_bits: int, num_frac_bits: int, mantissa: int = 0):
        self._num_bits = num_bits
        self._num_frac_bits = num_frac_bits
        maxval = (1 << num_bits) - 1
        if mantissa < 0 or mantissa > maxval:
            raise ValueError(f"Value {mantissa} exceeds the range of {num_bits} bits.")
        self._mantissa = int(mantissa)
    def __repr__(self):
        return f"UValue(num_bits={self._num_bits}, num_frac_bits={self._num_frac_bits}, mantissa={self._mantissa})"
    def float_value(self):
        return self._mantissa / (1 << self._num_frac_bits)
    def mantissa(self):
        return self._mantissa
    def __add__(self, other) -> 'UValue':
        if not isinstance(other, UValue):
            raise TypeError("Addition is only supported between FixedPointValue instances.")
        if self._num_bits != other._num_bits or self._num_frac_bits != other._num_frac_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits and fraction bits for addition.")
        
        result_mantissa = self._mantissa + other._mantissa
        return UValue(self._num_bits, self._num_frac_bits, result_mantissa)
    def __sub__(self, other) -> 'UValue':
        if not isinstance(other, UValue):
            raise TypeError("Subtraction is only supported between FixedPointValue instances.")
        if self._num_bits != other._num_bits or self._num_frac_bits != other._num_frac_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits and fraction bits for subtraction.")
        
        result_mantissa = self._mantissa - other._mantissa
        return UValue(self._num_bits, self._num_frac_bits, result_mantissa)
    def __truediv__(self, other) -> 'UValue':
        if not isinstance(other, UValue):
            raise TypeError("Division is only supported between Value instances.")
        if self._num_bits != other._num_bits:
            raise ValueError("FixedPointValue instances must have the same number of bits for division.")
        
        result_mantissa = self._mantissa // other._mantissa
        result_num_bits = self._num_bits
        result_num_frac_bits = self._num_frac_bits - other._num_frac_bits
        return UValue(result_num_bits, result_num_frac_bits, result_mantissa)
    def __mul__(self, other) -> 'UValue':
        if not isinstance(other, UValue):
            raise TypeError("Multiplication is only supported between FixedPointValue instances.")
        
        result_mantissa = self._mantissa * other._mantissa
        result_num_bits = self._num_bits + other._num_bits
        result_num_frac_bits = self._num_frac_bits + other._num_frac_bits
        return UValue(result_num_bits, result_num_frac_bits, result_mantissa)
    def square(self) -> 'UValue':
        result_mantissa = self._mantissa * self._mantissa
        result_num_bits = self._num_bits * 2
        result_num_frac_bits = self._num_frac_bits * 2
        return UValue(result_num_bits, result_num_frac_bits, result_mantissa)
    def sqrt(self) -> 'UValue':
        if self._mantissa < 0:
            raise ValueError("Cannot compute square root of a negative number.")
        if self._num_bits % 2 != 0 or self._num_frac_bits % 2 != 0:
            raise ValueError("Number of bits and fraction bits must be even for square root.")
        if self._num_bits < 2:
            raise ValueError("Number of bits must be at least 2 for square root.")
        
        result_mantissa = int(self._mantissa ** 0.5)
        result_num_bits = self._num_bits // 2
        result_num_frac_bits = self._num_frac_bits // 2
        return UValue(result_num_bits, result_num_frac_bits, result_mantissa)
    def abs(self) -> 'UValue':
        return UValue(self._num_bits, self._num_frac_bits, abs(self._mantissa))
    def add_msb(self, n = 1) -> 'UValue':
        return UValue(self._num_bits + n, self._num_frac_bits, self._mantissa)
