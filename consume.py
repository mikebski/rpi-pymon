#!/usr/bin/env python
import pika
import psycopg2
import time

dbconn = None
cur = None
insertStatement = "INSERT INTO stats (stats_json) VALUES (%s)"

while dbconn is None:
	try:
		dbconn = psycopg2.connect(dbname="pimon", user="postgres", password="83riafdfbak8793qjqktlk;b;'q0[", host="db")
		cur = dbconn.cursor()
		print(' [*] Database connected')
	except:
		print(' [^] Database connection error, trying again')
		time.sleep(1)
		pass
	pass


connection = None
while connection is None:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmqmon'))
		channel = connection.channel()
	except:
       		print(' [^] Messaging connection error, trying again')
        	time.sleep(1)
        	pass
	pass

#channel.exchange_declare(exchange='test', exchange_type='fanout')
#result = channel.queue_declare(queue='', exclusive=True)

queue_name = "test"
channel.queue_declare(queue='test')
#channel.queue_bind(exchange='test', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    bodyStr = body.decode('utf-8')
    print(" [x] %s" % bodyStr)
    cur.execute(insertStatement, (bodyStr,))
    dbconn.commit()

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
