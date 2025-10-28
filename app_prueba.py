import os
import time
import logging
from random import randint
from dotenv import load_dotenv

from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggingHandler  # Este es el Handler oficial para logging

# ------------------- Variables de entorno -------------------
load_dotenv()
SERVICE_NAME = os.getenv("SERVICE_NAME", "app-prueba")
OTEL_ENDPOINT = os.getenv(
    "OTEL_COLLECTOR_ENDPOINT",
    "http://otel-collector.observabilidad.svc.cluster.local:4317",
)

# ------------------- Recurso común -------------------
resource = Resource.create({"service.name": SERVICE_NAME})

# ------------------- Traces -------------------
trace_provider = TracerProvider(resource=resource)
trace_exporter = OTLPSpanExporter(endpoint=OTEL_ENDPOINT, insecure=True)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

# ------------------- Metrics -------------------
metric_exporter = OTLPMetricExporter(endpoint=OTEL_ENDPOINT, insecure=True)
metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter(__name__)
counter = meter.create_counter("requests_total", description="Número de solicitudes procesadas")

# ------------------- Logs -------------------
logger_provider = LoggerProvider(resource=resource)
log_exporter = OTLPLogExporter(endpoint=OTEL_ENDPOINT, insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

# Logger de Python normal con OTEL
logger = logging.getLogger(SERVICE_NAME)
logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# Handler para OTEL Collector
otel_handler = LoggingHandler(logger_provider=logger_provider, level=logging.INFO)
logger.addHandler(otel_handler)

# ------------------- Loop de prueba -------------------
logger.info("Inicio de la aplicación de prueba.")

while True:
    with tracer.start_as_current_span("procesar_peticion") as span:
        requests = randint(1, 100)
        span.set_attribute("valor.random", requests)
        counter.add(1, {"tipo": "aleatorio"})

        logger.info(f"Procesadas {requests} solicitudes.")  # Consola + OTEL Collector
    time.sleep(3)
