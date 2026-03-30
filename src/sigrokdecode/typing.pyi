from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import DecoderHeader

def validate_decoder_header(d: 'type[DecoderHeader]'): ...
