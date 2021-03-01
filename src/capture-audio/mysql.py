import aion.mysql as mysql


class MysqlManager(mysql.BaseMysqlAccess):
    """UpdateDeviceStateToDB
        Store device list to mysql
        This function will be deleted.
    """
    def __init__(self):
        super().__init__("PeripheralDevice")

    def update_microphone_state(self, card_no, device_no):
        sql = """
            UPDATE microphones SET available_flg = true WHERE card_no = %(card_no)s AND device_no = %(device_no)s ;
            """
        args = {"card_no": card_no, "device_no": device_no}
        self.set_query(sql, args)
