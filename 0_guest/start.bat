@echo off
call venv\Scripts\activate
:infinity_loop
python vm_host_main_socket.py
goto infinity_loop