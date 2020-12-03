# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import time
import os

from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, initialize_logger, lprint_exception
from .capture import CaptureAudioFromMic


SERVICE_NAME = os.environ.get("SERVICE", "capture-audio-from-mic")
SLEEP_TIME = os.environ.get("SLEEP_TIME", "0.5")
DEVICE_NAME = os.environ.get("DEVICE_NAME")
LOOP_COUNT = os.environ.get("LOOP_COUNT", "10")
DEVICE_INDEX = os.environ.get("DEVICE_INDEX", 24)
initialize_logger(SERVICE_NAME)


@main_decorator(SERVICE_NAME)
def main_with_kanban(opt: Options):
    lprint("start main_with_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban = conn.get_one_kanban(SERVICE_NAME, num)


    # get output data path
    data_path = kanban.get_data_path()
    # get previous service list
    service_list = kanban.get_services()

    ######### main function #############

    # output after kanban
    conn.output_kanban(
        result=True,
        connection_key="key",
        output_data_path=data_path,
        process_number=num,
    )


@main_decorator(SERVICE_NAME)
def main_without_kanban(opt: Options):
    lprint("start main_without_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)

    # get output data path
    # data_path = kanban.get_data_path()
    # get previous service list
    # service_list = kanban.get_services()
    # print(service_list)

    ######### main function #############
    while True:
        try:
            captureObj = CaptureAudioFromMic(DEVICE_INDEX,
                                             sampling_rate=32000, rec_time=60)
            outputFilePath = captureObj.output_wave_file()
        except Exception as e:
            lprint_exception(e)
            break

        lprint("> Success: output audio (path: {})".format(outputFilePath))

        # output after kanban
        conn.output_kanban(
            result=True,
            connection_key="default",
            metadata={"audio_file_path": outputFilePath},
        )


@main_decorator(SERVICE_NAME)
def main_with_kanban_itr(opt: Options):
    lprint("start main_with_kanban_itr()")
    # get cache kanban
    conn = opt.get_conn()
    num = int(opt.get_number())
    try:
        for kanban in conn.get_kanban_itr(SERVICE_NAME, num):
            metadata = kanban.get_metadata()
            lprint(metadata)
    except Exception as e:
        print(str(e))
    finally:
        pass

@main_decorator(SERVICE_NAME)
def send_kanbans_at_highspeed(opt: Options):
    lprint("start send_kanbans_at_highspeed()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban: Kanban = conn.set_kanban(SERVICE_NAME, num)
    data_path = kanban.get_data_path()

    index = 0
    while True:
        if index > int(LOOP_COUNT):
            lprint("break loop")
            break

        conn.output_kanban(
            result=True,
            connection_key="default",
            output_data_path=data_path,
            metadata={
                "data": {
                    "key": index,
                    "dataForm": "normal",
                    "robotData": [
                        {
                            "robotStatus": 0,
                            "sample": "いしい",
                        },
                    ],
                    "arrayNo": 1,
                }
            },
            process_number=num,
            device_name=DEVICE_NAME,
        )
        index = index + 1
        time.sleep(float(SLEEP_TIME))
