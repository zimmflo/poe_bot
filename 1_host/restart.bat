@echo off

:loop
tasklist | find /i "PathOfExile.exe" && (
    tasklist | find /i "Alcor75RDServer.exe" && (
        tasklist | find /i "DreamPoeBot.exe" || (
            taskkill /IM PathOfExile.exe /F
            taskkill /IM Alcor75RDServer.exe /F
            taskkill /IM DreamPoeBot.exe /F
        )
    )
) || (
    taskkill /IM PathOfExile.exe /F
    taskkill /IM Alcor75RDServer.exe /F
    taskkill /IM DreamPoeBot.exe /F

    cd "C:\Program Files (x86)\Grinding Gear Games\Path of Exile\"
    start "" "PathOfExile.exe" --nopatch
    
    timeout /t 10

    cd "C:\TradeMacro\DreamPoeBot\"
    start "" "DreamPoeBot.exe" --autostart --autoupdate
)


timeout /t 60

goto loop