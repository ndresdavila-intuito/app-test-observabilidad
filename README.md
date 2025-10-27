## Descripción

Este repositorio contiene una aplicación de prueba desarrollada en Python que genera y envía datos de observabilidad utilizando OpenTelemetry.
La aplicación simula el procesamiento de solicitudes y exporta trazas, métricas y logs a un OpenTelemetry Collector mediante el protocolo OTLP/gRPC.

Cada pocos segundos, el programa:

Crea una traza que representa una operación simulada.

Registra una métrica que cuenta el número de solicitudes procesadas.

Envía logs informativos al colector y a la consola local.

## App de prueba para enviar observabilidad.

### Crear ambiente virtual

python -m venv venv

### Activar ambiente virtual

.\venv\Scripts\Activate.ps1

### Instalar desde requirements.txt

pip install -r requirements.txt

### Instalar dependencias exactas

pip install -r requirements_freeze.txt

### python app_prueba.py
