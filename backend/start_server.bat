@echo off
REM Скрипт для запуска всех сервисов на windows
start "Uvicorn Server" cmd /k "uvicorn main:app --reload"
start "HTTP Server" cmd /k "http-server -p 8081"
start "Redis Server" cmd /k "redis-server"
start "Locust" cmd /k "cd tests && locust -f locustfile.py --host=http://127.0.0.1:8000"
