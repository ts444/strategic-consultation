from dataclasses import dataclass


@dataclass
class Violation:
    rule: str
    line: int | None
    message: str
