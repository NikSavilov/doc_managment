from dashboard.polling.service import Service
from secret.bot_settings import settings


def read_settings():
    variants = {}
    v_string = "\n"
    for var in settings.keys():
        name_ = settings[var]['name']
        variants.update({var: name_})
        v_string += str(var) + ") " + name_ + "\n"
    structure = 0

    read_settings = settings[structure]
    return read_settings


def get_service():
    system_settings = read_settings()
    service = Service(system_settings)
    return service
