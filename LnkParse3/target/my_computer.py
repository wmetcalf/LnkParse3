from struct import unpack
from LnkParse3.target.lnk_target_base import LnkTargetBase

"""
----------------------------------------------------------------------
|              0-7b              |               8-15b               |
----------------------------------------------------------------------
| ClassTypeIndicator == 0x20-0x2F|            UnknownData            |
----------------------------------                                   |
|                                             ? B                    |
----------------------------------------------------------------------

https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#33-volume-shell-item
"""


# TODO: rename to volume_shell_item
class MyComputer(LnkTargetBase):
    def __init__(self, *args, **kwargs):
        self.name = "Volume Item"
        super().__init__(*args, **kwargs)

    def as_item(self):
        item = super().as_item()
        flags = self.flags()
        item["flags"] = f"0x{flags:02X}"
        if flags & 0x01:  # HasName
            item["name"] = self.volume_name()
        return item

    # dup: ./shell_fs_folder.py flags()
    # dup: ../target_factory.py item_type()
    def flags(self):
        flags = self.class_type_indicator()

        # FIXME: delete masking
        return flags & 0x0F

    def volume_name(self):
        start = 1
        binary = self._raw_target[start:]
        text = self.text_processor.read_string(binary)
        return text
