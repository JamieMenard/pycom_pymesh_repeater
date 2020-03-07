import os
from machine import SD

def sd_setup():
    try:
        sd = SD()
        os.mount(sd, '/sd')
        print("SD card mounted")
        # try:
        #     os.remove('/sd/www/chat.txt')
        # except:
        #     print('did not delete')
        try:
            f = open('/sd/www/status_log.txt', 'r')
            print("Already a status log")
        except:
            try:
                os.mkdir('/sd/www')
                f = open('/sd/www/status_log.txt', 'w+')
                f.write("Status log:\n")
            except:
                f = open('/sd/www/status_log.txt', 'w+')
                f.write("Status log:\n")
            print("Status Log created")
        f.close()

        try:
            f = open('/sd/www/chat.txt', 'r')
            print("Already a chat log")
        except:
            try:
                os.mkdir('/sd/www')
                f = open('/sd/www/chat.txt', 'w+')
                f.write("Chat log:\n")
            except:
                f = open('/sd/www/chat.txt', 'w+')
                f.write("Chat log:\n")
            print("chat Log created")
        f.close()

    except:
        print("SD card not loaded, chat not saved")

def copy(s, t):
    try:
        f = open(t, 'rb')
    except:
        f = open(t, 'wb')
    s = open(s, "rb")
    while True:
        b = s.read(4096)
        print(b)
        if not b:
           break
        f.write(b)
    f.close()
    s.close()
