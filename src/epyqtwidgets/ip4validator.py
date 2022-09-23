import PyQt5.QtGui as qtg


class IP4Validator(qtg.QValidator):
    """
    Validator to check the validity of the IP address.  This code was copied with minor modifications from
    https://stackoverflow.com/questions/53873737/pyqt5-qline-setinputmask-setvalidator-ip-address
    """
    def __init__(self, parent=None):
        super(IP4Validator, self).__init__(parent)

    def validate(self, address, pos):
        if not address:
            return qtg.QValidator.Acceptable, address, pos

        # check to permit 'localhost'
        if address == "localhost":
            return qtg.QValidator.Acceptable, address, pos
        elif address in "localhost":
            return qtg.QValidator.Intermediate, address, pos

        octets = address.split(".")
        size = len(octets)
        if size > 4:
            return qtg.QValidator.Invalid, address, pos
        empty_octet = False
        for octet in octets:
            if not octet or octet == "___" or octet == "   ":  # check for mask symbols
                empty_octet = True
                continue
            try:
                value = int(str(octet).strip(' _'))  # strip mask symbols
            except Exception:
                return qtg.QValidator.Intermediate, address, pos
            if value < 0 or value > 255:
                return qtg.QValidator.Invalid, address, pos
        if size < 4 or empty_octet:
            return qtg.QValidator.Intermediate, address, pos
        return qtg.QValidator.Acceptable, address, pos