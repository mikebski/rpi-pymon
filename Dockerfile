FROM python
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install psycopg2
RUN pip install pika
RUN apt-get autoremove -y gcc
RUN mkdir /opt/consumer
COPY consume.py /opt/consumer/
CMD ["python","/opt/consumer/consume.py"]
