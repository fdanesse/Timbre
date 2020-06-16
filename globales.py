import os
import json

import datetime  # https://docs.python.org/3/library/datetime.html

from collections import OrderedDict

BASEDIR = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.dirname(__file__)


def get_file_data(path):
    arch = open(path, "r")
    _dict = json.load(arch)
    arch.close()
    return _dict


def get_text_to_datetime_time(text):
    return datetime.datetime.strptime(text, '%H:%M:%S').time()


def get_datetime_time_to_text(_time):
    return datetime.time.strftime(_time, '%H:%M:%S')

def getHorarios():
    data = get_file_data(os.path.join(BASE_PATH, "horarios.json"))
    # FIXME: diccionario cuyas keys sean los horarios y tengan duración y turno como valores ?
    # El programa mira la hora y en función de ello determina en que timbre se encuentra
    # Debe mostrar:
    #   la hora
    #   el turno en el que se encuentra
    #   los timbres pasados en el turno
    #   El progreso de tiempo hacia el siguiente timbre
    #   Los timbres que faltan en el turno

    _dict = OrderedDict()
    for key in data.keys():
        for item in data[key]:
            timbre = get_text_to_datetime_time(item[0])            
            
            duracion = get_text_to_datetime_time(item[1])
            # FIXME: Timedelta? print (duracion, type(duracion))

            _dict[timbre] = {'duracion': duracion, 'turno': key}
    return _dict
