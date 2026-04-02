from abc import abstractmethod
from typing import Any, ClassVar, Dict, List, Literal, NotRequired, Optional, Protocol, Tuple, TypeAlias, TypedDict, Union


GVariantBridge: TypeAlias = Union[int, float, str]


class OptionEntry(TypedDict):
    id: str
    desc: NotRequired[str]
    default: NotRequired[GVariantBridge]
    values: NotRequired[Tuple[GVariantBridge, ...]]


class ChannelEntry(TypedDict):
    id: str
    name: str
    desc: str


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


OptionValues: TypeAlias = Dict[str, GVariantBridge]
'''
Option values on an instantiated decoder object.

Python does not allow typing class variables and instance variables as
unrelated types, so to type the instance variable on access, manual casting
is required:

>>> instance_options = cast(OptionValues, self.options)
>>> reveal_type(instance_options)
'''


class Decoder(Protocol):
    '''
    The decoder abstract class. All decoders shall be built upon this class and
    implement all abstract methods.
    
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
    def put(self, start_sample: int, end_sample: int, output_id: int, data: Any, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    def register(self, output_type: int, /, proto_id: str = ..., meta: Tuple[Union[int, float], str, str] = ...) -> int:
        '''
        Register a new output stream.
        
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


class AsStacked(Protocol):
    '''
    Decoder is on top of other decoder(s).
    '''
    @abstractmethod
    def decode(self, start_sample: int, end_sample: int, data: Any, /) -> None:
        '''
        Process custom decode request from other decoders.
        '''
        ...


class BottomDecoder(Decoder, AsBottom, Protocol):
    '''
    Base class for a bottom decoder.
    '''
    pass


class StackedDecoder(Decoder, AsStacked, Protocol):
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
    Mark the decoder as that it provides annotation row ("channel")
    descriptions.
    '''
    annotation_rows: ClassVar[AnnotationRowList]


class HasBinary(Protocol):
    '''
    Mark the decoder as that it provides binary stream ("channel")
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


OUTPUT_ANN: int = ...
'Output type: Annotation'

OUTPUT_PYTHON: int = ...
'Output type: Custom Python callback'

OUTPUT_BINARY: int = ...
'Output type: Binary stream'

OUTPUT_LOGIC: int = ...
'Output type: Logic'

OUTPUT_META: int = ...
'Output type: Extra metadata from the decoder'

SRD_CONF_SAMPLERATE: int = ...
'libsigrokdecode metadata type: Capture samplerate'
