
from razrc522.rfid import RFID
from razrc522.easyrfid import EasyRFID, EasyRFIDUIDMode

reader = RFID()
easyRFID = EasyRFID(reader)
allModes = [EasyRFIDUIDMode.HEX, EasyRFIDUIDMode.HEX_BACKWARD, EasyRFIDUIDMode.DECIMAL, EasyRFIDUIDMode.DECIMAL_BACKWARD, EasyRFIDUIDMode.BINARY, EasyRFIDUIDMode.BINARY_BACKWARD, EasyRFIDUIDMode.BASE64, EasyRFIDUIDMode.BASE64_BACKWARD, EasyRFIDUIDMode.INT_LIST, EasyRFIDUIDMode.RAW]
modeIndex = 0
currentMode = allModes[modeIndex]
while True:
    uid = easyRFID.wait_and_read_uid()
    nextMode = allModes[(modeIndex + 1) % len(allModes)]
    easyRFID.set_new_mode(nextMode)
    print(currentMode, uid, "next mode", nextMode)
    modeIndex = (modeIndex + 1) % len(allModes)