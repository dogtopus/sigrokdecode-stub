'''
Typing-specific objects.
'''

from abc import abstractmethod
from typing import ClassVar, Dict, Generic, List, Literal, NotRequired, Protocol, Tuple, TypeAlias, TypedDict, TypeVar, Union


# This is a hack that provides a type that's effectively just int, but different
# enough so type checkers recognize it as something different. The non-hacky way
# would be defining IntEnums for these constants in the C extension and use
# e.g. Literal[OutputType.ANN] instead but that seems hard to manage due to the
# fact that the IntEnum class is implemented in Python.
class AnnotationConstMarker(int):
    pass


class PythonConstMarker(int):
    pass


class BinaryConstMarker(int):
    pass


class LogicConstMarker(int):
    pass


class MetaConstMarker(int):
    pass


GVariantBridge: TypeAlias = Union[float, str]


class OptionEntry(TypedDict):
    id: str
    desc: NotRequired[str]
    default: NotRequired[GVariantBridge]
    values: NotRequired[Tuple[GVariantBridge, ...]]


class ChannelEntry(TypedDict):
    id: str
    name: str
    desc: str


ClassDescPair: TypeAlias = Tuple[int, str]
NameDescPair: TypeAlias = Tuple[str, str]
NameDescClasses: TypeAlias = Tuple[str, str, Tuple[int, ...]]
ChannelId: TypeAlias = Union[int, str]
ChannelCondition: TypeAlias = Literal['h', 'l', 'r', 'f', 'e', 'skip']


Condition: TypeAlias = Dict[ChannelId, ChannelCondition]
ConditionList: TypeAlias = Union[List[Condition], Condition]


OptionList: TypeAlias = Tuple[OptionEntry, ...]
ChannelList: TypeAlias = Tuple[ChannelEntry, ...]
NameDescList: TypeAlias = Tuple[NameDescPair, ...]
AnnotationRowList: TypeAlias = Tuple[NameDescClasses, ...]


OutputTypeAnnotation: TypeAlias = AnnotationConstMarker
OutputTypePython: TypeAlias = PythonConstMarker
OutputTypeBinary: TypeAlias = BinaryConstMarker
OutputTypeLogic: TypeAlias = LogicConstMarker
OutputTypeMeta: TypeAlias = MetaConstMarker


# Same as above in concept but these aren't hacks.
class AnnotationStream(int):
    pass


class PythonStream(int):
    pass


class BinaryStream(int):
    pass


class LogicStream(int):
    pass


class MetaStream(int):
    pass


OptionValues: TypeAlias = Dict[str, GVariantBridge]
'''
Option values on an instantiated decoder object.

Python does not allow typing class variables and instance variables as
unrelated types, so to type the instance variable on access, manual casting
is required:

>>> instance_options = cast(OptionValues, self.options)
>>> reveal_type(instance_options)
'''


IPT = TypeVar('IPT', contravariant=True)
'Input Python type'
OPT = TypeVar('OPT', contravariant=True)
'Output Python type'


class AsBottom(Protocol):
    '''
    Decoder is at the bottom of the decoder stack.
    '''
    @abstractmethod
    def decode(self, /) -> None:
        '''
        Process decoder request from libsigrokdecode.
        '''
        raise NotImplementedError()


class AsStacked(Generic[IPT], Protocol):
    '''
    Decoder is on top of other decoder(s).
    '''
    @abstractmethod
    def decode(self, start_sample: int, end_sample: int, data: IPT, /) -> None:
        '''
        Process custom decode request from other decoders.
        '''
        raise NotImplementedError()


class HasOptions(Protocol):
    '''
    Mark the decoder as that it provides custom options.
    '''
    options: ClassVar[OptionList]


class HasChannels(Protocol):
    '''
    Mark the decoder as that it provides output channel descriptions.
    '''
    channels: ClassVar[ChannelList]


class HasOptionalChannels(Protocol):
    '''
    Mark the decoder as that it provides optional output channel descriptions.
    '''
    optional_channels: ClassVar[ChannelList]


class HasAnnotations(Protocol):
    '''
    Mark the decoder as that it provides annotation type mappings.
    '''
    annotations: ClassVar[NameDescList]


class HasAnnotationRows(Protocol):
    '''
    Mark the decoder as that it provides annotation row
    descriptions.
    '''
    annotation_rows: ClassVar[AnnotationRowList]


class HasBinary(Protocol):
    '''
    Mark the decoder as that it provides binary stream row
    descriptions.
    '''
    binary: ClassVar[NameDescList]


class HasLogicOutputChannels(Protocol):
    '''
    Mark the decoder as that it provides logic output channel
    descriptions.
    '''
    logic_output_channels: ClassVar[NameDescList]


class SupportsFlush(Protocol):
    '''
    Decoder class supports handling the flush event from libsigrok.
    '''
    @abstractmethod
    def flush(self) -> None:
        '''
        Handle the flush event from libsigrokdecode.
        '''
        raise NotImplementedError()


class SupportsReset(Protocol):
    '''
    Decoder class supports handling the reset event from libsigrok.
    '''
    @abstractmethod
    def reset(self) -> None:
        '''
        Handle the reset event from libsigrokdecode.

        The implementation shall reset the protocol decoder to its initial
        state.
        '''
        raise NotImplementedError()


class SupportsMetadata(Protocol):
    '''
    Decoder class supports receiving metadata from libsigrok.
    '''
    @abstractmethod
    def metadata(self, key: int, value: int) -> None:
        '''
        Receive metadata sent over by libsigrokdecode.

        Currently the only key that is supported is SRD_CONF_SAMPLERATE,
        which indicates the capture sample rate.
        '''
        raise NotImplementedError()
