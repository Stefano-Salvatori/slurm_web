from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Tuple
import re
from flaskr.command_executor import CommandExecutor


class GpuType(Tuple[str, int], Enum):
    NVIDIA_GEFORCE_3090 = ("nvidia_geforce_rtx_3090", 24576)
    TITAN_XP = ("titan_xp", 12194)

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


@dataclass
class Job:
    id: int
    user: str
    task_name: str
    state: str
    time: str
    num_nodes: int
    nodes: List[str]
    gpu_indices: List[int] = None


@dataclass
class Node:
    ip: str
    hostname: str
    cpus: int
    gpus: Dict[GpuType, int]
    allocated_jobs: List[Job] = field(default_factory=list)

    def splitted_ip(self) -> Tuple[int, int, int, int]:
        return tuple(int(part) for part in self.ip.split("."))

    def __hash__(self) -> int:
        return hash(self.ip)


class Slurm:
    def __init__(self) -> None:
        self.command_executor = CommandExecutor()

    def num_nodes(self):
        return int(self.command_executor.execute("sinfo --Format=Nodes --noheader"))

    def cluster_nodes(self) -> List[Node]:
        def _parse_nodes_info(command_output_lines: List[str]):
            nodes = []
            for node in command_output_lines:
                ip, hostname, cpus, gpu_info = node.split()
                regex = re.compile("gpu:(\w+):(\d)").search(gpu_info)
                gpu_type = GpuType.gpu_by_label(regex.group(1))
                gpu_number = int(regex.group(2))
                nodes.append(Node(ip=ip, hostname=hostname, cpus=cpus, gpus={gpu_type.name: gpu_number},))
            return nodes

        nodes_info = self.command_executor.execute(
            "sinfo --Format=NodeAddr,NodeHost:50,CPUs:10,Gres:50 --noheader", split_new_lines=True
        )

        return _parse_nodes_info(nodes_info)

    def gpu_of_job(self, job_id: int) -> List[int]:
        def _parse_gpu(command_output: str):
            return re.compile("\sGRES=gpu:\w*:\d\(IDX:(\d)(-(\d))*\)").search(command_output)

        res = self.command_executor.execute(f"scontrol show jobid -d {job_id} | grep GRES")
        parsed = _parse_gpu(res)
        return [int(g) for g in parsed.groups()[::2] if g is not None] if parsed is not None else []

    def get_jobs(self) -> List[Job]:
        def _parse_jobs(command_output_lines: List[str]):
            jobs_list = []
            for task_string in command_output_lines:
                fields = task_string.split()
                gpu_indices = self.gpu_of_job(fields[0])
                jobs_list.append(
                    Job(
                        id=fields[0],
                        user=fields[2],
                        task_name=fields[1],
                        state=fields[3],
                        time=fields[4],
                        num_nodes=int(fields[5]),
                        nodes=[fields[6]] if len(fields) >= 7 else [],
                        gpu_indices=gpu_indices,
                    )
                )
            return jobs_list

        command_output = self.command_executor.execute(
            "squeue --Format=JobID,Name:50,UserName:50,State,TimeUsed,NumNodes,NodeList:50 --noheader",
            split_new_lines=True,
        )
        return _parse_jobs(command_output)

    def gpu_stats(self, node_hostname: str) -> List[Gpu]:
        def _parse_gpu_stats(command_output_lines: List[str]):
            gpus = []
            for g in command_output_lines:
                gpu_index, gpu_temp, gpu_mem, gpu_name = g.strip().split(",")
                gpus.append(
                    Gpu(
                        index=int(gpu_index),
                        type=GpuType.gpu_by_label(gpu_name.lstrip().replace(" ", "_").lower()),
                        memory_occupied=int(gpu_mem),
                        temperature=int(gpu_temp),
                    )
                )
            return gpus

        gpu_stats = self.command_executor.execute(
            f"srun -w {node_hostname} --priority='TOP' -D /tmp -c 1 nvidia-smi --query-gpu=index,temperature.gpu,memory.used,gpu_name --format=csv,noheader,nounits",
            split_new_lines=True,
        )
        return _parse_gpu_stats(gpu_stats)

    def all_gpu_stats(self) -> Dict[str, List[Gpu]]:
        return {node.ip: self.gpu_stats(node.hostname) for node in self.cluster_nodes()}
