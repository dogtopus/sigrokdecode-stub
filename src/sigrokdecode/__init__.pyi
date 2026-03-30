from typing import Any, ClassVar, Dict, List, Literal, NotRequired, Protocol, Tuple, TypedDict, Union

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


ChannelList = Tuple[ChannelEntry, ...]


ChannelId = Union[int, str]
ChannelCondition = Literal['h', 'l', 'r', 'f', 'e', 'skip']
Condition = Dict[ChannelId, ChannelCondition]
ConditionList = Union[List[Condition], Condition]


OptionList = Tuple[OptionEntry, ...]
AnnotationList = Tuple[NameDescPair, ...]
AnnotationRowList = Tuple[str, str, Tuple[int, ...]]
BinaryList = Tuple[NameDescPair, ...]


class DecoderHeaderBase(Protocol):
    '''
    Required decoder header fields.

    All decoders must have these fields set.
    '''
    
    api_version: ClassVar[int]
    id: ClassVar[str]
    name: ClassVar[str]
    longname: ClassVar[str]
    desc: ClassVar[str]
    license: ClassVar[str]
    inputs: ClassVar[List[str]]
    outputs: ClassVar[List[str]]
    tags: ClassVar[List[str]]

    def decode(self, start_sample: int, end_sample: int, data: Any) -> None: ...


### BEGIN FRAGS DEFINE
### ('options', 'OptionList')
### ('channels', 'ChannelList')
### ('optional_channels', 'ChannelList')
### ('annotations', 'AnnotationList')
### ('annotation_rows', 'AnnotationRowList')
### ('binary', 'BinaryList')
### END FRAGS DEFINE
### BEGIN FRAGS GENERATED
class DecoderHeaderFrag1(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]


class DecoderHeaderFrag2(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]


class DecoderHeaderFrag3(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]


class DecoderHeaderFrag4(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]


class DecoderHeaderFrag5(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]


class DecoderHeaderFrag6(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]


class DecoderHeaderFrag7(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]


class DecoderHeaderFrag8(DecoderHeaderBase, Protocol):
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag9(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag10(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag11(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag12(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag13(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag14(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag15(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]


class DecoderHeaderFrag16(DecoderHeaderBase, Protocol):
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag17(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag18(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag19(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag20(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag21(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag22(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag23(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag24(DecoderHeaderBase, Protocol):
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag25(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag26(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag27(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag28(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag29(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag30(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag31(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]


class DecoderHeaderFrag32(DecoderHeaderBase, Protocol):
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag33(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag34(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag35(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag36(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag37(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag38(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag39(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag40(DecoderHeaderBase, Protocol):
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag41(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag42(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag43(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag44(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag45(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag46(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag47(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag48(DecoderHeaderBase, Protocol):
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag49(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag50(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag51(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag52(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag53(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag54(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag55(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag56(DecoderHeaderBase, Protocol):
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag57(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag58(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag59(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag60(DecoderHeaderBase, Protocol):
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag61(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag62(DecoderHeaderBase, Protocol):
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


class DecoderHeaderFrag63(DecoderHeaderBase, Protocol):
    options: ClassVar[OptionList]
    channels: ClassVar[ChannelList]
    optional_channels: ClassVar[ChannelList]
    annotations: ClassVar[AnnotationList]
    annotation_rows: ClassVar[AnnotationRowList]
    binary: ClassVar[BinaryList]


DecoderHeader = Union[
    DecoderHeaderBase,
    DecoderHeaderFrag1, DecoderHeaderFrag2, DecoderHeaderFrag3, DecoderHeaderFrag4,
    DecoderHeaderFrag5, DecoderHeaderFrag6, DecoderHeaderFrag7, DecoderHeaderFrag8,
    DecoderHeaderFrag9, DecoderHeaderFrag10, DecoderHeaderFrag11, DecoderHeaderFrag12,
    DecoderHeaderFrag13, DecoderHeaderFrag14, DecoderHeaderFrag15, DecoderHeaderFrag16,
    DecoderHeaderFrag17, DecoderHeaderFrag18, DecoderHeaderFrag19, DecoderHeaderFrag20,
    DecoderHeaderFrag21, DecoderHeaderFrag22, DecoderHeaderFrag23, DecoderHeaderFrag24,
    DecoderHeaderFrag25, DecoderHeaderFrag26, DecoderHeaderFrag27, DecoderHeaderFrag28,
    DecoderHeaderFrag29, DecoderHeaderFrag30, DecoderHeaderFrag31, DecoderHeaderFrag32,
    DecoderHeaderFrag33, DecoderHeaderFrag34, DecoderHeaderFrag35, DecoderHeaderFrag36,
    DecoderHeaderFrag37, DecoderHeaderFrag38, DecoderHeaderFrag39, DecoderHeaderFrag40,
    DecoderHeaderFrag41, DecoderHeaderFrag42, DecoderHeaderFrag43, DecoderHeaderFrag44,
    DecoderHeaderFrag45, DecoderHeaderFrag46, DecoderHeaderFrag47, DecoderHeaderFrag48,
    DecoderHeaderFrag49, DecoderHeaderFrag50, DecoderHeaderFrag51, DecoderHeaderFrag52,
    DecoderHeaderFrag53, DecoderHeaderFrag54, DecoderHeaderFrag55, DecoderHeaderFrag56,
    DecoderHeaderFrag57, DecoderHeaderFrag58, DecoderHeaderFrag59, DecoderHeaderFrag60,
    DecoderHeaderFrag61, DecoderHeaderFrag62, DecoderHeaderFrag63,
]
### END FRAGS GENERATED


class Decoder:
    def put(self, start_sample: int, end_sample: int, output_id: int, data: Any, /) -> None: ...
    def register(self, output_type: int, proto_id: str = ..., meta: Tuple[type[Any], str, str] = ...) -> None: ...
    def wait(self, condition: ConditionList | None) -> None: ...
    def has_channel(self, index: int) -> bool: ...


OUTPUT_ANN: int = ...
OUTPUT_PYTHON: int = ...
OUTPUT_BINARY: int = ...
OUTPUT_LOGIC: int = ...
OUTPUT_META: int = ...
SRD_CONF_SAMPLERATE: int = ...
