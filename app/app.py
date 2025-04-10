import json
import logging
import os
import time
from datetime import datetime
import redis
from elasticsearch import Elasticsearch
from flask import Flask, jsonify
from prometheus_client import Counter

app = Flask(__name__)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "time": self.formatTime(record),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configuración del logger
logger = logging.getLogger("jsonLogger")

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = 6379
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# Redis connection
db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Elasticsearch configuration
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch')
es = Elasticsearch(f"http://{ELASTICSEARCH_HOST}:9200")

# Prometheus metrics
REQUESTS = Counter('server_requests_total', 'Total number of requests to this webserver')
HEALTHCHECK_REQUESTS = Counter(
    'healthcheck_requests_total',
    'Total number of requests to healthcheck'
)
MAIN_ENDPOINT_REQUESTS = Counter('main_requests_total', 'Total number of requests to main endpoint')
LOGS_ENDPOINT_REQUESTS = Counter('logs_requests_total', 'Total number of requests to logs endpoint')

# Error: Uncomment to see how pylint works.
# x = "This variable has a very short name"

def get_hit_count():
    retries = 5
    while True:
        try:
            return db.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def index():
    count = get_hit_count()
    logger.info("Request recibido")

    # Crear el mensaje de log
    log_message = {
        "redis_host": REDIS_HOST,
        "redis_port": REDIS_PORT,
        "message": "Request recibido",
        "hits": count,
        "timestamp": datetime.now().isoformat()
    }

    # Indexar datos en Elasticsearch
    try:
        es.index(index="flask-logs", document=log_message)
        logger.info(f"Datos almacenados en Elasticsearch: {log_message}")
        REQUESTS.inc()
        MAIN_ENDPOINT_REQUESTS.inc()
    except Exception as e:
        logger.error(f"Error al almacenar en Elasticsearch: {e}")
        return jsonify({"error": str(e)}), 500


    return f"La página ha sido cargada {count} veces."

@app.route("/health", methods=["GET"])
def health_check():
    """Implement health check endpoint"""

    logger.info("Healthcheck request received")

    log_message = {
        "message": "Request a health recibido",
        "timestamp": datetime.now().isoformat()
    }

    try:
        es.index(index="health-logs", document=log_message)
        logger.info(f"Llamada a health almacenada: {log_message}")

        REQUESTS.inc()
        HEALTHCHECK_REQUESTS.inc()

        return {"health": "ok"}
    except Exception as e:
        logger.error(f"Error de llamada a health: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Recupera los datos almacenados en Elasticsearch.
    """
    try:
        response = es.search(index=["flask-logs", "health-logs"], query={"match_all": {}})
        hits = response.get("hits", {}).get("hits", [])
        logs = [hit["_source"] for hit in hits]
        logger.info("Datos recuperados desde Elasticsearch")

        REQUESTS.inc()
        LOGS_ENDPOINT_REQUESTS.inc()

        return jsonify(logs), 200
    except Exception as e:
        logger.error(f"Error al recuperar datos desde Elasticsearch: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
