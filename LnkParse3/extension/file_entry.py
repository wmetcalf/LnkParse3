from struct import unpack
from LnkParse3.extension.extension_base import ExtensionBase
from LnkParse3.decorators import dostime


class FileEntry(ExtensionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_item(self):
        item = super().as_item()
        item["creation_time"] = self.creation_time()
        item["last_access_time"] = self.last_access_time()
        item["long_name"] = self.long_name()
        return item

    @dostime
    def creation_time(self):
        start, end = 8, 12
        return self._raw[start:end]

    @dostime
    def last_access_time(self):
        start, end = 12, 16
        return self._raw[start:end]

    def long_name(self):
        version = self.version()
        if version < 3:
            return ""

        start = 18
        if version >= 3:
            start += 2
        if version >= 7:
            start += 18
        if version >= 8:
            start += 4
        if version >= 9:
            start += 4

        binary = self._raw[start:]
        text = self.text_processor.read_unicode_string(binary)
        return text
