import warnings
from struct import unpack_from, error as StructError

from LnkParse3.extension_factory import ExtensionFactory


class ExtensionBlocks:
    def __init__(self, indata=None, cp=None):
        self.cp = cp
        self._raw = indata

        size = unpack_from("<H", self._raw, 0)[0]
        offset = unpack_from("<H", self._raw, size - 2)[0]
        self._raw_blocks = self._raw[offset : size - 2] if offset else None

    def __iter__(self):
        return self._iter()

    def _iter(self):
        rest = self._raw_blocks
        while rest:
            factory = ExtensionFactory(indata=rest)

            size = factory.item_size()
            if not size:
                break

            extension_class = factory.extension_class()
            if extension_class:
                yield extension_class(indata=rest[:size], cp=self.cp)

            rest = rest[size:]

    def as_dict(self):
        res = {}
        for extension in self:
            try:
                res[extension.name()] = extension.as_item()
            except (StructError, ValueError) as e:
                msg = "Error while parsing `%s` (%s)" % (extension.name(), e)
                warnings.warn(msg)
                continue
        return res
