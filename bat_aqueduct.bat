cd 1_host
set machine=g2
set debug=0
set unique_id=7d1165934e24534a1ba5_g2
set remote_ip=172.30.3.75
set password=n19980502
set build_name=GenericHitter
set predefined_strategy=atlas_explorer


TITLE %machine% %remote_ip% %unique_id% %predefined_strategy% %build_name%
:infinity_loop
python launch.py {'script':'aqueduct','REMOTE_IP':'%remote_ip%','unique_id':'%unique_id%','password':'%password%','force_reset_temp':False,'custom_strategy':'','predefined_strategy':'%predefined_strategy%','build':'%build_name%'}

goto :infinity_loop

