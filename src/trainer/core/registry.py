from typing import Callable

type ReadMethod = str
type WriteMethod = str
type CastFn = Callable[[object], object]
type RegistryEntry = tuple[ReadMethod, WriteMethod, CastFn]

TYPE_REGISTRY: dict[str, RegistryEntry] = {
    
    "float":        ("read_float",          "write_float",          float),
    "double":       ("read_double",         "write_double",         float),

    "int":          ("read_int",            "write_int",            int),
    "short":        ("read_short",          "write_short",          int),
    "long":         ("read_long",           "write_long",           int),
    "longlong":     ("read_longlong",       "write_longlong",       int),

    "uint":         ("read_uint",           "write_uint",           int),
    "ushort":       ("read_ushort",         "write_ushort",         int),
    "ulong":        ("read_ulong",          "write_ulong",          int),
    "ulonglong":    ("read_ulonglong",      "write_ulonglong",      int),

    "bool":         ("read_bool",           "write_bool",           bool),
    "char":         ("read_char",           "write_char",           bytes),
    "uchar":        ("read_uchar",          "write_uchar",          int),
    "bytes":        ("read_bytes",          "write_bytes",          bytes),

    "int64":        ("read_int",            "write_int",            int),
    "longlong":     ("read_longlong",       "write_longlong",       int),
}