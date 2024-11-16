to_code = int(input("type something u wanna convert: "))
to_code2 = input("type something u wanna convert to decimal: ")

def bin_to_decimal(num):
    binary_number = ""
    while num > 0:
        remnant = num % 2
        binary_number = str(remnant) + binary_number
        num = num // 2
    return binary_number

print(bin_to_decimal(to_code))

def decimal_to_bin(num):
    decimal_number = 0
    for numbers in num:
        decimal_number = decimal_number*2 + int(numbers)
    return decimal_number

print(decimal_to_bin(to_code2))