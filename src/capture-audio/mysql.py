import aion.mysql as mysql


class MysqlManager(mysql.BaseMysqlAccess):
    """UpdateDeviceStateToDB
        Store device list to mysql
        This function will be deleted.
    """
    def __init__(self):
        super().__init__("PeripheralDevice")

    def update_microphone_state(self):
        sql = """
            INSERT INTO microphones SET available_flg = true;
            """
        self.set_query(sql)

    def update_down_device_state(self):
        """
            update device state in mysql which is not attached
        """
        now = datetime.now() - timedelta(seconds=1)
        sql = """
            UPDATE cameras
            SET path = "", state = 0
            WHERE timestamp < %(time)s
            """
        args = {"time": now.strftime('%Y-%m-%d %H:%M:%S')}
        self.set_query(sql, args)

    def check_invalid_state(self):
        """
            update device state in mysql which is not attached
        """
        now = datetime.now() + timedelta(seconds=10)
        sql = """
            UPDATE cameras
            SET path = "", state = 0
            WHERE timestamp > %(time)s
            """
        args = {"time": now.strftime('%Y-%m-%d %H:%M:%S')}
        self.set_query(sql, args)

