cd 1_host
set machine=k1
set debug=0
set unique_id=00e01bebd8bb
set remote_ip=172.23.246.121
set password=n19980502
TITLE %machine% %remote_ip% %unique_id% 
:infinity_loop
python price_checker.py {'REMOTE_IP':'%remote_ip%','unique_id':'%unique_id%','password':'%password%','force_reset_temp':False}
pause
goto :infinity_loop

