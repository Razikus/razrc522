from .rfid import RFID
from enum import Enum, StrEnum
import base64
from typing import Union, List, Optional


class EasyRFIDUIDMode(StrEnum):
    """
    RFID readers on the market sometimes return the UID in different formats.
    """
    HEX = "hex"
    HEX_BACKWARD = "hex_backward"
    DECIMAL = "decimal"
    DECIMAL_BACKWARD = "decimal_backward"
    BINARY = "binary"
    BINARY_BACKWARD = "binary_backward"
    BASE64 = "base64"
    BASE64_BACKWARD = "base64_backward"
    INT_LIST = "int_list"
    STRING = "string"
    RAW = "raw"


class EasyRFIDAuth(StrEnum):
    AuthA = "auth_a"
    AuthB = "auth_b"


class EasyRFID:
    def __init__(self, rfidReader: RFID, mode: EasyRFIDUIDMode = EasyRFIDUIDMode.INT_LIST):
        self.rfidReader = rfidReader
        self.mode = mode

    def bytes_to_uid(self, uid: List[int], mode_to_use: Optional[EasyRFIDUIDMode] = None) -> Union[
        str, bytes, List[int]]:
        mode_to_check = self.mode
        if mode_to_use:
            mode_to_check = mode_to_use

        if mode_to_check == EasyRFIDUIDMode.HEX:
            return ''.join(f'{byte:02x}' for byte in uid)
        elif mode_to_check == EasyRFIDUIDMode.HEX_BACKWARD:
            return ''.join(f'{byte:02x}' for byte in reversed(uid))
        elif mode_to_check == EasyRFIDUIDMode.DECIMAL:
            return ''.join(str(byte) for byte in uid)
        elif mode_to_check == EasyRFIDUIDMode.DECIMAL_BACKWARD:
            return ''.join(str(byte) for byte in reversed(uid))
        elif mode_to_check == EasyRFIDUIDMode.BINARY:
            return ''.join(f'{byte:08b}' for byte in uid)
        elif mode_to_check == EasyRFIDUIDMode.BINARY_BACKWARD:
            return ''.join(f'{byte:08b}' for byte in reversed(uid))
        elif mode_to_check == EasyRFIDUIDMode.BASE64:
            return base64.b64encode(bytes(uid)).decode('utf-8')
        elif mode_to_check == EasyRFIDUIDMode.BASE64_BACKWARD:
            return base64.b64encode(bytes(reversed(uid))).decode('utf-8')
        elif mode_to_check == EasyRFIDUIDMode.INT_LIST:
            return uid
        elif mode_to_check == EasyRFIDUIDMode.STRING:
            return ''.join(chr(byte) for byte in uid)
        else:
            return bytes(uid)

    def set_new_mode(self, newMode: EasyRFIDUIDMode):
        self.mode = newMode

    def wait_and_read_uid(self) -> Union[str, bytes, List[int]]:
        while True:
            self.rfidReader.wait_for_tag()
            error, req = self.rfidReader.request()
            if not error:
                error, uid = self.rfidReader.anticoll()
                if not error:
                    return self.bytes_to_uid(uid)

    def wait_and_select(self) -> tuple[Union[str, bytes, List[int]], List[int]]:
        while True:
            self.rfidReader.wait_for_tag()
            error, req = self.rfidReader.request()
            if not error:
                error, uid = self.rfidReader.anticoll()
                if not error:
                    selected = self.rfidReader.select_tag(uid)
                    if selected:
                        return self.bytes_to_uid(uid), uid

    def stop(self):
        return self.rfidReader.halt()

    def authorize(self, keyType: EasyRFIDAuth, key: List[int], uid: List[int], block: int):
        keyTypeRaw = RFID.auth_a
        if keyType == EasyRFIDAuth.AuthA:
            keyTypeRaw = RFID.auth_a
        elif keyType == EasyRFIDAuth.AuthB:
            keyTypeRaw = RFID.auth_b
        else:
            raise ValueError("Invalid key type")

        what = self.rfidReader.card_auth(keyTypeRaw, block, key, uid)
        return not what

    def read_block(self, block: int):
        error, data = self.rfidReader.read(block)
        if not error:
            return data
        return None

    def write_block(self, block: int, data: bytes):
        if (len(data) != 16):
            raise ValueError("Data must be exactly 16 bytes long")
        err = self.rfidReader.write(block, data)
        return not err

    def deauth(self):
        self.rfidReader.stop_crypto()
