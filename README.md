## App de prueba para enviar observabilidad.

# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
.\venv\Scripts\Activate.ps1

# Instalar desde requirements.txt
pip install -r requirements.txt

# Instalar dependencias exactas
pip install -r requirements_freeze.txt

# Ejecutar programa
python app_prueba.py
