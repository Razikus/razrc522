
from razrc522.rfid import RFID
from razrc522.easyrfid import EasyRFID, EasyRFIDUIDMode, EasyRFIDAuth
import random

def random_string():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))

reader = RFID(antenna_gain=7, logger = None)
easyRFID = EasyRFID(reader, mode=EasyRFIDUIDMode.HEX)
while True:
    convertedUID, rawUID = easyRFID.wait_and_select()
    block = 8

    # Standard MIFARE 1k key
    authorized = easyRFID.authorize(EasyRFIDAuth.AuthB, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], rawUID, block)
    if authorized:
        readed = easyRFID.read_block(block)
        if readed:
            isALLZero = all(byte == 0 for byte in readed)
            if isALLZero:
                randomed = random_string()
                dataToWrite = bytes(randomed, 'utf-8')
                success = easyRFID.write_block(block, dataToWrite)
                if success:
                    print("Write successful", randomed)
            else:
                print("Readed from sector:", easyRFID.bytes_to_uid(readed, EasyRFIDUIDMode.STRING))

