## korean client, mouse doesnt move.
- not sure why, but sending inputs via win32 doesnt work in pair with korean client, use standalone instead

## running on host, 50006 port is free, hyper-v enabled. hud plugin ->ServerRestartEvent was crushed -> System.Net.HttpListenerException (32):" where error 32 is "file already opened"
- shortly, hyper-v reserves ports around 50000 for internal use, disable hyper-v, or manually restrict hyper-v from using 50006, https://github.com/docker/for-win/issues/3171#issuecomment-1895729704

