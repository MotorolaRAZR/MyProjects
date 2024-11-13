#!/usr/bin/env python
# Проверка на то есть ли ec_sys в прописке загрузки или нет
import time  # импорт времени для замедления сигналов
import subprocess  # для последующей загрузки модулей из ядра
# import multiprocessing as mp
import sys


def is_parameter_in_boot_option(param):
    try:
        # открываем файл cmdline как f
        with open("/proc/cmdline", "r") as f:
            cmdline = f.read()  # делаем переменную cmdline читая файлик f
            return param in cmdline  # возвращаем данные из строки
    # но если файла нету выводим ошибку
    except FileNotFoundError:
        print(
            "Файл /proc/cmdline не найден. Ты точно на линуксе?")
        return False
        quit()  # закрываем программу так как она не на линуксе


# если линукс то запускаем проверку
if is_parameter_in_boot_option("ec_sys"):
    pass  # пропускаем
else:
    print("Пропиши 'ec-sys' как параметр для загрузки в GRUB или rEFInd")
    quit()  # закрываем программу если нету ec_sys как параметра в загрузке

subprocess.call(["modprobe", "-r", "ec_sys"])  # удаляем модуль
# прописываем обратно с правами записи
subprocess.call(["modprobe", "ec_sys",  "write_support=1"])


def led(state):
    # wb - запись в двоичном коде
    lampochka = open("/sys/kernel/debug/ec/ec0/io", "wb")
    lampochka.seek(12)  # читаем 12-ую строчку в файле io
    if state:
        # x8a - binary статус включенной лампочки который видит линукс
        # b в начале - превращает в двоичный код
        lampochka.write(b"\x8a")  # включенный
    else:
        lampochka.write(b"\x0a")  # x0a - наоборот

    if state == "default":
        lampochka.write(b"\x8a")

    lampochka.flush()  # чистим оперативную память и сразу включаем


# тут есть драйвера у линукса поэтому тут легче
def led2(state):
    # открываем файл и просим "дай нам написать пожалуйста"
    lampochka = open("/proc/acpi/ibm/led", "w")
    if state:
        lampochka.write("0 on")  # включен
    else:
        lampochka.write("0 off")  # выключен
    if state == "default":
        lampochka.write("0 on")  # стандарт


"""while True:  # ради интереса сделал выбор в цикле который не закончится пока не будет ввод нуля или единицы
    a = input("0выкл/1вкл: ")
    if a == "0":
        led(False)
        break
    elif a == "1":
        led(True)
        break
    else:
        print("некорекктный вариант ответа")"""

MORSE_DICT = {'A': '.-', 'B': '-...',
              'C': '-.-.', 'D': '-..', 'E': '.',
              'F': '..-.', 'G': '--.', 'H': '....',
              'I': '..', 'J': '.---', 'K': '-.-',
              'L': '.-..', 'M': '--', 'N': '-.',
              'O': '---', 'P': '.--.', 'Q': '--.-',
              'R': '.-.', 'S': '...', 'T': '-',
              'U': '..-', 'V': '...-', 'W': '.--',
              'X': '-..-', 'Y': '-.--', 'Z': '--..',
              '1': '.----', '2': '..---', '3': '...--',
              '4': '....-', '5': '.....', '6': '-....',
              '7': '--...', '8': '---..', '9': '----.',
              '0': '-----', ', ': '--..--', '.': '.-.-.-',
              '?': '..--..', '/': '-..-.', '!': '-.-.--', '-': '-....-',
              '(': '-.--.', ')': '-.--.-'}  # взял с интернета на гитхабе


def iz_texta_v_morse(text):
    cipher = ""  # создаем пустой список, потом его вернем с шифром и отправим на вывод к лампочке
    # цикл включен пока не закончит перевод т.к for x in y
    for letter in text.upper():  # делаем капсы что бы совпало с списком
        if letter != " ":
            # пробел между буквами чтобы затем сделать по нему задержку между буквами
            cipher += MORSE_DICT[letter] + " "
        else:
            # символ пробела взят за деш в списке :shrug:
            cipher += "/"
    return cipher


zamedlitel = 0.15  # чем меньше тем быстрее


# прописи задержек в виде переменных
VREMYA_DIT = 1  # вроде в секундах
VREMYA_MEJDY_SIGNALAMI = 1
VREMYA_DAH = 3
VREMYA_MEJDY_BYKVAMI = 3
VREMYA_MEJDY_SLOVAMI = 5
VREMYA_TSIKLA = 8


def zaderjka_mejdy_signalami():
    if strochka_morse[indicator+1] != [" ", "/"]:
        time.sleep(zamedlitel * VREMYA_MEJDY_SIGNALAMI)


while True:
    strochka = input("введи на английском то что хочешь вывести на лампочку: ")
    led_choice = int(input("выбери лампочку: 1 на крышке/2 кнопка питания: "))

    while True:
        # если ответы правильные выключаем цикл
        if led_choice == 1:
            break
        elif led_choice == 2:
            break
        else:
            print("некорекктный вариант ответа")
    print("код морзе: ", end="")  # очень глупое решение но оно работает
    if __name__ == "__main__":  # напрямую запускаем
        while True:
            led(False)  # выключаем для последующих сигналов
            strochka_morse = iz_texta_v_morse(strochka)
            # убираем или \n или энтер в конце с помощью  [:-1], цикл включен пока полностью не выведет на лампочку
            for indicator, char in enumerate(strochka_morse[:-1]):
                # char - символ dit(.) или dat(-)
                if char == ".":
                    if led_choice == 1:
                        led(True)  # включаем лампу
                    else:
                        led2(True)
                    # держим ее включенной с длинной времени для dit
                    time.sleep(zamedlitel * VREMYA_DIT)
                    if led_choice == 1:
                        led(False)  # выключаем
                    else:
                        led2(False)
                    print(".", end="")  # выводим что напечатали в консоль
                    sys.stdout.flush()  # сразу выводим, stdout - standart output - в нем находится буффер, с помощью flush() мы заставляем питон писать незаконченный буффер
                    zaderjka_mejdy_signalami()
                elif char == "-":
                    if led_choice == "1":
                        led(True)  # включаем лампу
                    else:
                        led2(True)
                    # держим ее включенной с задержкой dah
                    time.sleep(zamedlitel * VREMYA_DAH)
                    if led_choice == "1":
                        led(False)  # выключаем
                    else:
                        led2(False)
                    print("-", end="")  # выводим что напечатали в консоль
                    sys.stdout.flush()
                    zaderjka_mejdy_signalami()
                elif char == " ":
                    # ставим пробел между буквами
                    print(" ", end="")
                    if strochka_morse[indicator + 1] != "/" and strochka_morse[indicator - 1] != "/":
                        # ждем перед следующей буквой
                        time.sleep(zamedlitel * VREMYA_MEJDY_BYKVAMI)
                elif char == "/":
                    print(" / ", end="")  # ждем до нового слова
                    time.sleep(zamedlitel * VREMYA_MEJDY_SLOVAMI)
            # time.sleep(zamedlitel * VREMYA_TSIKLA) нету смысла
            time.sleep(zamedlitel * VREMYA_TSIKLA)
            if led_choice == "1":
                led("default")
            else:
                led2("default")
            break

        # вопрос: продолжать код или нет? если ответ равен списку да д - продолжить если нет не - выключить, а если ничего из этих - неправильный вариант ответа
        # strip() для удаления случайных пробелов и lower() для того что бы сделать списки проверки меньше
        continue_input = input("\nхочешь повторить? д/н: ").strip().lower()
        # не можем использовать if x == y and z т.к оно будет проверять только первую часть(y)
        if continue_input in ["да", "д"]:
            print('passed')
            continue  # повторяем цикл
        elif continue_input in ["нет", "н"]:
            break  # выключаем цикл
        else:
            print("неправильный вариант ответа")
