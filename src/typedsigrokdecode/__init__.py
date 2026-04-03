'''
sigrokdecode wrapper module
'''

from .typing import *

try:
    _srd = __import__('sigrokdecode')
except ModuleNotFoundError:
    from . import _runtime_stub as _srd


OUTPUT_ANN = _srd.OUTPUT_ANN
OUTPUT_PYTHON = _srd.OUTPUT_PYTHON
OUTPUT_BINARY = _srd.OUTPUT_BINARY
OUTPUT_LOGIC = _srd.OUTPUT_LOGIC
OUTPUT_META = _srd.OUTPUT_META
SRD_CONF_SAMPLERATE = _srd.SRD_CONF_SAMPLERATE


# Do the bare minimum to satisfy runtime requirement
class AbstractDecoder(Generic[OPT], _srd.Decoder):
    # Ensure these are always readable
    matched = None
    samplenum = 0

    def get_options(self):
        return self.options


class BottomDecoder(Generic[OPT], AbstractDecoder[OPT]):
    pass


class StackedDecoder(Generic[IPT, OPT], AbstractDecoder[OPT]):
    pass
