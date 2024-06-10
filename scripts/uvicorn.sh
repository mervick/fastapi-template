#!/usr/bin/env bash

/usr/local/bin/alembic upgrade head
/usr/local/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
