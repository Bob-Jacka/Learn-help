from typing import OrderedDict

from fastapi import FastAPI

from main import App


class Cache:
    suits_data_cache: OrderedDict = None


web_server: FastAPI = FastAPI(description="Small web server for sending question data to mobile app")


@web_server.get("/get_questions", description="Get questions data")
def send_data():
    print('Getting question suits to mobile')
    if Cache.suits_data_cache is None:
        App.check_for_all()
        App.check_for_global()
        suits = App.get_suits(with_questions=True)
        Cache.suits_data_cache = suits
        return suits
    return Cache.suits_data_cache


@web_server.get("/get_questions/<str>", description="Get questions data of one suit")
def send_data():
    # TODO
    if Cache.suits_data_cache is None:
        App.check_for_all()
        App.check_for_global()
        suits = App.get_suits(with_questions=True)
        Cache.suits_data_cache = suits
        if None in suits:
            return Cache.suits_data_cache
    return App.get_suits(with_questions=True)


@web_server.get("/status")
def get_status():
    print('Connection!')
    return {"status": "ok"}


@web_server.post('/statistics', description="Receive statistics from mobile client")
def get_statistics():
    print('Receiving statistics from mobile')
    pass
