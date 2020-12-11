from datetime import datetime


class Message:
    class MessageError(Exception):
        def __init__(self, message):
            # Call the base class constructor with the parameters it needs
            super().__init__(message)

    def __init__(self, dict_):
        try:
            self.message_id = dict_["message_id"]
            self.user_id = dict_["user_id"]
            self.chat_id = dict_["chat_id"]
            self.chat_obj = dict_["chat_obj"]
            self.source = dict_["source"]
            self.name = dict_["name"]
            self.unix_time = dict_["unix_time"]
            self.text = dict_["text"]
            self.attachments = dict_["attachments"]
            self.obj_dict = dict_.get("obj", None)
            self.final_files = []
            self.pages = 0
            self.price = 0
            self.status = "created"
            self.order_id = 0
            self.printer_id = 0
            self.kassa_id = 0
        except:
            raise self.MessageError("Wrong params.")

    def to_dict(self):
        try:
            dict_ = {
                "message_id": self.message_id,
                "user_id": self.user_id,
                "source": self.source,
                "final_files": ", ".join(self.final_files),
                "status": self.status,
                "pages": self.pages,
                "order_id": self.order_id,
                "time_": datetime.utcfromtimestamp(self.unix_time).strftime('%Y-%m-%d %H:%M:%S')
            }
            return dict_
        except:
            return {"message_id": self.message_id,
                    "user_id": self.user_id,
                    "source": self.source,
                    "order_id": self.order_id,
                    "printer_id": self.printer_id}
