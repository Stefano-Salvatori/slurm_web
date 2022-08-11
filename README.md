# Start Application

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=37339
```

or (for production)

```bash
export FLASK_APP=flaskr
export FLASK_ENV=production
waitress-serve --port=$PORT --call 'flaskr:create_app'
```

You can also use the bash script `start_server.sh`
```bash
start_server.sh <dev|prod> <port>
```

## Start inside Docker
Build with 
```bash
sudo docker build -t <image> .
```
use `<image>= slurm-web-app-test` for testing and `<image>= slurm-web-app` for production

For production:
```bash
sudo docker run -d -it -v /etc/munge:/etc/munge:ro -v /etc/slurm/:/etc/slurm:ro -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro --net=host --restart always slurm-web-app prod <port>
```

For testing:
```bash
sudo docker run -it --rm -v /etc/munge:/etc/munge:ro -v /etc/slurm/:/etc/slurm:ro -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro --net=host slurm-web-app-test <dev|prod> <port>
```