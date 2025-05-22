# -*- encoding: utf-8 -*-
"""
gunicorn-cfg.py
Gunicorn configuration file for running a Django application.
"""

bind = "0.0.0:8000"  # Bind to all interfaces on port 8000
workers = 1  # Number of worker processes
accesslog = "-"  # Log access to stdout
errorlog = "-"  # Log errors to stdout
loglevel = "debug"  # Set log level to debug
pidfile = "/tmp/gunicorn.pid"  # Path to the PID file
capture_output = True  # Capture stdout/stderr for logging
enable_stdio_inheritance = True  # Enable stdio inheritance