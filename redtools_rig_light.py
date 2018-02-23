# -*- coding: utf-8 -*-

import socket
import json
import datetime
import time
import telepot
from telepot.loop import MessageLoop

#-- CONFIG -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

token = '1234567890:FHhfFHdjJFhfJFhdJFnvJFnvJFDHDSSADS'  # Key of telegram bot
telegramID = 1234567                                     # ID of your telegram

miner_ip = '127.0.0.1'
miner_port = 3333

#-- END CONFIG -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

TelegramBot = telepot.Bot(token)

def handle(msg):
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        global ALERTSTATUS
        global NOTIFYSTATUS 
        global SECURENOTIFYSTATUS

        if content_type != 'text':
            return

        chat_id = msg['chat']['id']

        if chat_id == telegramID:
            commandfull = msg['text'].strip().lower()
            command = commandfull.split('@')[0]

            if command == '/status':
                gpu_temp, gpu_fans, hashrate_total, hashrate, accepted_shares, invalid_shares, miner_uptime = get_data_req()

            #-- Uptime -------
                miner_uptime_str = 'Uptime: ' + str(datetime.timedelta(seconds=(int(miner_uptime)*60)))
            #-- Total HR -------
                hashrate_total_str = 'Hashrate_total: ' + str("{:,.2f}".format(hashrate_total / float(1000))) + ' Mh/s'
            #-- GPU HR -------
                hashrate_str = 'GPU Mh/s: ' + str("{:,.2f}".format(int(hashrate[0]) / float(1000)))
                for i in range(1, len(hashrate)):
                    hashrate_str +=  ', ' + str("{:,.2f}".format(int(hashrate[i]) / float(1000)))
            #-- GPU Temp -------
                gpu_temp_str = 'GPU temp: ' + str(gpu_temp[0])
                for i in range(1, len(gpu_temp)):
                    gpu_temp_str +=  'C, ' + str(gpu_temp[i])
                gpu_temp_str +=  'C'
            #-- GPU Fans -------
                gpu_fans_str = 'GPU fans: ' + str(gpu_fans[0])
                for i in range(1, len(gpu_fans)):
                    gpu_fans_str +=  '%, ' + str(gpu_fans[i])
                gpu_fans_str +=  '%'
            #-- Shares-------
                shares_str = 'Accepted/invalid: ' + str(accepted_shares) + ' / ' + str(invalid_shares)
            #-- Message -------
                report_msg = miner_uptime_str + '\n' + hashrate_total_str  + '\n' + hashrate_str + '\n' + gpu_temp_str + '\n' + gpu_fans_str + '\n' + shares_st
r
                
                TelegramBot.sendMessage(chat_id, report_msg)
    except Exception as e:
        return False

def get_data(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
    try:
        sock.connect(server_address)
    except Exception as e:
        return []
    request = '{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\"}'
    request = request.encode()
    try:
        sock.sendall(request)
    except Exception as e:
        return []
    try:
        data = sock.recv(512)
    except Exception as e:
        return []
    message = json.loads(data)
    sock.close()
    return message

def get_data_req():
    hashrate_total = []
    hashrate = []
    accepted_shares = []
    invalid_shares = []
    miner_uptime = []

    data = get_data(miner_ip, miner_port)

    try:
        all = data['result'][6].split(';')
        gpu_temp = all[::2]
        gpu_fans = all[1::2]
        hashrate_total = int(data['result'][2].split(';')[0])
        hashrate = data['result'][3].split(';')
        accepted_shares = int(data['result'][2].split(';')[1])
        invalid_shares = int(data['result'][2].split(';')[2])
        miner_uptime = data['result'][1]

        return gpu_temp, gpu_fans, hashrate_total, hashrate, accepted_shares, invalid_shares, miner_uptime

    except Exception as e:
        return []

def main():
    MessageLoop(TelegramBot, handle).run_as_thread()
    while True:
        time.sleep(30)

if __name__ == '__main__':
    main()
