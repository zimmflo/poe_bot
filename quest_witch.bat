cd 1_host
set machine=d1
set debug=0
set unique_id=7d1165934e24534a1ba5_quest
set remote_ip=172.19.137.191
set password=n19980502
set strategy=witch_minions

TITLE %machine% %remote_ip% %unique_id% %predefined_strategy% %build_name%
:infinity_loop
python quest.py {'REMOTE_IP':'%remote_ip%','unique_id':'%unique_id%','password':'%password%','force_reset_temp':False,'custom_strategy':'','leveling_strategy':'%strategy%'}

goto :infinity_loop

