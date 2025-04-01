from dataclasses import dataclass, field


@dataclass
class ScanMask:
    points: list[tuple[int, int]] = field(default_factory=list)
