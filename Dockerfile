FROM slurm-web

WORKDIR /app

COPY environment.yml /app/environment.yml
COPY flaskr ./flaskr
COPY start_server.sh ./start_server.sh

RUN conda init bash
RUN . /root/.bashrc \
    && conda init bash \
    && conda env create -f environment.yml \
    && conda activate slurm_web \
    && conda install -c conda-forge waitress -y 

ENTRYPOINT ["/app/start_server.sh"]

CMD ["prod", "37336"]
