while True:
    try:
        to_code = int(input("type a number: "))
        break
    except ValueError:
        print("not a number u idiot!!!!!!")

while True:
    to_code2 = input("type a binary number: ")
    if to_code2.isdigit():
        break
    else:
        print("not a number u idiot!!!!!!")

# self-explanatory, im lazy to explain this
def decimal_to_bin(num):
    binary_number = ""
    while num > 0:
        remnant = num % 2
        binary_number = str(remnant) + binary_number
        num = num // 2
    return binary_number or "0"


def bin_to_decimal(num):
    decimal_number = 0
    # decimal number equals the addition of numbers multplied by 2 with power index from the right to left
    # enumerate defines the index so its easier for me
    for index, digits in enumerate(reversed(num)):
        decimal_number += int(digits) * (2**index)
    return decimal_number


# another great example of converting bin to decimal would be
def bin_to_decimal2(num):
    decimal_number = 0
    for digits in num:
        decimal_number = decimal_number*2 + int(digits)
    return decimal_number
# this method uses the another method of converting by shifting the numbers to left in binary terms


print("binary number:", decimal_to_bin(to_code))
print("decimal number:", bin_to_decimal(to_code2), bin_to_decimal2(to_code2))
