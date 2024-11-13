import colorama

FC_BLUE = colorama.Fore.LIGHTBLUE_EX
FC_RED = colorama.Fore.RED

FC_RESET = colorama.Fore.RESET

def logInfo(text):
    print(FC_BLUE, f"[INFO]: {text}", FC_RESET)

def logError(text):
    print(FC_RED, f"[ERROR]: {text}", FC_RESET)