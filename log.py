from colorama import init, Fore, Style
init(autoreset=True)


class log:

    @classmethod
    def general(cls, message: str, end='\n'):
        print(message, end=end)

    @classmethod
    def art(cls, message: str, end='\n'):
        print(f'{Fore.LIGHTGREEN_EX}{message}', end=end)

    @classmethod
    def data(cls, message, end='\n'):
        print(f'{Fore.LIGHTBLACK_EX}{message}', end=end)

    @classmethod
    def success(cls, message: str, end='\n'):
        print(f'{Fore.GREEN}{Style.BRIGHT}RESULT: {message}', end=end)

    @classmethod
    def debug(cls, message: str, end='\n'):
        print(f'{Fore.BLUE}{message}', end=end)

    @classmethod
    def info(cls, message: str, end='\n'):
        print(f'{Fore.CYAN}{message}', end=end)

    @classmethod
    def algo(cls, message: str, end='\n'):
        print(f'{Fore.MAGENTA}{message}', end=end)

    @classmethod
    def warn(cls, message: str, end='\n'):
        print(f'{Fore.YELLOW}WARNING: {message}', end=end)

    @classmethod
    def error(cls, message: str, end='\n'):
        print(f'{Fore.RED}{Style.BRIGHT}ERROR: {message}', end=end)
