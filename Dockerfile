FROM python:3.8-alpine
RUN mkdir /app
ADD ./app.py /app
ADD ./requirments.txt /app
WORKDIR /app
RUN pip3 install -r requirments.txt
EXPOSE  4004
CMD ["python3", "app.py"]
