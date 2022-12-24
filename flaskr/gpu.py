from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class GpuType(Tuple[str, int], Enum):
    NVIDIA_GEFORCE_3090 = ("nvidia_geforce_rtx_3090", 24576)
    TITAN_XP = ("titan_xp", 12194)
    NVIDIA_TITAN_XP = ("nvidia_titan_xp", 12288)

    def __init__(self, value: Tuple[str, int]):
        self.label = value[0]
        self.memory = value[1]

    @classmethod
    def gpu_by_label(cls, label: str):
        for item in cls:
            if item.label == label:
                return item
        raise ValueError(f"{label} not found")


@dataclass
class Gpu:
    index: int
    type: GpuType
    memory_occupied: int
    temperature: int
    gpu_utilization: int
