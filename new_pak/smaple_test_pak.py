from . import sample_pak


def main():
    num1 = 10
    num2 = 5

    print("Addition:", sample_pak.add(num1, num2))
    print("Subtraction:", sample_pak.subtract(num1, num2))
    print("Multiplication:", sample_pak.multiply(num1, num2))
    print("Division:", sample_pak.divide(num1, num2))