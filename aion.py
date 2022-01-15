# venv\Scripts\activate
import os
import logging
import time
import datetime
import atexit
import subprocess
import multiprocessing as mp


# background vars
rcv_port = 5000
start_time = datetime.datetime.now()
background_processes = []
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


    # terminating backroung processes
    for process in background_processes:
        print(f'- Terminating process: {process}')
        process.kill()


def receive_input (raw_input):
    """
    The brain of Aion
    """
    input = ""

    print(f'{colors.fg.lightcyan}Received input: {colors.reset}{raw_input}{colors.reset}')
    logging.info(f'Received input: {raw_input}')

    input = raw_input
    # null input error
    if len(input) == 0:
        print(f'null input')

    input = input.split(' ')
    if len(input) == 1:
        print(f"short input")
    # lowercasing command
    input[0].lower()
    #input[1].lower()

    return True






if __name__ == '__main__':

    # initialization n stuff
    os.system("")
    print(f'{colors.fg.lightgreen}\n\nInitializing Aion{colors.reset}')

    logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', filename='logs\\aion.log', level=logging.INFO)
    logging.info("Starting")

    atexit.register(exit_handler)

    mp_context = mp.get_context('spawn')
    #mp.set_start_method('spawn')

    #TODO remove
    # setting env vars
    os.environ['TELEGRAM_CHAT_ID'] = '1948408284'
    os.environ['AION_BOT_TOKEN'] = "5021950068:AAFeqwg-3dCweyEuOlWvsFYxPIl1sS9nflE"


    # importing my modules
    print('Importing user modules')
    import modules 

    # starting telegram interface
    """print("Connecting to telegram interface")
    tgi_readpipe, tgi_writepipe = mp.Pipe()

    print("Starting telegram interface")
    tgi_process = process_context.Process(target=telegram_interface.start, args=(tgi_readpipe, tgi_writepipe, 1))
    tgi_process.start()
    background_processes.append(tgi_process)
    print("Waiting for telegram interface to load")
    while True:
        if tgi_readpipe.poll(1):
            print(tgi_readpipe.recv())
            break"""
    print('Creating connection for telegram interface')
    tg_rcv_pipe, tg_rcv_child_pipe = mp.Pipe()

    print(f'Starting telegram receiver on port {rcv_port}')
    receive_sms_process = mp_context.Process(target=modules.receive_telegram.start_listener, args=(rcv_port, tg_rcv_child_pipe))
    background_processes.append(receive_sms_process)
    receive_sms_process.start()
    print("Waiting for flask server to go online")
    time.sleep(1.5)


    # starting up the ngrok tunnel
    print('Starting ngrok localhost tunnel')
    ngrok_process = subprocess.Popen(['ngrok', 'http', str(rcv_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
    background_processes.append(ngrok_process)
    ngrok_start_time = datetime.datetime.now()
    time.sleep(2)



    print(f'{colors.fg.lightgreen}Aion online{colors.reset}')
    logging.info("Online")

    while True:
        
        time.sleep(1/60)
        """if tgi_readpipe.poll(1):
            input = tgi_readpipe.recv()
            print(input)
            if input == '/shutdown':
                print('received shutdown from tgi interface')
                exit()"""



"""print(f'Starting sms receiver on port {rcv_port}')
    sms_rcv_readpipe, sms_rcv_writepipe = mp.Pipe()
    receive_sms_process = mp_context.Process(target=receive_sms.start_server, args=(rcv_port, sms_rcv_writepipe))
    background_processes.append(receive_sms_process)
    receive_sms_process.start()
    print("Waiting for flask server to go online")
    time.sleep(2)
    # starting up the ngrok tunnel
    print('Starting ngrok localhost tunnel')
    ngrok_process = subprocess.Popen(['ngrok', 'http', str(rcv_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
    background_processes.append(ngrok_process)
    ngrok_fallback_process = subprocess.Popen(['ngrok', 'http', str(rcv_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
    background_processes.append(ngrok_fallback_process)
    ngrok_start_time = datetime.datetime.now()
    time.sleep(2)

    # getting the ngrok urls
    print('Fetching ngrok public URL')
    url_request = requests.get("http://127.0.0.1:4040/api/tunnels")
    url_request_json = json.loads(url_request.content.decode("utf-8"))
    webhook_url = url_request_json["tunnels"][0]["public_url"]
    print(f'- Public URL: {webhook_url}')
    url_request = requests.get("http://127.0.0.1:4041/api/tunnels")
    url_request_json = json.loads(url_request.content.decode("utf-8"))
    fallback_webhook_url = url_request_json["tunnels"][0]["public_url"]
    print(f'- Fallback public URL: {fallback_webhook_url}')

    # giving url to twilio
    receive_sms.set_webhook_url(webhook_url)
    receive_sms.set_webhook_url(fallback_webhook_url, fallback=True)"""


"""# checking if sms message has been received
        if sms_rcv_readpipe.poll(1):
            receive_input(sms_rcv_readpipe.recv(), 'sms')

        # checking if ngrok needs to be refreshed
        if (datetime.datetime.now() - ngrok_start_time).seconds >= ngrok_refresh_rate * 60:
            print(f"{colors.fg.yellow}Renewing ngrok connection{colors.reset}")
            logging.debug('Renewing ngrok')
            # terminating current ngrok processs
            for process in background_processes:
                if process.pid == ngrok_process.pid:
                    print("Terminating old ngrok session")
                    process.terminate()
                    background_processes.remove(process)
                    break
            for process in background_processes:
                if process.pid == ngrok_fallback_process.pid:
                    print("Terminating old fallback ngrok session")
                    process.terminate()
                    background_processes.remove(process)
                    break

            # starting ngrok
            print('Starting new ngrok tunnel')
            ngrok_process = subprocess.Popen(['ngrok', 'http', str(rcv_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            background_processes.append(ngrok_process)
            ngrok_fallback_process = subprocess.Popen(['ngrok', 'http', str(rcv_port)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            background_processes.append(ngrok_fallback_process)
            ngrok_start_time = datetime.datetime.now()
            time.sleep(2)

            # getting the ngrok urls
            print('Fetching new public URLs')
            url_request = requests.get("http://127.0.0.1:4040/api/tunnels")
            url_request_json = json.loads(url_request.content.decode("utf-8"))
            webhook_url = url_request_json["tunnels"][0]["public_url"]
            print(f'- Public URL: {webhook_url}')
            url_request = requests.get("http://127.0.0.1:4041/api/tunnels")
            url_request_json = json.loads(url_request.content.decode("utf-8"))
            fallback_webhook_url = url_request_json["tunnels"][0]["public_url"]
            print(f'- Fallback public URL: {fallback_webhook_url}')

            # sendin em to twilio
            receive_sms.set_webhook_url(webhook_url)
            receive_sms.set_webhook_url(fallback_webhook_url, fallback=True)
            print(f"{colors.fg.lightgreen}Aion back online{colors.reset}")"""