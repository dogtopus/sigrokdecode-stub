from abc import abstractmethod
from typing import ClassVar, Final, Generic, List, Optional, Protocol, Tuple, overload
from .typing import *


OUTPUT_ANN: Final[AnnotationConstMarker] = ...  # cast(_AnnotationConstMarker, 0)
'Output type: Annotation'

OUTPUT_PYTHON: Final[PythonConstMarker] = ...
'Output type: Custom Python callback'

OUTPUT_BINARY: Final[BinaryConstMarker] = ...
'Output type: Binary stream'

OUTPUT_LOGIC: Final[LogicConstMarker] = ...
'Output type: Logic'

OUTPUT_META: Final[MetaConstMarker] = ...
'Output type: Extra metadata from the decoder'

SRD_CONF_SAMPLERATE: Final[int] = ...
'libsigrokdecode metadata type: Capture samplerate'


class AbstractDecoder(Generic[OPT], Protocol):
    '''
    The decoder abstract class. All decoders shall be built upon this class and
    implement all abstract methods.

    The OPT type variable can be used to specify the type of message sent with
    the put() method.

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

    matched: Optional[Tuple[bool, ...]] = ...
    '''
    Wait condition match state. Length is the same as the ConditionList last
    passed to wait() method.
    '''

    samplenum: int = ...
    'Current absolute input sample offset.'

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: AnnotationStream, data: ClassAnnotationPair, /) -> None:
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
    def put(self, start_sample: int, end_sample: int, output_id: BinaryStream, data: ClassBytesPair, /) -> None:
        '''
        Put an annotation for the specified span of samples.

        Arguments: start and end sample number, stream id, annotation data.
        Annotation data's layout depends on the output stream type.
        '''
        ...

    @overload
    def put(self, start_sample: int, end_sample: int, output_id: LogicStream, data: ClassBytesPair, /) -> None:
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

    def wait(self, condition: Optional[ConditionList]) -> Optional[Tuple[int, ...]]:
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

    def get_options(self) -> OptionMap:
        '''
        Read decoder instance option map and cast it appropriately.

        This method is specific to typedsigrokdecode. It is equivalent to
        accessing self.options in an untyped sigrokdecode decoder instance.
        '''
        ...

    @abstractmethod
    def start(self) -> None:
        '''
        Prepare the decoder after initialization. Generally things like
        registering the output channels and parsing of instance options
        should be done here.
        '''
        ...

    @abstractmethod
    def reset(self) -> None:
        '''
        Handle the reset event from libsigrokdecode.

        The implementation shall reset the protocol decoder to its initial
        state.
        '''
        ...


class BottomDecoder(Generic[OPT], AbstractDecoder[OPT], AsBottom, Protocol):
    '''
    Abstract class of a bottom (non-stacked) decoder.

    The OPT type variable can be used to specify the type of message sent with
    the put() method.

    The same limitation on concrete class handling also applies to this class.
    '''
    pass


class StackedDecoder(Generic[IPT, OPT], AbstractDecoder[OPT], AsStacked[IPT], Protocol):
    '''
    Abstract class of a stacked decoder.

    The IPT type variable can be used to specify the type of the data received
    through the decode() method that was previously sent from other decoders
    via put(), and the OPT type variable can be used to specify the type of
    message sent with the put() method.

    The same limitation on concrete class handling also applies to this class.
    '''
    pass
