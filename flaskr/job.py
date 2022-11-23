from dataclasses import dataclass, field
from typing import Dict, List
import time
import datetime
import re


@dataclass
class AllocatedNode:
    sockets: dict = field(default_factory=dict)
    cores: dict = field(default_factory=dict)
    memory: int = 0
    cpus: int = 0


@dataclass
class JobResources:
    nodes: str = ""
    allocated_cpus: int = 0
    allocated_hosts: int = 0
    allocated_nodes: Dict[str, AllocatedNode] = field(default_factory=dict)


@dataclass
class Job:
    name: str = ""
    account: str = ""
    accrue_time: int = 0
    admin_comment: str = ""
    array_job_id: int = 0
    array_task_id: int = None
    array_max_tasks: int = 0
    array_task_string: str = ""
    association_id: int = 0
    batch_features: str = ""
    batch_flag: bool = True
    batch_host: str = ""
    flags: list = field(default_factory=list)
    burst_buffer: str = ""
    burst_buffer_state: str = ""
    cluster: str = ""
    cluster_features: str = ""
    command: str = ""
    comment: str = ""
    contiguous: bool = False
    core_spec: str = None
    thread_spec: str = None
    cores_per_socket: int = None
    billable_tres: int = 0
    cpus_per_task: int = 0
    cpu_frequency_minimum: int = None
    cpu_frequency_maximum: int = None
    cpu_frequency_governor: int = None
    cpus_per_tres: str = ""
    deadline: int = 0
    delay_boot: int = 0
    dependency: str = ""
    derived_exit_code: int = 0
    eligible_time: int = 0
    end_time: int = 0
    excluded_nodes: str = ""
    exit_code: int = 0
    features: str = ""
    federation_origin: str = ""
    federation_siblings_active: str = ""
    federation_siblings_viable: str = ""
    gres_detail: list = field(default_factory=list)
    group_id: int = 0
    job_id: int = 0
    job_resources: JobResources = None
    job_state: str = ""
    last_sched_evaluation: int = 0
    licenses: str = ""
    max_cpus: int = 0
    max_nodes: int = 0
    mcs_label: str = ""
    memory_per_tres: str = ""
    nodes: str = ""
    nice: int = None
    tasks_per_core: int = None
    tasks_per_node: int = 0
    tasks_per_socket: int = None
    tasks_per_board: int = 0
    cpus: int = 0
    node_count: int = 0
    tasks: int = 0
    het_job_id: int = 0
    het_job_id_set: str = ""
    het_job_offset: int = 0
    partition: str = ""
    memory_per_node: int = None
    memory_per_cpu: int = None
    minimum_cpus_per_node: int = 0
    minimum_tmp_disk_per_node: int = 0
    preempt_time: int = 0
    pre_sus_time: int = 0
    priority: int = 0
    profile: str = None
    qos: str = ""
    reboot: bool = False
    required_nodes: str = ""
    requeue: bool = True
    resize_time: int = 0
    restart_cnt: int = 0
    resv_name: str = ""
    shared: str = ""
    show_flags: list = field(default_factory=list)
    sockets_per_board: int = 0
    sockets_per_node: int = None
    start_time: int = 0
    state_description: str = ""
    state_reason: str = ""
    standard_error: str = ""
    standard_input: str = ""
    standard_output: str = ""
    submit_time: int = 0
    suspend_time: int = 0
    system_comment: str = ""
    time_limit: int = None
    time_minimum: int = 0
    threads_per_core: int = None
    tres_bind: str = ""
    tres_freq: str = ""
    tres_per_job: str = ""
    tres_per_node: str = ""
    tres_per_socket: str = ""
    tres_per_task: str = ""
    tres_req_str: str = ""
    tres_alloc_str: str = ""
    user_id: int = 0
    user_name: str = ""
    wckey: str = ""
    current_working_directory: str = ""

    @property
    def timeused(self) -> datetime.timedelta:
        return datetime.datetime.fromtimestamp(time.time()) - datetime.datetime.fromtimestamp(self.start_time)
    
    @property
    def gpu_indices(self) -> List[int]:
        if self.gres_detail is None or len(self.gres_detail) == 0:
            return list()
        parsed = re.compile("gpu:\w*:\d\(IDX:(\d)(-(\d))*\)").search(self.gres_detail[0])
        return [int(g) for g in parsed.groups()[::2] if g is not None] if parsed is not None else []

