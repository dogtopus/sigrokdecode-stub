from abc import abstractmethod
from typing import Any, ClassVar, Dict, List, Literal, NotRequired, Optional, Protocol, Tuple, TypeAlias, TypedDict, Union


'''
sigrokdecode module
'''


GVariantBridge = Union[int, float, str]
NameDescPair = Tuple[str, str]


class OptionEntry(TypedDict):
    id: str
    desc: NotRequired[str]
    default: NotRequired[GVariantBridge]
    values: NotRequired[Tuple[GVariantBridge, ...]]


class ChannelEntry(TypedDict):
    id: str
    name: str
    desc: str


ChannelList: TypeAlias = Tuple[ChannelEntry, ...]

ChannelId: TypeAlias = Union[int, str]
ChannelCondition: TypeAlias = Literal['h', 'l', 'r', 'f', 'e', 'skip']
Condition: TypeAlias = Dict[ChannelId, ChannelCondition]
ConditionList: TypeAlias = Union[List[Condition], Condition]


OptionList: TypeAlias = Tuple[OptionEntry, ...]
NameDescList: TypeAlias = Tuple[NameDescPair, ...]
AnnotationRowList: TypeAlias = Tuple[str, str, Tuple[int, ...]]


class Decoder(Protocol):
    '''
    The decoder abstract class.

    Decoder supports
    '''

    api_version: ClassVar[int]
    'API version.'

    id: ClassVar[str]
    'Decoder ID.'

    name: ClassVar[str]
    'Display name of the decoder.'

    longname: ClassVar[str]
    'Display name of the decoder but longer.'

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

    # TODO: data is typed as Any for now, but we may switch to a int+Generic
    # setup that allows data to be typed as long as the user passes something
    # returned by register() into output_id.
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

    # Not defined in Decoder class, but are necessary for the decoder to function.
    @abstractmethod
    def decode(self, start_sample: int, end_sample: int, data: Any, /) -> None: ...

    @abstractmethod
    def start(self) -> None:
        '''
        Prepare the decoder after initialization. Generally things like
        registering the output channels should be done here.
        '''
        ...


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
