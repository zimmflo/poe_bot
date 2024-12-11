cd 1_host
set machine=a2
set debug=0
set unique_id=b930676c8593d53test_a4
set remote_ip=172.22.152.242
set password=n19980502
set build_name=PoisonConcBouncingPf
set predefined_strategy=atlas_explorer

TITLE %machine% %remote_ip% %unique_id% %predefined_strategy% %build_name%
:infinity_loop
python launch.py {'script':'maps','REMOTE_IP':'%remote_ip%','unique_id':'%unique_id%','password':'%password%','force_reset_temp':False,'custom_strategy':'','predefined_strategy':'%predefined_strategy%','build':'%build_name%'}

goto :infinity_loop

