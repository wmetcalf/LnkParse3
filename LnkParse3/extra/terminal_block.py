from struct import unpack
from LnkParse3.extra.lnk_extra_base import LnkExtraBase

"""
------------------------------------------------------------------
|     0-7b     |     8-15b     |     16-23b     |     24-31b     |
------------------------------------------------------------------
|            <u_int32> BlockSignature == 0x00000000              |
------------------------------------------------------------------
|                     extra garbage                              |
------------------------------------------------------------------

"""


class TerminalBlock(LnkExtraBase):
    def name(self):
        return "TERMINAL_BLOCK"

    def terminal_block(self):
        start = 4
        return self.extra_data()

    def extra_data(self):
        start = 4
        return self._raw[start:]

    def as_dict(self):
        tmp = super().as_dict()
        tmp["extra_garbage"] = self.extra_data()
        return tmp

