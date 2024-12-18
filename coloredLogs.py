
from termcolor import colored, cprint



def printWithColor(message, signal):

    if signal == "green":
        print(colored(message, 'white', 'on_green', attrs=['bold']))


    elif signal == "yellow":
        print(colored(message, 'black', 'on_light_yellow',  attrs=['bold']))

    elif signal == "red":
        print(colored(message,'white', 'on_red', attrs=['bold']))
        
    elif signal == "info":
        print(colored(message,'black', 'on_light_cyan', attrs=['bold']))

    elif signal == "steps":
        print(colored(message,'black', 'on_white'))
    


# Tests 
# text = colored('Hello, World!', 'red', attrs=['reverse', 'blink', 'bold'])
# print(text)
# cprint('Hello, World!', 'white', 'on_red')

# print(colored('Hello', 'red'), colored('Medium', 'black', 'on_light_yellow'), colored('world', 'green'))
