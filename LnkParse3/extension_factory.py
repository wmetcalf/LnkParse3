from struct import unpack
from LnkParse3.extension.file_entry import FileEntry


class ExtensionFactory:
    EXTENSION_BLOCKS = {
        0xBEEF0004: FileEntry,
    }

    def __init__(self, indata):
        self._raw = indata

    def item_size(self):
        start, end = 0, 2
        size = unpack("<H", self._raw[start:end])[0]
        return size

    def extension_class(self):
        start, end = 4, 8
        sig = unpack("<I", self._raw[start:end])[0]
        return self.EXTENSION_BLOCKS.get(sig)
