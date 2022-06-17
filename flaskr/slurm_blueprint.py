import dataclasses
from flask import Blueprint
import os
import json
from flaskr.slurm import Slurm
from flask import render_template


slurm_bp = Blueprint("slurm", __name__, url_prefix="/slurm")
slurm_api = Slurm()


@slurm_bp.route("/")
def index():
    output = os.popen("sinfo --noheader").read()
    return output


@slurm_bp.route("/squeue")
def squeue():
    return json.dumps([job.to_json() for job in slurm_api.get_jobs()])


@slurm_bp.route("/sinfo")
def sinfo():
    return render_template("slurm.html", nodes=[dataclasses.asdict(n) for n in slurm_api.cluster_nodes()])
