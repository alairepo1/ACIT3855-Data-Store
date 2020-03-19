import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from order_form import OrderForm
from repair_form import RepairForm
import datetime
import json
import yaml
from threading import Thread
import pykafka
from flask_cors import CORS, cross_origin


with open('app_conf.yaml', 'r') as f:
    app_conf = yaml.safe_load(f.read())


with open("kafka_conf.yaml", 'r') as f:
    kafka_conf = yaml.safe_load(f.read())

DB_ENGINE = create_engine('mysql+pymysql://' 
+ app_conf['datastore']['user'] 
+ ":" + app_conf['datastore']['password'] + "@" 
+ app_conf['datastore']['hostname'] + ":" 
+ app_conf['datastore']['port'] + '/' + app_conf['datastore']['db'])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_order_forms(startDate, endDate):
    """
    Takes in a start and end date and filters out the order forms
    that are within the dates
    """
    results_list = []
    session=DB_SESSION()

    results=[]
    results=session.query(OrderForm).all()

    for result in results:     
        if checkDateTime(startDate, endDate, result.to_dict()['date_created']):
            results_list.append(result.to_dict())   
        else: 
            pass

    session.close()
    return results_list, 200

def get_repair_forms(startDate, endDate):
    """
    Takes in a start and end date and filters out the repair forms
    that are within the dates
    """

    results_list = []
    session=DB_SESSION()

    results=[]
    results=session.query(RepairForm).all()
    for result in results:
        if checkDateTime(startDate, endDate, result.to_dict()['date_created']):
            results_list.append(result.to_dict())   
        else: 
            pass

    session.close()
    return results_list, 200


def checkDateTime(startDate, endDate, dateToCheck):
    if datetime.datetime.strptime(startDate,"%Y-%m-%dT%H:%M:%S") < datetime.datetime.strptime(dateToCheck, "%Y-%m-%d %H:%M:%S.%f") \
            and datetime.datetime.strptime(dateToCheck,"%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.strptime(endDate,"%Y-%m-%dT%H:%M:%S"):
        return True
    else: 
        return False

def process_messages():
    """
    sProesses messages from kafka producer in Lab1 
    adds to the database
    """
    client = pykafka.KafkaClient(
    hosts=kafka_conf['kafka']['server'] + ':' + kafka_conf['kafka']['port'])
    topic = client.topics[kafka_conf['kafka']['topic']]
    
    consumer = topic.get_simple_consumer(
        consumer_group="mygroup",
        auto_offset_reset=pykafka.common.OffsetType.LATEST,
        reset_offset_on_start=True,
        auto_commit_enable=True,
        auto_commit_interval_ms=1000
    )
    

    headers = {
        'Content-Type': 'application/json'
    }

    for message in consumer:
        msg = json.loads(message.value.decode('utf-8', errors='replace'))
        print(msg)
        if msg['type'] == 'order_form':
            session = DB_SESSION()

            data=msg['payload']
            of = OrderForm(
                data['customer_address'],
                data['customer_id'],
                data['customer_name'],
                data['price_id'],
                data['shoe_id'],
                data['timestamp']
            )

            session.add(of)
            session.commit()
            session.close()

        elif msg['type'] == 'repair_form':
            session = DB_SESSION()
            data=msg['payload']
            rf = RepairForm(
                data['customer_address'],
                data['customer_id'],
                data['customer_name'],
                data['damage_description'],
                data['shoe_type'],
                data['timestamp']
            )

            session.add(rf)

            session.commit()
            session.close()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1=Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)