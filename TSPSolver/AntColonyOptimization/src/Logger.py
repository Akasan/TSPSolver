import colorama
colorama.init(autoreset=True)
from colorama import Fore, Back


def info(mes):
    print(f"[Info] " + Fore.RED + mes)