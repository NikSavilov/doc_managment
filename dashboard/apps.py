import time
from threading import Thread

from django.apps import AppConfig


#
#
# class PollingThread(Thread):
#     def run(self):
#         while True:
#             print("Im thread")
#             time.sleep(3)
#             s = get_service()


class DashboardConfig(AppConfig):
    name = 'dashboard'

    # def ready(self):
    #     PollingThread().start()
