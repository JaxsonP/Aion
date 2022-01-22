# venv\Scripts\activate
import os
import logging
import time
import datetime
import atexit
import pkgutil
import multiprocessing as mp

# tokens and ids and stuff
import constants


# background vars
start_time = datetime.datetime.now()
background_processes = []
active_modules = {}
pid = os.getpid()

class colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'





def exit_handler():
    # on exit do this stuff
    print(f'{colors.fg.lightgreen}Exiting Aion{colors.reset}')
    logging.info("Exiting")
    modules.telegram_interface.send_message("Aion shutting down...")


    # terminating backroung processes
    print('Terminating background processes...')
    for process in background_processes:
        print(f'- Terminating process: {process}')
        process.kill()


def receive_input (raw_input):
    """
    The brain of Aion
    """
    global active_modules

    print(f'{colors.fg.lightcyan}Received input: {colors.reset}{raw_input}{colors.reset}')
    logging.info(f'Received input: {raw_input}')


    # null input error
    if len(raw_input) == 0:
        print(f'{colors.fg.red}Received null input{colors.reset}')
        return False

    # commands
    if raw_input == '/help':
        modules.telegram_interface.send_message("Available modules:")
        msg = ""
        for m in active_modules:
            msg += f'\n- {m}'
        modules.telegram_interface.send_message(msg)
        return True
    elif raw_input == '/shutdown':
        print(f'{colors.fg.red}Received telegram shutdown command\n{colors.reset}Starting shutdown...')
        exit()

    input = raw_input.split(' ')

    # parsing the module
    input[0] = input[0].lower()
    module = None
    if input[0].replace('_', '') in [x.replace('_', '') for x in active_modules]:
        print(f'Determined module: {getattr(modules, input[0])}')
        module = getattr(modules, input[0])
    else: 
        
        # invalid module
        print(f"{colors.fg.red}Could not locate module:{colors.reset} {input[0]}")
        modules.telegram_interface.send_message(f"Could not locate module: {input[0]}")
        modules.telegram_interface.send_message(f"Use the /help command to get a list of modules")
        return False

    # asking about functions from a module
    if len(input) == 1 or input[1].lower() == 'help':
        modules.telegram_interface.send_message(f"Available functions in module \'{input[0]}\':")
        msg = ""
        for x in dir(module):
            if callable(getattr(module, x)):
                msg += f'- {x}\n'
        modules.telegram_interface.send_message(msg)
        return True

    return True






if __name__ == '__main__':

    # initialization n stuff
    os.system("")
    print(f'{colors.fg.lightgreen}\n\nInitializing Aion{colors.reset}')

    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', filename='logs\\aion.log', level=logging.INFO)
    logging.info("Starting")

    atexit.register(exit_handler)

    mp_context = mp.get_context('spawn')

    #TODO remove
    # setting env vars
    os.environ['TELEGRAM_CHAT_ID'] = constants.telegram_chat_id
    os.environ['AION_BOT_TOKEN'] = constants.bot_token


    # importing my modules
    print('Importing user modules')
    import modules

    # starting telegram interface
    print('Creating connection for telegram interface')
    tg_rcv_pipe, tg_rcv_child_pipe = mp.Pipe()

    print(f'Starting telegram receiver')
    telegram_interface_process = mp_context.Process(target=modules.telegram_interface.start, args=(tg_rcv_child_pipe,))
    background_processes.append(telegram_interface_process)
    telegram_interface_process.start()
    time.sleep(1)

    #parsing active modules
    print(f"Gathering active modules")
    modules_path = os.path.dirname(modules.__file__)
    for x in pkgutil.iter_modules([modules_path]):
        active_modules[x[1]] = [x[0]]
    print(f"Found {len(active_modules)} active modules")
    print(active_modules.keys())

    print(f'{colors.fg.lightgreen}Aion online{colors.reset}')
    logging.info("Online")
    modules.telegram_interface.send_message('Aion online')

    try:
        while True:
        
            if tg_rcv_pipe.poll(1):
                receive_input(tg_rcv_pipe.recv())
    except KeyboardInterrupt:
        print(f'{colors.fg.red}Received KeyboardInterrupt\n{colors.reset}Starting shutdown...')
        exit()