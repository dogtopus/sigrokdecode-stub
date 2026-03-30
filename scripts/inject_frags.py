# AI slop

import sys

from ast import literal_eval
from itertools import zip_longest
from io import StringIO
from pathlib import Path
from typing import List, Tuple


BEGIN_MARKER = '### BEGIN FRAGS GENERATED'
END_MARKER = '### END FRAGS GENERATED'
BEGIN_MARKER_DEFINE = '### BEGIN FRAGS DEFINE'
END_MARKER_DEFINE = '### END FRAGS DEFINE'


def grouper(iterable, n):
    iterators = [iter(iterable)] * n
    return zip_longest(*iterators, fillvalue=None)


def gen_frags(out: StringIO, table: List[Tuple[str, str]]):
    for i in range(1, 2**len(table)):
        out.write(f'class DecoderHeaderFrag{i}(DecoderHeaderBase, Protocol):\n')
        n = 0
        while i != 0:
            if i & 1 == 1:
                b = table[n]
                out.write(f'    {b[0]}: ClassVar[{b[1]}]\n')
            i >>= 1
            n += 1
        out.write('\n\n')


def gen_union(out: StringIO, table: List[Tuple[str, str]]):
    out.write('DecoderHeader = Union[\n    DecoderHeaderBase,\n')
    for group in grouper(range(1, 2**len(table)), 4):
        line = ', '.join(f'DecoderHeaderFrag{i}' for i in group if i is not None)
        out.write(f'    {line},\n')
    out.write(']')


def inject_frags(file_path: str) -> None:
    buffer = StringIO()

    path = Path(file_path)
    text = path.read_text(encoding='utf-8')

    table_begin = text.find(BEGIN_MARKER_DEFINE)
    table_end = text.find(END_MARKER_DEFINE)

    if table_begin == -1 or table_end == -1:
        raise ValueError('Could not find both DEFINE markers.')
    if table_begin > table_end:
        raise ValueError('BEGIN marker appears after END marker.')

    table: List[Tuple[str, str]] = []
    define = text[table_begin + len(BEGIN_MARKER_DEFINE):table_end]
    for line in define.split('\n'):
        if line.startswith('###'):
            table.append(literal_eval(line[3:].strip()))

    gen_frags(buffer, table)
    gen_union(buffer, table)

    begin = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)

    if begin == -1 or end == -1:
        raise ValueError('Could not find both GENERATED markers.')
    if begin > end:
        raise ValueError('BEGIN marker appears after END marker.')

    before = text[:begin + len(BEGIN_MARKER)]
    after = text[end:]

    path.write_text(f"{before}\n{buffer.getvalue().rstrip()}\n{after}", encoding='utf-8')


if __name__ == '__main__':
    inject_frags(sys.argv[1])
