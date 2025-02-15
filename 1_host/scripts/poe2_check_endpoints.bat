@echo off

call venv\Scripts\activate
python poe_2_test_all_tcp_endpoints.py %1 %2

PAUSE