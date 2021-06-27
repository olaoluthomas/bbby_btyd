FROM python:3.9.1-slim
COPY . /bucket
WORKDIR /bucket
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python ./src/main.py