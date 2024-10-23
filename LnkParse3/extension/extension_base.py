from struct import unpack
from LnkParse3.text_processor import TextProcessor


class ExtensionBase:
    def __init__(self, indata=None, cp=None):
        self._raw = indata

        self.cp = cp
        self.text_processor = TextProcessor(cp=self.cp)

    def as_item(self):
        return {
            "name": self.name(),
            "signature": self.signature(),
            "version": self.version(),
        }

    @classmethod
    def name(cls):
        return cls.__class__.__name__

    def size(self):
        start, end = 0, 2
        size = unpack("<H", self._raw[start:end])[0]
        return size

    def version(self):
        start, end = 2, 4
        version = unpack("<H", self._raw[start:end])[0]
        return version

    def signature(self):
        start, end = 4, 8
        version = unpack("<I", self._raw[start:end])[0]
        return version
