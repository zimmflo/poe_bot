cd 1_host

set machine=j2
set debug=0
set unique_id=poe2_test
set build_name=InfernalistMinion
set hostname=WIN-POE1

REM if you want to use the ip, then REM the next line and -- set remote_ip=
for /f "tokens=2 delims=[]" %%a in ('ping -n 1 %hostname% ^| findstr "["') do set remote_ip=%%a

TITLE %machine% %remote_ip% %unique_id% %predefined_strategy% %build_name%
call venv\Scripts\activate

:infinity_loop
python poe_2_mapper.py {'script':'maps','REMOTE_IP':'%remote_ip%','unique_id':'%unique_id%','password':'%password%','force_reset_temp':False,'custom_strategy':'','predefined_strategy':'%predefined_strategy%','build':'%build_name%'}
pause
goto :infinity_loop