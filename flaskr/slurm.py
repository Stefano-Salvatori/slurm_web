from typing import Dict, List
import re
from flaskr.command_executor import CommandExecutor
from .job import Job
from .node import Node
from .gpu import GpuType, Gpu
from threading import Timer
import json


class Slurm:
    def __init__(self, gpu_state_interval: float = 5) -> None:
        """_summary_

        Args:
            gpu_state_interval (float, optional): Time interval (in seconds) between each gpu state update. Defaults to 5.
        """
        self.command_executor = CommandExecutor()
        self.gpu_state_interval = gpu_state_interval
        self.__periodic_update_gpu_stats()
        self.slurm_version = self.__slurm_version()

    def get_nodes(self) -> List[Node]:
        return [Node(**n) for n in json.loads(self.command_executor.execute("sinfo --json"))["nodes"]]

    def get_jobs(self) -> List[Job]:
        jobs = json.loads(self.command_executor.execute("squeue --json"))["jobs"]
        return [Job(**j) for j in jobs]

    def __periodic_update_gpu_stats(self):
        self.gpus = self.all_gpu_stats()
        Timer(interval=self.gpu_state_interval, function=self.__periodic_update_gpu_stats).start()

    def __slurm_version(self) -> str:
        return json.loads(self.command_executor.execute("sinfo --json"))["meta"]["Slurm"]["release"]

    def num_nodes(self):
        return int(self.command_executor.execute("sinfo --Format=Nodes --noheader"))

    def gpu_stats(self, node_hostname: str) -> List[Gpu]:
        return self.gpus[node_hostname] if self.gpus is not None and node_hostname in self.gpus else list()

    def all_gpu_stats(self) -> Dict[str, List[Gpu]]:
        return {node.hostname: self.__gpu_stats(node.hostname) for node in self.get_nodes()}

    def __gpu_stats(self, node_hostname: str) -> List[Gpu]:
        def _parse_gpu_stats(command_output_lines: List[str]):
            gpus = []
            for g in command_output_lines:
                gpu_index, gpu_temp, gpu_mem, gpu_name, gpu_utilization = g.strip().split(",")
                gpus.append(
                    Gpu(
                        index=int(gpu_index),
                        type=GpuType.gpu_by_label(gpu_name.lstrip().replace(" ", "_").lower()),
                        memory_occupied=int(gpu_mem),
                        temperature=int(gpu_temp),
                        gpu_utilization=int(gpu_utilization),
                    )
                )
            return gpus

        gpu_stats = self.command_executor.execute(
            f"srun -w {node_hostname} --priority='TOP' -D /tmp -c 1 nvidia-smi --query-gpu=index,temperature.gpu,memory.used,gpu_name,utilization.gpu --format=csv,noheader,nounits",
            split_new_lines=True,
        )
        return _parse_gpu_stats(gpu_stats)