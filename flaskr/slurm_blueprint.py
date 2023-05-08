from flask import Blueprint
import json
from flaskr.slurm import Slurm
from flask import render_template
import socket

slurm_bp = Blueprint("slurm", __name__, url_prefix="/slurm")
slurm_api = Slurm()


@slurm_bp.route("/", methods=["GET"])
def sinfo():
    jobs = slurm_api.get_jobs()
    nodes = sorted(slurm_api.get_nodes(), key=lambda n: socket.inet_aton(n.address))
    for node in nodes:
        node.allocated_jobs = [j for j in jobs if node.hostname == j.nodes]
    return render_template("slurm.html", nodes=nodes, jobs=jobs)


@slurm_bp.route("/api/v1/nodes/<hostname>/gpus", methods=["GET"])
def node_gpus(hostname: str):
    return json.dumps(slurm_api.gpu_stats(hostname), default=vars)
