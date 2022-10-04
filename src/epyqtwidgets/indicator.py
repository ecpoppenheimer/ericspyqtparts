import PyQt5.QtWidgets as qtw


class Indicator(qtw.QFrame):
    DEFAULT_SIZE = 20

    def __init__(self, color, indicator_size=None):
        super().__init__()
        self.set_color(color)
        size = indicator_size or self.DEFAULT_SIZE
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setMaximumHeight(size)
        self.setMinimumHeight(size)
        self.setAutoFillBackground(True)

    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")
