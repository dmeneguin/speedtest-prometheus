import speedtest
from prometheus_client import start_http_server, Gauge
import time
import os
import logging
import json
import sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "filename": record.filename,
            "lineno": record.lineno,
            "function": record.funcName,
        }
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


# Define Prometheus metrics
download_speed = Gauge('internet_download_mbps', 'Download speed in Mbps')
upload_speed = Gauge('internet_upload_mbps', 'Upload speed in Mbps')
latency = Gauge('internet_latency_ms', 'Latency in milliseconds')
last_speedtest_timestamp = Gauge('last_speedtest_timestamp', 'Timestamp of the last speed test (Unix time)')
available = Gauge('available', 'Internet is available')

APP_PORT = os.getenv("APP_PORT","8000")
POLLING_INTERVAL_MINUTES = os.getenv("POLLING_INTERVAL_MINUTES","15")

# Simulate speed test and update metrics
def simulate_speed_test():
    while True:
        try:
            logger.info("testing connection...")
            st = speedtest.Speedtest()
            st.get_best_server()

            ping = st.results.ping
            download = st.download()
            upload = st.upload()
            online = 1
            logger.info(f"connection tested. Ping:{ping}, Download:{download}, Upload:{upload}")
        except Exception as e:
            logger.error(e)
            ping = 0
            download = 0
            upload = 0
            online = 0            

        now = int(time.time())

        download_speed.set(download)
        upload_speed.set(upload)
        latency.set(ping)
        last_speedtest_timestamp.set(now)
        available.set(online)
        time.sleep(int(POLLING_INTERVAL_MINUTES) * 60)

if __name__ == '__main__':
    start_http_server(int(APP_PORT))
    print("Prometheus metrics available at http://localhost:8000/metrics")
    simulate_speed_test()