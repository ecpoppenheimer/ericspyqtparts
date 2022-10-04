import pickle


class Settings:
    """
    A simple settings data class, which is basically just a wrapper for a dict that exposes its keys as attributes
    """
    def __init__(self, settings_path=None, **kwargs):
        object.__setattr__(self, "dict", dict(**kwargs))
        self.settings_path = settings_path
        if self.settings_path is not None:
            try:
                self.load(self.settings_path)
            except Exception:
                pass

    def keys(self):
        return self.dict.keys()

    def update(self, updates):
        self.dict.update(updates)

    def establish_defaults(self, **kwargs):
        keys = set(self.keys())
        for key, value in kwargs.items():
            if key not in keys:
                self.dict[key] = value
        return set(kwargs.keys())

    def get_subset(self, subset):
        return {key: self.dict[key] for key in subset}

    def __getattribute__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return self.dict[key]

    def __setattr__(self, key, value):
        if key in {"dict", "keys", "update", "dict"}:
            object.__setattr__(self, key, value)
        else:
            self.dict[key] = value

    def load(self, filename):
        with open(filename, "rb") as inFile:
            self.update(pickle.load(inFile))
        self.upconvert_dicts()

    def reload(self, filename):
        """
        Differs from load in that this function will update in place, so references are preserved.
        """
        with open(filename, "rb") as inFile:
            new_data = pickle.load(inFile)
            for key, value in new_data.items():
                if type(value is dict):
                    self.dict[key].update(value)
                else:
                    self.dict[key] = value

    def save(self, filename=None):
        if filename is None:
            filename = self.settings_path
        if filename is None:
            raise ValueError("Settings file path was never provided.")
        with open(filename, "wb") as outFile:
            pickle.dump(self.dict, outFile)

    def upconvert_dicts(self):
        for key in self.keys():
            if type(self.dict[key]) is dict:
                self.dict[key] = Settings(**self.dict[key])
