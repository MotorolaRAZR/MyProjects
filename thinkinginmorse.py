#!/usr/bin/env python
# Для создания алиаса что бы легче запустить

# Сразу скажу что смотрел очень много в интернете, особенно где найти прописку лампочки на крышке экрана
# А еще спасибо r/thinkpad и stackoverflow и chatgpt в проверке

# Проверка на то есть ли ec_sys в прописке загрузки или нет
import time  # импорт времени для замедления сигналов
import subprocess  # для последующей загрузки модулей из ядра


def is_parameter_in_boot_option(param):
    try:
        # открываем файл cmdline как f
        with open("/proc/cmdline", "r") as f:
            cmdline = f.read()  # делаем переменную cmdline читая файлик f
            return param in cmdline  # возвращаем данные из строки
    # но если файла нету выводим ошибку
    except FileNotFoundError:
        print(
            "Файл /proc/cmdline не найден? Ты точно на линуксе?")
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
        # x8a - статус включенной лампочки который видит линукс
        lampochka.write(b"\x8a")
    else:
        lampochka.write(b"\x0a")  # x0a - наоборот

    lampochka.flush()  # чистим оперативную память


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
    cipher = ""  # создаем пустой список, потом его вернем и отправим на вывод к лампочке
    for letter in text.upper():  # делаем капсы что бы совпало с списком
        if letter != " ":
            # пробел между буквами чтобы легче раскодировать морзе letter - буква из списка, А к примеру
            cipher += MORSE_DICT[letter] + " "
        else:
            # символ пробела взят за деш в списке :shrug:
            cipher += "/"
    return cipher


zamedlitel = 0.15  # чем меньше тем быстрее

VREMYA_DIT = 1  # вроде в секундах
VREMYA_MEJDY_SIGNALAMI = 1
VREMYA_DAH = 3
VREMYA_MEJDY_BYKVAMI = 3
VREMYA_MEJDY_SLOVAMI = 5
VREMYA_TSIKLA = 8

strochka = input("введи на английском то что хочешь вывести на лампочку: ")


# если после ентера нету пробела или деша то сделать задержку между буквами
def zaderjka_mejdy_signalami():
    if strochka_morse[indicator+1] != " " and "/":
        time.sleep(zamedlitel * VREMYA_MEJDY_SIGNALAMI)


if __name__ == "__main__":  # напрямую запускаем
    while True:
        led(False)  # выключаем для последующих сигналов
        strochka_morse = iz_texta_v_morse(strochka)
        # убираем ентер в конце с помощью  [:-1]
        for indicator, char in enumerate(strochka_morse[:-1]):
            # char - символ dit(.) или dat(-)
            if char == ".":
                led(True)  # включаем лампу
                # держим ее включенной с длинной времени для дит
                time.sleep(zamedlitel * VREMYA_DIT)
                led(False)  # выключаем
                print(".", end="")  # выводим что напечатали в консоль

                zaderjka_mejdy_signalami()
            elif char == "-":
                led(True)  # включаем лампу
                # держим ее включенной с длинной времени для дах
                time.sleep(zamedlitel * VREMYA_DAH)
                led(False)  # выключаем
                print("-", end="")  # выводим что напечатали в консоль

                zaderjka_mejdy_signalami()
            elif char == " ":
                # ставим пробел между буквами что-бы по желанию декодировать на сайте
                print(" ", end="")
                if strochka_morse[indicator + 1] != "/" and strochka_morse[indicator - 1] != "/":
                    # ждем перед следующей буквой
                    time.sleep(zamedlitel * VREMYA_MEJDY_BYKVAMI)
            elif char == "/":
                print(" / ", end="")  # ждем до нового слова
                time.sleep(zamedlitel * VREMYA_MEJDY_SLOVAMI)
        # time.sleep(zamedlitel * VREMYA_TSIKLA)
        break
