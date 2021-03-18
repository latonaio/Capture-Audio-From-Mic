import aion.mysql as mysql
from aion.logger import lprint
from enum import Enum


class MicStatus(Enum):
    STANDBY = 'standby'
    ACTIVE = 'active'
    DISABLE = 'disable'


class MysqlManager(mysql.BaseMysqlAccess):
    """UpdateDeviceStateToDB
        Store device list to mysql
        This function will be deleted.
    """

    def __init__(self):
        super().__init__("PeripheralDevice")

    def update_microphone_state(self, card_no, device_no, status: MicStatus, processNum):
        sql = """
            UPDATE microphones SET status = %(status)s, manager_pod_process_num = %(processNum)s WHERE card_no = %(card_no)s AND device_no = %(device_no)s ;
            """
        args = {"card_no": card_no, "device_no": device_no, "status": status.value, "processNum": processNum}
        self.set_query(sql, args)
