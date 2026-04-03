from abc import abstractmethod
from typing import ClassVar, Dict, Final, Generic, List, Literal, NotRequired, Optional, Protocol, Tuple, TypeAlias, TypedDict, TypeVar, Union, overload


# This is a hack that provides a type that's effectively just int, but different
# enough so type checkers recognize it as something different. The non-hacky way
# would be defining IntEnums for these constants in the C extension and use
# e.g. Literal[OutputType.ANN] instead but that seems hard to manage due to the
# fact that the IntEnum class is implemented in Python.
class _AnnotationConstMarker(int):
    pass


class _PythonConstMarker(int):
    pass


class _BinaryConstMarker(int):
    pass


class _LogicConstMarker(int):
    pass


class _MetaConstMarker(int):
    pass


OUTPUT_ANN: Final[_AnnotationConstMarker] = ...  # cast(_AnnotationConstMarker, 0)
'Output type: Annotation'

OUTPUT_PYTHON: Final[_PythonConstMarker] = ...
'Output type: Custom Python callback'

OUTPUT_BINARY: Final[_BinaryConstMarker] = ...
'Output type: Binary stream'

OUTPUT_LOGIC: Final[_LogicConstMarker] = ...
'Output type: Logic'

OUTPUT_META: Final[_MetaConstMarker] = ...
'Output type: Extra metadata from the decoder'

SRD_CONF_SAMPLERATE: Final[int] = ...
'libsigrokdecode metadata type: Capture samplerate'


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


OutputTypeAnnotation: TypeAlias = _AnnotationConstMarker
OutputTypePython: TypeAlias = _PythonConstMarker
OutputTypeBinary: TypeAlias = _BinaryConstMarker
OutputTypeLogic: TypeAlias = _LogicConstMarker
OutputTypeMeta: TypeAlias = _MetaConstMarker


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


class Decoder(Generic[OPT], Protocol):
    '''
    The decoder abstract class. All decoders shall be built upon this class and
    implement all abstract methods.

    The OPT type variable can be used to specify the output type of Python
    callback initiated by the put() method.

    Note that Python type checkers do not enforce concrete classes during
    declaration, only on instantiation. Therefore one needs to instantiate
    the resulting decoder (preferably wrapped in TYPE_CHECKING) to ensure
    that all required attributes and methods are present in the final decoder
    class.
    '''

    api_version: ClassVar[int]
    'API version. Should be 3 for all modern decoders.'

    id: ClassVar[str]
    'Decoder ID.'

    name: ClassVar[str]
    'Short display name of the decoder.'

    longname: ClassVar[str]
    'Long display name of the decoder.'

    desc: ClassVar[str]
    'Decoder description.'

    license: ClassVar[str]
    'Decoder code license.'

    inputs: ClassVar[List[str]]
    'List of inputs.'

    outputs: ClassVar[List[str]]
    'List of outputs.'

    tags: ClassVar[List[str]]
    '''
    Decoder category tags. See libsigrokdecode/HACKING for a list of known
    tags.
    '''

    matched: Optional[Tuple[int, ...]]
    'Input channel match state.'

    samplenum: int
    'Input sample offset'

    # Bad sigrok, very bad sigrok
    #options: OptionValues

    # TODO: data is typed as Any for now, but we may switch to a int+Generic
    # setup that allows data to be typed as long as the user passes something
    # returned by register() into output_id.
    # (Not possible due to sigrokdecode enforcing list tuples as the only type
    # that can be taken by data, we can use list[Any] or list[GVariantBridge]
    # but such type hints are not precise enough to be worthwhile. Mypy plugin
    # won't work on Pyright on VSCode and on whatever JB uses on their IDEs.)
    @overload
    def put(self, start_sample: int, end_sample: int, output_id: AnnotationStream, data: ClassDescPair, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: PythonStream, data: OPT, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: BinaryStream, data: ClassDescPair, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: LogicStream, data: ClassDescPair, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: MetaStream, data: float, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def register(self, output_type: OutputTypeAnnotation, /, proto_id: str = ...) -> AnnotationStream:
        '''
        Register a new annotation output stream.

        Returns an output stream ID that can be used later with put().
        '''
        ...

    @overload
    def register(self, output_type: OutputTypePython, /, proto_id: str = ...) -> PythonStream:
        '''
        Register a new Python (stacked decoder callback) output stream.

        Returns an output stream ID that can be used later with put().
        '''
        ...

    @overload
    def register(self, output_type: OutputTypeBinary, /, proto_id: str = ...) -> BinaryStream:
        '''
        Register a new binary output stream.
        
        Returns an output stream ID that can be used later with put().
        '''
        ...

    @overload
    def register(self, output_type: OutputTypeLogic, /, proto_id: str = ...) -> LogicStream:
        '''
        Register a new logic output stream.

        Returns an output stream ID that can be used later with put().
        '''
        ...

    @overload
    def register(self, output_type: OutputTypeMeta, /, proto_id: str = ..., meta: Tuple[type[float], str, str] = ...) -> MetaStream:
        '''
        Register a new metadata output stream.

        An argument named meta needs to be specified that has the format of
        (type, name, desc). type must be either int or float, and name/desc
        are strings.

        Note that Python type checker does not differentiate int and float
        enough like sigrokdecode would. It treats float as a Union of both
        int and the actual float type. Therefore one still needs to be careful
        not to pass the wrong type when invoking put(). Anything too wrong
        however (e.g. passing a str as data) can be caught automatically by
        the type checker.

        Returns an output stream ID that can be used later with put().
        '''
        ...

    def wait(self, condition: Optional[ConditionList], /) -> Optional[Tuple[int, ...]]:
        '''
        Wait for one or more conditions to occur.

        Returns the sample data at the next position where the condition
        is seen. When the optional condition is missing or empty, the next
        sample number is used. The condition can be a dictionary with one
        condition's details, or a list of dictionaries specifying multiple
        conditions of which at least one condition must be true. Dicts can
        contain one or more key/value pairs, all of which must be true for
        the dict's condition to be considered true. The key either is a
        channel index or a keyword, the value is the operation's parameter.

        Supported parameters for channel number keys: 'h', 'l', 'r', 'f',
        or 'e' for level or edge conditions. Other supported keywords:
        'skip' to advance over the given number of samples.
        '''
        ...

    def has_channel(self, index: int, /) -> bool:
        '''
        Check whether input data is supplied for a given channel.

        Argument: A channel index.
        Returns: A boolean, True if the channel is connected,
        False if the channel is open (won't see any input data).
        '''
        ...

    @abstractmethod
    def start(self) -> None:
        '''
        Prepare the decoder after initialization. Generally things like
        registering the output channels should be done here.
        '''
        ...


class AsBottom(Protocol):
    '''
    Decoder is at the bottom of the decoder stack.
    '''
    @abstractmethod
    def decode(self, /) -> None:
        '''
        Process decoder request from libsigrokdecode.
        '''
        ...


class AsStacked(Generic[IPT], Protocol):
    '''
    Decoder is on top of other decoder(s).
    '''
    @abstractmethod
    def decode(self, start_sample: int, end_sample: int, data: IPT, /) -> None:
        '''
        Process custom decode request from other decoders.
        '''
        ...


class BottomDecoder(Generic[OPT], Decoder[OPT], AsBottom, Protocol):
    '''
    Base class for a bottom decoder.
    '''
    pass


class StackedDecoder(Generic[IPT, OPT], Decoder[OPT], AsStacked[IPT], Protocol):
    '''
    Base class for a stacked decoder.
    '''
    pass


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


class SupportsFlush(Protocol):
    '''
    Decoder class supports handling the flush event from libsigrok.
    '''
    @abstractmethod
    def flush(self) -> None:
        '''
        Handle the flush event from libsigrokdecode.
        '''
        ...


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
        ...


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
        ...
