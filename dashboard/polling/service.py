import subprocess
import time
import traceback
from datetime import datetime

import arrow
import ntplib

from .bot import Bot
from .dao import DAO
from .singleton import Singleton


class Service(metaclass=Singleton):
    def __init__(self, system_settings):
        try:
            self.sync_time()
            self.settings = system_settings
            self.dao = DAO(self, system_settings)
            self.bot = Bot(self)
            self.report("Service had been initialized successfully.")

        except:
            self.report("Error 110", traceback.format_exc())

    def sync_time(self):
        for i in range(3):
            try:
                client = ntplib.NTPClient()
                response = client.request('pool.ntp.org')
                online_time = arrow.get(response.tx_time)
                local = online_time.to('Europe/Moscow')
                return1 = subprocess.Popen('date ' + local.format('DD-MM-YY'), shell=True).wait()
                return2 = subprocess.Popen('time ' + local.format('HH:mm:ss'), shell=True).wait()
                if return1 != 0 or return2 != 0:
                    self.report('Not enough permissions to synchronize time.')
                else:
                    self.report('Time synchronization was successful.')
                break
            except ntplib.NTPException:
                self.report("Time synchronization error.")
                time.sleep(i * i + 1)

    def report(self, message, trace=None, module="/service", info=False):
        try:
            fmt = '%Y-%m-%d %H:%M:%S'
            time_ = datetime.now().strftime(fmt)
            message = time_ + " : " + str(module) + " : " + str(message)
            with open('service_log.txt', 'a', encoding='utf-8') as f:
                if info:
                    print(message)
                else:
                    print(message + '\n', file=f)
                    print(message)
                if trace:
                    try:
                        print(time_ + ":\n" + str(trace) + '\n', file=f)
                        print(time_ + ":\n" + str(trace))
                    except:
                        print("Error 107.\n" + traceback.format_exc())
                        return
                    try:
                        print(time_ + ":\n" + str(self.dao) + "\n", file=f)
                        print(time_ + ":\n" + str(self.dao))
                    except:
                        print(time_ + "Can't detailize.\n" + traceback.format_exc(), file=f)
                        print(time_ + "Can't detailize.\n" + traceback.format_exc())
        except:
            print("Error 108. Report is impossible.", traceback.format_exc())

    def add_event(self, event):
        self.bot.event_queue.append(event)
