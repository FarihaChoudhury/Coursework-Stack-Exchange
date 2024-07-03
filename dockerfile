FROM python:latest

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY scrape.py . 
COPY insert.py .
COPY pipeline.py .

CMD python3 pipeline.py 






# RUN LOCALLY:
    # docker build -t stack-exchange-etl-local .
    # docker image ls
    # docker run --env-file .env stack-exchange-etl-local (??)

# AWS ECR PUSH COMMANDS:
    # aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
    # docker build --platform "linux/amd64" -t c11-fariha-stack-exchange-pipeline .
    # docker tag c11-fariha-stack-exchange-pipeline:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-stack-exchange-pipeline:latest
    # docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-stack-exchange-pipeline:latest



