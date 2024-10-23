from struct import unpack
from LnkParse3.target.lnk_target_base import LnkTargetBase
from LnkParse3.extension_blocks import ExtensionBlocks
from LnkParse3.extension.file_entry import FileEntry
from LnkParse3.decorators import dostime

"""
----------------------------------------------------------------------
|              0-7b              |               8-15b               |
----------------------------------------------------------------------
| ClassTypeIndicator == 0x30-0x3F|            UnknownValue           |
----------------------------------------------------------------------
|                        <u_int16> FileSize                          |
|                              4 B                                   |
----------------------------------------------------------------------
|           <dos_timestamp> LastModificationDateAndTime              |
|                              4 B                                   |
----------------------------------------------------------------------
|                       FileAttributeFlags                           |
----------------------------------------------------------------------
|                 <str/unicode_str> PrimaryName                      |
|                              ? B                                   |
----------------------------------------------------------------------
|                           UnknownData                              |
|                              ? B                                   |
----------------------------------------------------------------------
"""


# TODO: rename to file_entry
# https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#34-file-entry-shell-item
class ShellFSFolder(LnkTargetBase):
    def __init__(self, *args, **kwargs):
        self.name = "File entry"
        super().__init__(*args, **kwargs)
        self._extensions = None

    def extensions(self):
        if self._extensions is None:
            self._extensions = ExtensionBlocks(indata=self._raw, cp=self.cp).as_dict()

        return self._extensions

    def as_item(self):
        item = super().as_item()
        try:
            item["flags"] = self.flags()
            item["file_size"] = self.file_size()
            creation_time = self.creation_time()
            if creation_time:
                item["creation_time"] = self.creation_time()
            item["modification_time"] = self.modification_time()
            last_access_time = self.last_access_time()
            if last_access_time:
                item["last_access_time"] = self.last_access_time()
            item["file_attribute_flags"] = self.file_attribute_flags()
            item["primary_name"] = self.primary_name()
            secondary_name = self.secondary_name()
            if secondary_name:
                item["secondary_name"] = secondary_name
        except KeyError:
            # FIXME This try-catch is just a hot-fix.
            # We should probably solve failing attributes in a better way.
            pass
        return item

    # dup: ./my_computer.py flags()
    # dup: ../target_factory.py item_type()
    def flags(self):
        flags = self.class_type_indicator()

        # FIXME: delete masking
        return self.SHELL_ITEM_SHEL_FS_FOLDER[flags & 0x0F]

    def file_size(self):
        start, end = 2, 6
        size = unpack("<I", self._raw_target[start:end])[0]
        return size

    @dostime
    def modification_time(self):
        start, end = 6, 10
        return self._raw_target[start:end]

    def file_attribute_flags(self):
        start, end = 10, 12
        flags = unpack("<H", self._raw_target[start:end])[0]
        return flags

    def primary_name(self):
        start = 12
        binary = self._raw_target[start:]

        if self.has_unicode_strings():
            text = self.text_processor.read_unicode_string(binary)
        else:
            text = self.text_processor.read_string(binary)

        return text

    # https://github.com/libyal/libfwsi/blob/master/documentation/Windows%20Shell%20Item%20format.asciidoc#341-file-entry-shell-item--pre-windows-xp
    def secondary_name(self):
        file_entry = self.extensions().get(FileEntry.name())
        if not file_entry:
            return None

        return file_entry.get("long_name")

    def creation_time(self):
        file_entry = self.extensions().get(FileEntry.name())
        if not file_entry:
            return None

        return file_entry.get("creation_time")

    def last_access_time(self):
        file_entry = self.extensions().get(FileEntry.name())
        if not file_entry:
            return None

        return file_entry.get("last_access_time")

    def shell_folder_identifier(self):
        # TODO:
        pass
