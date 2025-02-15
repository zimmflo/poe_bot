protoc --python_out="%cd%\..\utils" data.proto
protoc --csharp_out="%cd%\..\..\0_guest\Plugins\Source\ShareData" data.proto
pause