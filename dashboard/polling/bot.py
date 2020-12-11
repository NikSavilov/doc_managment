import threading
import traceback
from collections import deque

import requests
from django.core.files.base import ContentFile

from doc_managment.settings import BOT_SYSTEM_KEYWORD, FIRST_BOT_MESSAGE, IGNORE_BOT_INVITATION_MESSAGE
from .message import Message
from ..models import Document, Group, InformationObject, InfoObjectCategory, Keyword


class Bot:

    def __init__(self, service):
        self.service = service
        self.command_handlers = {"[first_join]": self.com_first_join}
        self.event_queue = deque()
        self.queue_listener_thread = threading.Thread(target=self.queue_listener)
        self.queue_listener_thread.start()
        self.thread_limiter = threading.BoundedSemaphore(10)
        self.report("Bot had been initialized successfully.")

    def report(self, message, trace=None, module="", info=False):
        self.service.report(message, trace=trace, module='/bot' + module, info=info)

    def send_text(self, user_id, source, text, buttons=None):
        self.service.dao.send_text(user_id, source, text, buttons)

    def hello(self):
        with open('bin/hello.txt', 'r', encoding='utf-8') as f:
            hello = f.read()
        return hello

    def rules(self):
        with open('bin/rules.txt', 'r', encoding='utf-8') as f:
            rules = f.read()
        return rules

    def queue_listener(self):
        while True:
            if self.event_queue:
                current_event = self.event_queue.popleft()
                thread = threading.Thread(target=self.handle_event, args=(current_event,))
                thread.setDaemon(True)
                thread.start()

    def is_in_dict(self, dict_, word):
        # Returns True if word or similar is in dict_
        for variant in dict_:
            if word.find(variant) != -1:
                return True
        return False

    def handle_event(self, event):
        self.report("Event: {}".format(event))
        if event["type"] == "new_message":
            # Incoming message handler
            message = event["message"]
            self.handle_message(message)
        else:
            print("WTF")

    def handle_message(self, message: Message):
        try:
            words = message.text.split()
            if words and words[0] == BOT_SYSTEM_KEYWORD:
                if words.__len__() > 1:
                    command = words[1]
                    handler = self.command_handlers.get(command, self.com_unknown)
                    handler(message)
            if message.attachments:
                self.handle_docs(message)
        except:
            self.error_answer(message)

    def error_answer(self, message):
        self.send_text(message.chat_id,
                       message.source,
                       "Произошла непредвиденная ошибка. Мы уже работаем над ее устранением.")
        self.report("Unknown error.", traceback.format_exc())

    def com_unknown(self, message: Message):
        self.send_text(message.user_id, message.source, "Неизвестная команда")

    def handle_docs(self, message: Message):
        default_category = {0: None}
        if message.text:
            for kwd in Keyword.objects.all():
                if message.text.find(kwd.word) != -1:
                    default_category.update({10: kwd.category})
                    break
            if not default_category.get(10, None):
                for cat in InfoObjectCategory.objects.all():
                    words = cat.title.split()
                    words = [s.lower() for s in words]
                    prefixes_ = [word[:2] for word in words] if words.__len__() > 1 else [words[0][:3]]
                    found = [message.text.find(prefix) != -1 for prefix in prefixes_]
                    if all(found):
                        default_category.update({prefixes_.__len__(): cat})
                        break
        def_category = default_category[max(default_category.keys())]
        for attachment in message.attachments:
            already_send = set()
            bin_f = requests.get(attachment['link']).content
            groups = Group.objects.filter(chat_id_vk=message.chat_id)
            for group in groups:
                doc = Document.objects.create(filename=attachment["name"],
                                              extension=attachment["ext"],
                                              file_url=attachment['link'],
                                              size=attachment['size'],
                                              source=InformationObject.Source.VK,
                                              connected_group=group,
                                              source_id=attachment['id'],
                                              category=def_category
                                              )
                doc.file.save(attachment["name"], ContentFile(bin_f))
                msg = "Документ {file} добавлен в группу {group} {cat}".format(
                    file=attachment["name"],
                    group=group.name,
                    cat="с категорией {}".format(def_category.title) if isinstance(def_category, InfoObjectCategory)
                    else ""
                )
                if message.chat_id not in already_send:
                    self.send_text(message.chat_id, message.source, msg)
                    already_send.add(message.chat_id)

    def com_first_join(self, message: Message):
        for word in message.text.split():
            if word.find("tuckdock") > -1:
                group_uuid = word[8:]
                try:
                    cur_group = Group.objects.get(group_uuid=group_uuid)
                except:
                    cur_group = None
                if isinstance(cur_group, Group):
                    if not cur_group.chat_id_vk:
                        cur_group.chat_id_vk = message.chat_id
                        title = message.chat_obj["chat_settings"]["title"]
                        cur_group.name = title
                        cur_group.save()
                        invite_link = cur_group.get_invite()
                        msg = FIRST_BOT_MESSAGE.format(group_name=title, invite_link=invite_link)
                        self.send_text(message.chat_id, message.source, msg)
                    else:
                        msg = IGNORE_BOT_INVITATION_MESSAGE.format(admin=cur_group.administrator.username,
                                                                   link=cur_group.get_invite())
                        self.send_text(message.chat_id, message.source, msg)
