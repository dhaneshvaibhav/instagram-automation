import multiprocessing
import os

# Gunicorn configuration for FastAPI/Uvicorn
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Timeouts
timeout = 120
keepalive = 5
