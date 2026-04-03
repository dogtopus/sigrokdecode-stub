'''
sigrokdecode wrapper module
'''


try:
    _srd = __import__('sigrokdecode')
except ModuleNotFoundError:
    from . import _runtime_stub as _srd


Decoder = _srd.Decoder
OUTPUT_ANN = _srd.OUTPUT_ANN
OUTPUT_PYTHON = _srd.OUTPUT_PYTHON
OUTPUT_BINARY = _srd.OUTPUT_BINARY
OUTPUT_LOGIC = _srd.OUTPUT_LOGIC
OUTPUT_META = _srd.OUTPUT_META
SRD_CONF_SAMPLERATE = _srd.SRD_CONF_SAMPLERATE

# Satisfy runtime requirement
BottomDecoder = StackedDecoder = Decoder

from .typing import *
