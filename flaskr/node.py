from dataclasses import dataclass, field
from typing import List, Tuple
import re

from flaskr.slurm import Job
from .gpu import GpuType


@dataclass
class Node:
    architecture: str = "",
    burstbuffer_network_address: str = "",
    boards: int = 0,
    boot_time: int = 0,
    comment: str = "",
    cores: int = 0,
    cpu_binding: int = 0,
    cpu_load: int = 0,
    extra: str = "",
    free_memory: int = 0,
    cpus: int = 0,
    last_busy: int = 0,
    features:str = "",
    active_features:str = "",
    gres:str = "",
    gres_drained:str = "",
    gres_used:str = "",
    mcs_label:str = "",
    name:str = "",
    next_state_after_reboot:str = "",
    address:str = "",
    hostname:str = "",
    state:str = "",
    state_flags: list = field(default_factory=list),
    next_state_after_reboot_flags: list = field(default_factory=list),
    operating_system: str = "",
    owner:str = None,
    partitions:list = field(default_factory=list),
    port: int = 0,
    real_memory: int = 0,
    reason:str = "",
    reason_changed_at:int = 0,
    reason_set_by_user:str = None,
    slurmd_start_time:int = 0,
    sockets:int = 0,
    threads:int = 0,
    temporary_disk:int = 0,
    weight:int = 1,
    tres:str = "",
    slurmd_version:int = "",
    alloc_memory: int = 0,
    alloc_cpus: int = 0,
    idle_cpus: int = 0,
    tres_used:str = "",
    tres_weighted:int = 16
    allocated_jobs: List[Job] = field(default_factory=list)

    @property
    def gpus(self):
        regex = re.compile("gpu:(\w+):(\d)").search(self.gres)
        gpu_type = GpuType.gpu_by_label(regex.group(1))
        gpu_number = int(regex.group(2))
        return {gpu_type.name: gpu_number}

    def splitted_ip(self) -> Tuple[int, int, int, int]:
        return tuple(int(part) for part in self.address.split("."))

    def __hash__(self) -> int:
        return hash(self.address)