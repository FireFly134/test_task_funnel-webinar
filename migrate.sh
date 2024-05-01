#!/bin/sh

alembic revision --autogenerate -m "create_migration"
alembic upgrade head
python3 main.py