import pathlib

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class SettingsEntryBox(qtw.QWidget):
    def __init__(
        self, settings, key, value_type, validator=None, callback=None, label=None, left_margin=0
    ):
        super().__init__()
        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(left_margin, 0, 0, 0)
        self.setLayout(layout)

        if label is None:
            label = qtw.QLabel(str(key).replace("_", " "))
        else:
            label = qtw.QLabel(str(label))
        label.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
        layout.addWidget(label)

        self.edit_box = qtw.QLineEdit()
        layout.addWidget(self.edit_box)
        self.edit_box.setText(str(settings.dict[key]))
        if validator:
            self.edit_box.setValidator(validator)

        def edit_callback():
            value = value_type(self.edit_box.text())
            settings.dict[key] = value

        self.edit_box.editingFinished.connect(edit_callback)
        if callback is not None:
            try:
                for each in callback:
                    self.edit_box.editingFinished.connect(each)
            except TypeError:
                self.edit_box.editingFinished.connect(callback)


class SettingsRangeBox(qtw.QWidget):
    def __init__(self, settings, label, low_key, high_key, value_type, validator=None, callback=None):
        super().__init__()
        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.settings = settings
        self.value_type = value_type
        self.low_key = low_key
        self.high_key = high_key
        self.callback = callback

        if label != "":
            label = qtw.QLabel(label)
            label.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
            layout.addWidget(label)

        self.low_entry = qtw.QLineEdit()
        layout.addWidget(self.low_entry)
        self.low_entry.setText(str(settings.dict[low_key]))
        if validator:
            self.low_entry.setValidator(validator)

        self.high_entry = qtw.QLineEdit()
        layout.addWidget(self.high_entry)
        self.high_entry.setText(str(settings.dict[high_key]))
        if validator:
            self.high_entry.setValidator(validator)

        self.low_entry.editingFinished.connect(self.low_callback)
        self.high_entry.editingFinished.connect(self.high_callback)

    def low_callback(self):
        low_value = self.value_type(self.low_entry.text())
        high_value = self.value_type(self.high_entry.text())

        if low_value >= high_value:
            self.low_entry.setStyleSheet("QLineEdit { background-color: pink}")
        else:
            self.common_callback(low_value, high_value)

    def high_callback(self):
        low_value = self.value_type(self.low_entry.text())
        high_value = self.value_type(self.high_entry.text())

        if high_value <= low_value:
            self.high_entry.setStyleSheet("QLineEdit { background-color: pink}")
        else:
            self.common_callback(low_value, high_value)

    def common_callback(self, low_value, high_value):
        self.high_entry.setStyleSheet("QLineEdit { background-color: white}")
        self.low_entry.setStyleSheet("QLineEdit { background-color: white}")
        self.settings.dict[self.low_key] = low_value
        self.settings.dict[self.high_key] = high_value
        if self.callback is not None:
            try:
                for each in self.callback:
                    each()
            except TypeError:
                self.callback()

    def set_range(self, low, high):
        self.low_entry.setText(str(low))
        self.low_callback()
        self.high_entry.setText(str(high))
        self.high_callback()


class SettingsFileBox(qtw.QWidget):
    def __init__(
            self, settings, key, system_path, filter="*", mode=None, callback=None, callback_2=None
    ):
        super().__init__()
        self.filter = filter
        self.system_path = system_path
        if mode == "save":
            self.do_save = True
            self.do_load = False
            self.do_save_dialog_type = True
            self.save_callback = callback
            self.load_callback = None
        elif mode == "load":
            self.do_save = False
            self.do_load = True
            self.do_save_dialog_type = False
            self.save_callback = None
            self.load_callback = callback
        elif mode == "both":
            self.do_save = True
            self.do_load = True
            self.do_save_dialog_type = True
            self.save_callback = callback
            self.load_callback = callback_2
        elif mode == "none" or mode is None:
            self.do_save = False
            self.do_load = False
            self.do_save_dialog_type = True
            self.save_callback = None
            self.load_callback = None
        else:
            raise ValueError("SettingsFileBox: mode must be specified, and one of {save, load, both, none}")
        self.settings = settings
        self.key = key

        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        if self.do_save:
            self.save_button = qtw.QPushButton("Save")
            self.save_button.setMaximumWidth(32)
            self.save_button.clicked.connect(self.save)
            layout.addWidget(self.save_button)
        if self.do_load:
            self.load_button = qtw.QPushButton("Load")
            self.load_button.setMaximumWidth(32)
            self.load_button.clicked.connect(self.load)
            layout.addWidget(self.load_button)

        self.select_button = qtw.QPushButton("Select")
        self.select_button.setMaximumWidth(37)
        self.select_button.clicked.connect(self.select)
        layout.addWidget(self.select_button)

        self.label = qtw.QLineEdit()
        self.label.setText(str(self.settings.dict[key]))
        self.label.setReadOnly(True)
        layout.addWidget(self.label)

    def save(self):
        if self.save_callback is not None:
            try:
                self.save_callback()
            except TypeError:
                for each in self.save_callback:
                    each()

    def load(self):
        if self.load_callback is not None:
            try:
                self.load_callback()
            except TypeError:
                for each in self.load_callback:
                    each()

    def select(self):
        if self.do_save:
            selected_file, _ = qtw.QFileDialog.getSaveFileName(
                directory=str(self.system_path), filter=self.filter
            )
        else:
            selected_file, _ = qtw.QFileDialog.getOpenFileName(
                directory=str(self.system_path), filter=self.filter
            )
        if selected_file:
            self.settings.dict[self.key] = str(pathlib.Path(selected_file))
            self.label.setText(selected_file)
        self.label.setStyleSheet("QLineEdit { background-color: white}")

    def notify_bad_selection(self):
        self.label.setStyleSheet("QLineEdit { background-color: pink}")


class SettingsComboBox(qtw.QWidget):
    def __init__(self, component, label, settings_key, settings_options, callback=None):
        super().__init__()
        self.component = component
        self.settings_key = settings_key
        self.settings_options = settings_options

        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        layout.addWidget(qtw.QLabel(label))

        selector = qtw.QComboBox()
        layout.addWidget(selector)
        selector.addItems(settings_options)
        selector.setCurrentIndex(settings_options.index(self.component.settings.dict[settings_key]))
        selector.currentIndexChanged.connect(self.set_setting)

        if callback is not None:
            try:
                for each in callback:
                    selector.currentIndexChanged.connect(each)
            except TypeError:
                selector.currentIndexChanged.connect(callback)

    def set_setting(self, index):
        self.component.settings.dict[self.settings_key] = self.settings_options[index]


class SettingsVectorBox(qtw.QWidget):
    def __init__(self, settings, label, settings_key, callback=None):
        super().__init__()
        self.settings = settings
        self.settings_key = settings_key

        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        layout.addWidget(qtw.QLabel(label))
        self.entries = []
        for i in range(3):
            initial = self.settings.dict[settings_key][i]
            entry = qtw.QLineEdit()
            self.entries.append(entry)
            entry.setText(str(initial))
            entry.setValidator(qtg.QDoubleValidator(-1e6, 1e6, 7))
            layout.addWidget(entry)

        self.entries[0].editingFinished.connect(self.callback_x)
        self.entries[1].editingFinished.connect(self.callback_y)
        self.entries[2].editingFinished.connect(self.callback_z)

        if callback is not None:
            try:
                for each in callback:
                    self.entries[0].editingFinished.connect(each)
                    self.entries[1].editingFinished.connect(each)
                    self.entries[2].editingFinished.connect(each)
            except TypeError:
                self.entries[0].editingFinished.connect(callback)
                self.entries[1].editingFinished.connect(callback)
                self.entries[2].editingFinished.connect(callback)

    def callback_x(self):
        value = float(self.entries[0].text())
        self.settings.dict[self.settings_key][0] = value

    def callback_y(self):
        value = float(self.entries[1].text())
        self.settings.dict[self.settings_key][1] = value

    def callback_z(self):
        value = float(self.entries[2].text())
        self.settings.dict[self.settings_key][2] = value


class SettingsCheckBox(qtw.QWidget):
    def __init__(self, settings, key, label, callback=None):
        super().__init__()

        layout = qtw.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.label = qtw.QLabel(label)
        layout.addWidget(self.label)

        check_box = qtw.QCheckBox()
        layout.addWidget(check_box)
        check_box.setCheckState(settings.dict[key])
        check_box.setTristate(False)

        def set_setting(new_state):
            settings.dict[key] = bool(new_state)

        check_box.stateChanged.connect(set_setting)

        if callback is not None:
            try:
                for each in callback:
                    check_box.stateChanged.connect(each)
            except TypeError:
                check_box.stateChanged.connect(callback)


class ColorEntryButton(qtw.QPushButton):
    def __init__(self, settings, key, callback=None):
        super().__init__()
        self.setText("Color")
        self.clicked.connect(self.click)
        self.callback = callback
        self.settings = settings
        self.key = key

    def click(self):
        color = qtw.QColorDialog.getColor().name()
        self.settings.dict[self.key] = color
        self.setStyleSheet(f"QPushButton {{ background-color: {color}}}")
        self.callback()
