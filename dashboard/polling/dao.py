import os
import threading
import time
import traceback
from json import dumps

import requests

from dashboard.polling.message import Message
from doc_managment.settings import BASE_DIR


class VK:
    def __init__(self, social_source, params):
        self.return_url = params['return_url']
        self.group_id = params['group_id']
        self.token = params['token']
        self.url = params['url']
        self.id = params['id']
        self.data = {'key': '', 'server': '', 'ts': 1}
        self.social_source = social_source
        self.start_polling()

    def report(self, message, trace=None, module="", info=False):
        self.social_source.report(message, trace=trace, module='/vk' + module, info=info)

    def send_text(self, user_id, message, buttons=None):
        resp = requests.get('https://api.vk.com/method/messages.send', params={
            'access_token': self.token,
            'peer_id': user_id,
            'message': message,
            'keyboard': buttons,
            'v': '5.80'}
                            )
        # TODO : add buttons to the text, only in VK
        if resp.json() and "error" in resp.json().keys():
            self.report("Error of sending a message, json:", resp.json())

    # TODO: check if sent's been successful

    def get_data(self):
        try:
            self.data = requests.get('https://api.vk.com/method/groups.getLongPollServer',
                                     params={'access_token': self.token,
                                             'v': 5.126,
                                             'group_id': self.group_id}).json()['response']
            try:
                with open(self._get_ts_path(), "r", encoding="utf-8") as f:
                    self.data['ts'] = int(f.readline())
            except OSError:
                self.report("Error 109. Reading ts.")
            # If reading was not successful nothing changes.
            if 'key' in self.data.keys() and 'server' in self.data.keys() and 'ts' in self.data.keys():
                self.report("Got data for polling. Ts: {}".format(self.data['ts']))
            else:
                self.report('Wrong data format: ', self.data)
                self.get_data()
        except:
            self.report('Error of getting data.', traceback.format_exc())

    def polling(self):
        self.report("Waiting of service initialization.")
        time.sleep(5)
        self.report("Vk polling started.")
        while True:
            try:
                response = requests.get(
                    '{server}?act=a_check&key={key}&ts={ts}&wait={wait}&mode=2&version=2'.format(
                        server=self.data['server'],
                        key=self.data['key'],
                        ts=self.data['ts'],
                        wait=2), timeout=3).json()
                self.data['ts'] = response['ts']
                with open(self._get_ts_path(), "w", encoding="utf-8") as f:
                    f.write(str(response['ts']))
                self.report('ts: ' + dumps(response['ts']) + ', событий: ' + str(len(response['updates'])), info=True)
                self.handle_response(response)
            except requests.exceptions.ReadTimeout:
                self.report('Lost internet connection.')
                time.sleep(5)
            except KeyError:
                self.report('Updating data.')
                self.get_data()
            except OSError:
                self.report('TS file was not found.' + traceback.format_exc())
                time.sleep(5)
            except:
                self.report('TS file was not found.', traceback.format_exc())

    def _get_ts_path(self):
        return os.path.join(BASE_DIR, "vk-ts{}.txt".format(self.id))

    def find_attachments(self, message_):
        def search(message):
            if 'doc' in message:
                yield message['doc']
            for k in message:
                if isinstance(message[k], list):
                    for i in message[k]:
                        for j in search(i):
                            yield j

        files = list(search(message_))
        final_list = []
        for file in files:
            final_file = {}
            try:
                final_file.update({"id": str(file["id"]) + "_" + str(file["owner_id"])})
                final_file.update({"name": file["title"]})
                final_file.update({"link": file["url"]})
                final_file.update({"size": file["size"]})
                final_file.update({"ext": file["ext"]})
                final_list.append(final_file)
            except KeyError:
                self.report("Key error.", traceback.format_exc())
        return final_list

    def api(self, method, params):
        try:
            params['v'] = '5.126'
            params['access_token'] = self.token
            return requests.get('https://api.vk.com/method/{m}'.format(m=method), params=params).json()
        except:
            self.report("Ошибка API запроса: " + str(params), traceback.format_exc())
            return None

    def handle_response(self, response):
        updates = response['updates']
        if updates:
            print(updates)
            for element in updates:
                type_ = element.get("type")
                if type_ == "message_new":
                    try:
                        self.report(str(element))
                        message_by_id = element.get("object").get("message")
                        user_by_id = self.api('users.get',
                                              {'user_ids': message_by_id["from_id"], 'name_case': 'noms'})['response']
                        first_name = user_by_id[0]['first_name']
                        chat_obj = self.api('messages.getConversationsById',
                                            {"peer_ids": message_by_id["peer_id"],
                                             "extended": 1,
                                             "fields": "name,photo_50"})['response']["items"][0]

                        attachments = self.find_attachments(message_by_id)
                        message = {
                            "source": "VK",
                            "message_id": message_by_id["id"],
                            "user_id": message_by_id["from_id"],
                            "chat_id": message_by_id["peer_id"],
                            "chat_obj": chat_obj,
                            'name': first_name,
                            "unix_time": message_by_id["date"],
                            "text": message_by_id["text"].lower(),
                            "attachments": attachments,
                            "obj": message_by_id
                        }
                        message = Message(message)
                        self.social_source.handle_new_message(message)
                    except:
                        self.report('Error of handling update.', traceback.format_exc())

    def start_polling(self):
        try:
            self.get_data()
            self.polling_thread = threading.Thread(target=self.polling)
            self.polling_thread.start()
        except:
            self.report("Restarting vk polling.")
            self.start_polling()

    def make_buttons(self, buttons):
        # Returns string in JSON for VK API
        keyboard = {"one_time": True,
                    'buttons': [
                        [
                            {"action": {"type": "text",
                                        "label": "{button}".format(button=but_['text'])
                                        },
                             "color": "{default}".format(default=but_['color'])
                             }
                            for but_ in str_
                        ]
                        for str_ in buttons]}
        keyboard = dumps(keyboard, ensure_ascii=False)
        return keyboard


class TG:
    def __init__(self, social_source, params):
        self.return_url = params['return_url']
        self.token = params['token']
        self.url = params['url']
        self.new_offset = None
        self.social_source = social_source
        self.start_polling()

    def report(self, message, trace=None, module="", info=False):
        self.social_source.report(message, trace=trace, module='/tg' + module, info=info)

    def get_updates(self, offset=None, timeout=2):
        method = '/getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.url + self.token + method, params)
        result_json = resp.json().get('result', None)
        if result_json is None:
            print(resp, resp.content)
            return {}
        try:
            self.report("ts: " + (str(offset) if offset else "current") + ", событий: " + str(len(result_json)))
        except:
            self.report("Error of reporting in get updates.", traceback.format_exc())
        return result_json

    def api(self, method, params):
        try:
            resp = requests.get(self.url + self.token + '/' + method, params)
            result_json = resp.json()['result']
            return result_json
        except:
            self.report("API failed: " + str(resp.json()) + '\n' + str(params), traceback.format_exc())
            raise KeyError

    def ansOnCallback(self, callback_id):
        params = {'callback_query_id': callback_id}
        return self.api("answerCallbackQuery", params)

    def make_buttons(self, buttons):
        keyboard = {'inline_keyboard': [
            [
                {
                    "text": "{button}".format(button=but_['text']),
                    "callback_data": "{button}".format(button=but_['text'])
                }
                for but_ in str_
            ]
            for str_ in buttons]}
        keyboard = dumps(keyboard, ensure_ascii=False)
        return keyboard

    def send_text(self, chat_id, text, buttons=""):
        if buttons == "":
            params = {'chat_id': chat_id, 'text': text}
        else:
            params = {'chat_id': chat_id, 'text': text, 'reply_markup': buttons}
        return self.api("sendMessage", params)

    def sendImage(self, chat_id, image_src):
        url = self.url + self.token + "/sendPhoto"
        files = {'photo': open(image_src, 'rb')}
        data = {'chat_id': chat_id}
        r = requests.post(url, files=files, data=data)
        return r

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result) - 1]
        return last_update

    def polling(self):
        self.report("Waiting of service initialization.")
        time.sleep(5)
        self.report("Tg polling started.")
        while True:
            try:
                self.handle_response(self.get_updates(self.new_offset))
            except requests.exceptions.ReadTimeout:
                self.report('Lost internet connection.')
                time.sleep(5)
            except KeyError:
                self.report('Updating data.' + traceback.format_exc())

    def handle_response(self, updates):
        for update in updates:
            self.report(str(update))
            if "callback_query" in update:
                self.new_offset = update['update_id']
                # TODO: SEND MESSAGES TO THE ADMINS
                # # if update['callback_query']['message']['chat']['id'] != 204702595:
                #     self.send_text(204702595, update['callback_query']['data'] + "(cb)  from  " + str(
                #         update['callback_query']['message']['chat']['id']))
                self.new_offset = update['update_id'] + 1

                message = {
                    "source": "TG",
                    "message_id": update["callback_query"]["message"]["message_id"],
                    "user_id": update["callback_query"]["message"]["chat"]["id"],
                    "name": update["callback_query"]["message"]["chat"]["first_name"],
                    "unix_time": update["callback_query"]["message"]["date"],
                    "text": update['callback_query']['data'].lower(),
                    "attachments": []
                }
                message = Message(message)
                self.social_source.handle_new_message(message)
                self.ansOnCallback(update['callback_query']['id'])
                continue
            elif "message" in update:
                try:
                    # if "text" in update['message'] and update['message']['chat']['id'] != 204702595:
                    #     self.send_text(204702595,
                    #                    update['message']['text'] + "  from  " + str(update['message']['chat']['id']))
                    self.new_offset = update['update_id'] + 1
                    if "document" in update["message"]:
                        document = update["message"]["document"]
                        attachments = [{
                            "id": str(document["file_id"]),
                            "name": document["file_name"],
                            "link": "https://api.telegram.org/file/bot" + self.token + '/' + self.api(
                                "getFile",
                                {'file_id': document['file_id']})['file_path'],
                            "size": document["file_size"],
                            "ext": document["file_name"][document["file_name"].rfind(".") + 1:] if "." in document[
                                "file_name"] else ""
                        }]
                    else:
                        attachments = []
                    message = {
                        "source": "TG",
                        "name": update["message"]["chat"]["first_name"],
                        "message_id": update["message"]["message_id"],
                        "user_id": update["message"]["chat"]["id"],
                        "unix_time": update["message"]["date"],
                        "text": update['message']['text'].lower() if "text" in update['message'].keys() else "",
                        "attachments": attachments
                    }
                    message = Message(message)
                    self.social_source.handle_new_message(message)
                except:
                    self.report('Error of handling update.', traceback.format_exc())

    def start_polling(self):
        try:
            self.polling_thread = threading.Thread(target=self.polling)
            self.polling_thread.start()
        except:
            self.report("Restarting TG polling.")
            self.start_polling()


class SocialSource:

    def __init__(self, dao, settings):
        self.dao = dao
        self.vk = VK(self, settings['vk'])
        self.tg = TG(self, settings['tg'])

    def report(self, message, trace=None, module="", info=False):
        self.dao.report(message, trace=trace, module='/social_source' + module, info=info)

    def handle_new_message(self, message):
        # TODO : check if user is blocked
        event = {
            "type": "new_message",
            "message": message
        }
        self.dao.notify_service(event)

    def send_text(self, user_id, source, text, buttons=None):
        # def gen_str_list(buttons):
        # for str_ in buttons:
        # for but in str_:
        # yield but["text"]

        if buttons is None:
            buttons = {}
        if source == "TG":
            if buttons:
                buttons = self.tg.make_buttons(buttons)
                self.tg.send_text(user_id, text, buttons)
            else:
                self.tg.send_text(user_id, text)
        elif source == "VK":
            if buttons:
                # Appends buttons to text (feature for future)
                # text += "\n" + ("\n".join(list(gen_str_list(buttons)))) if buttons else ""
                buttons = self.vk.make_buttons(buttons)
                self.vk.send_text(user_id, text, buttons)
            else:
                self.vk.send_text(user_id, text)


class DAO:
    def __init__(self, service, system_settings):
        self.settings = system_settings
        self.service = service
        self.social_source = SocialSource(self, self.settings['social'])

    def __str__(self):
        string_ = '\n'.join([str(self.settings), str(self.social_source)])
        return string_

    def report(self, message, trace=None, module="", info=False):
        self.service.report(message, trace=trace, module='/dao' + module, info=info)

    def get_printers(self, user_id=None, source=None):
        try:
            return []
        except:
            self.report("Список принтеров не получен: ", traceback.format_exc())
            return []

    def send_text(self, user_id, source, text, buttons=None):
        self.social_source.send_text(user_id, source, text, buttons)

    def get_admins(self):
        try:
            return []
        except:
            self.report("Ошибка` получения админов.", traceback.format_exc())
            return []

    def is_user_registered(self, user_id, source):
        try:
            return False
        except:
            self.report("Checking of user's registration failed.", traceback.format_exc())
            return True

    def register_user(self, user_dict):
        # user_id: 000,
        # source: "vk",
        # status: "not blocked",
        # name: "Ivan"

        try:
            self.report("New user registered: " + str(user_dict))
        except:
            self.report("Can't register user.", traceback.format_exc())

    def get_user(self, user_id, source):
        try:
            user = {}
            return user
        except:
            self.report("Error 114.", traceback.format_exc())
            return None

    def notify_service(self, event):
        self.service.add_event(event)
        self.report("Service notified. Event: " + str(event))

    def user_has_paid_order(self, user_id, source):
        return False

    def get_name_of_last_order(self, user_id, source):
        return "File"

    def remove_not_paid_orders(self, user_id, source):
        return None

    def create_order_in_db(self, message):

        return 0

    def is_printer_available_for_order(self, printer_id, message):
        return False

    def is_promo_available(self, user_id, source, order_id, promo):
        return False

    def update_message(self, message):
        return False

    def get_message_by_order_id(self, order_id):

        return None

    def update_printer_id_of_order(self, printer_id, order_id):
        pass

    def update_price_of_order(self, price, order_id):
        pass

    def update_online_of_printer(self, printer_id):
        pass

    def get_payment_methods(self, user_id, source, printer_id, price=0):
        pass

    def get_buttons_of_payment_methods(self, message):
        pass

    def count_price(self, printer_id, pages):
        pass

    def get_kassa_credentails(self):
        pass

    def create_payment_for_order(self, message):
        pass
