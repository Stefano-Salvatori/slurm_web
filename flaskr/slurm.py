from dataclasses import dataclass
import dataclasses
from enum import Enum
from typing import Dict, List, Tuple
import json
import os
import re

from flaskr.command_executor import CommandExecutor


class GpuType(Tuple[str, int], Enum):
    NVIDIA_GEFORCE_3090 = ("nvidia_geforce_rtx_3090", 24)
    TITAN_XP = ("titan_xp", 12)

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
class Job:
    id: int
    user: str
    task_name: str
    state: str
    time: str
    num_nodes: int
    nodes: List[str]
    gpu_indices: List[int] = None

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))


@dataclass
class Node:
    ip: str
    name: str
    cpus: int
    gpus: Dict[GpuType, int]
    allocated_jobs: List[Job]


class Slurm:
    def __init__(self) -> None:
        self.command_executor = CommandExecutor()

    def cluster_nodes(self):
        nodes_info = self.command_executor.execute(
            "sinfo --Format=NodeAddr,NodeHost:38,CPUs:10,Gres:35 --noheader"
        ).split(os.linesep)
        jobs = self.get_jobs()
        nodes = []
        for node in nodes_info:
            if len(node) > 0:
                ip, hostname, cpus, gpu_info = node.split()
                regex = re.compile("gpu:(\w+):(\d)").search(gpu_info)
                gpu_type = GpuType.gpu_by_label(regex.group(1))
                gpu_number = int(regex.group(2))
                node = Node(
                    ip=ip,
                    name=hostname,
                    cpus=cpus,
                    gpus={gpu_type.name: gpu_number},
                    allocated_jobs=[j for j in jobs if hostname in j.nodes],
                )
                nodes.append(node)

        return nodes

    def gpu_of_job(self, job_id: int) -> int:
        res = self.command_executor.execute(f"scontrol show jobid -d {job_id} | grep GRES")
        regex = re.compile("\sGRES=gpu:\w*:\d\(IDX:(\d)\)")
        idx = regex.search(res).group(1)
        return int(idx)

    def get_jobs(self) -> List[Job]:
        tasks = self.command_executor.execute(
            "squeue --Format=JobID,Name,UserName:35,State,TimeUsed,NumNodes,NodeList --noheader"
        ).split(os.linesep)
        jobs_list = []
        for task_string in tasks:
            fields = task_string.split()
            if len(fields) > 0:
                gpu_index = self.gpu_of_job(fields[0])
                jobs_list.append(
                    Job(
                        id=fields[0],
                        user=fields[2],
                        task_name=fields[1],
                        state=fields[3],
                        time=fields[4],
                        num_nodes=int(fields[5]),
                        nodes=[fields[6]],
                        gpu_indices=[gpu_index],
                    )
                )
        return jobs_list

