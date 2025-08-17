
from razrc522.rfid import RFID
from razrc522.easyrfid import EasyRFID, EasyRFIDUIDMode, EasyRFIDAuth

reader = RFID(antenna_gain=7, logger = None)
easyRFID = EasyRFID(reader, mode=EasyRFIDUIDMode.HEX)
while True:
    convertedUID, rawUID = easyRFID.wait_and_select()
    block = 0
    # Standard MIFARE 1k key
    authorized = easyRFID.authorize(EasyRFIDAuth.AuthB, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], rawUID, block)
    if authorized:
        readed = easyRFID.read_block(block)
        if readed:
            fullUUID = easyRFID.bytes_to_uid(readed, EasyRFIDUIDMode.HEX)
            print(convertedUID, "vs", fullUUID)


