from enum import Enum, unique


@unique
class StelaFileType(Enum):
    INI = [".ini"]
    JSON = [".json"]
    YAML = [".yaml", ".yml"]
    TOML = [".toml"]
