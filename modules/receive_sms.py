
import os
import urllib
from multiprocessing import Process
from flask import Flask, request
import csv

app = Flask(__name__)
server = None
outpipe = None

@app.route("/atlas", methods=['POST', 'GET'])

def sms_receive():
    data = request.get_data().decode()
    # parsing the data
    data = data.split('&')
    parsed_data = {}
    for entry in data:
        parsed_data[entry.split('=')[0]] = urllib.parse.unquote_plus(entry.split('=')[1])
    #sending the data
    outpipe.send(parsed_data)

    #logging the message
    new_entry = []
    for key in parsed_data:
        new_entry.append(parsed_data[key])
    with open('logs\\sms_log.csv', 'a', newline='') as f:
        log_writer = csv.writer(f)
        log_writer.writerow(new_entry)

    return 'sms received', 200

def set_webhook_url (url, fallback=False):
    #changing the twilio webhook url
    phone_number = os.environ['ATLAS_PHONE_NUMBER']
    if not fallback:
        print("Setting webhook url")
        os.system(f'twilio phone-numbers:update {phone_number} --sms-url {url}/atlas')
    else:
        print("Setting fallback webhook url")
        os.system(f'twilio phone-numbers:update {phone_number} --sms-fallback-url {url}/atlas')
    return

def start_server(port, _outpipe):
    global outpipe
    outpipe = _outpipe
    server = Process(target=app.run(port=port, debug=False, use_reloader=False))
    server.start()
    print('Flask server terminated')

if __name__ == "__main__":
    print("why did u load this script from main u stupid idiot")

"""
{'ToCountry': 'US', 'ToState': 'MI', 'SmsMessageSid': 'SM653f62452840a174ee986ab28a683000', 'NumMedia': '0', 'ToCity': 'ROMEO', 'FromZip': '96790', 'SmsSid': 'SM653f62452840a174ee986ab28a683000', 'FromState': 'HI', 'SmsStatus': 'received', 'FromCity': 'KULA', 'Body': 'Testing symbols ?+"', 'FromCountry': 'US', 'To': '+15863316265', 'ToZip': '48501', 'NumSegments': '1', 'MessageSid': 'SM653f62452840a174ee986ab28a683000', 'AccountSid': 'ACfc570b9f44c88e9098377fb129ab1278', 'From': '+18087405007', 'ApiVersion': '2010-04-01'}
"""