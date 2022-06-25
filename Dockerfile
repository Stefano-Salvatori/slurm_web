FROM slurm-web


COPY environment.yml /app/environment.yml

WORKDIR /app

# SHELL ["/bin/bash", "-c"] 

RUN conda init bash
RUN . /root/.bashrc \
    && conda init bash \
    && conda env create -f environment.yml \
    && conda activate slurm_web \
    && conda install -c conda-forge waitress -y

COPY flaskr ./flaskr
COPY start_server.sh ./start_server.sh
#ENTRYPOINT ["/app/start_server.sh"]

#CMD ["prod", "37336"]
