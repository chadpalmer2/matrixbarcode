from qr import QRCode, ErrorCorrectLevel
import pdb

# generate with explicit type number
qr = QRCode()
qr.setTypeNumber(4)
qr.setErrorCorrectLevel(ErrorCorrectLevel.M)
qr.addData('here comes qr!')
qr.make()

# generate with auto type number
# qr = QRCode.getMinimumQRCode('here comes qr!', ErrorCorrectLevel.M)
# create an image

for r in range(qr.getModuleCount() ):
    for c in range(qr.getModuleCount() ):
        print(u'\u25a1', end="") if qr.isDark(r, c) else print(u'\u25a0', end="")
    print()