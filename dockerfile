# special lambda python image
FROM public.ecr.aws/lambda/python:latest

# set location as lambda task root - all lambdas are here
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements. txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy function code
COPY pipeline.py .
COPY scrape.py . 
COPY insert.py .


# Set the CMD to your handler (file.function)
CMD ["pipeline.lambda_handler"]

# AWS ECR PUSH COMMANDS:
    # aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
    # docker build --platform "linux/amd64" -t c11-fariha-trucks-report .
    # docker tag c11-fariha-trucks-report:latest 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-trucks-report:latest
    # docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c11-fariha-trucks-report:latest



