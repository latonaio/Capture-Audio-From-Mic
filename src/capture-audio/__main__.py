# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os

from . import main_with_kanban, main_without_kanban, main_with_kanban_itr, send_kanbans_at_highspeed

KANBAN_MODE = os.environ.get("KANBAN_MODE", "main_without_kanban")

if __name__ == "__main__":
    if KANBAN_MODE == "main_without_kanban":
        main_without_kanban()
    elif KANBAN_MODE == "main_with_kanban":
        main_with_kanban()
    elif KANBAN_MODE == "main_with_kanban_itr":
        main_with_kanban_itr()
    elif KANBAN_MODE == "send_kanbans_at_highspeed":
        send_kanbans_at_highspeed()
