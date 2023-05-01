FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install awscli
RUN aws s3 cp s3://ia-s3-bucket/ddilchan-json.zip .
RUN unzip ddilchan-json.zip

COPY . .

CMD [ "python3", "main.py" ]
