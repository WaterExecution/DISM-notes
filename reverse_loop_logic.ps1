$test1 = Test-Path 'HKLM:\SOFTWARE\Raptor'
$test2 = Test-Path 'HKLM:\SOFTWARE\RAPTOR'
if (-not $test1 -and -not $test2){
reg add "HKLM\SOFTWARE\RAPTOR"
reg add "HKLM\SOFTWARE\RAPTOR" /v reverse_loop_logic /d true
}
elseif ($test1){
reg add "HKLM\SOFTWARE\Raptor" /v reverse_loop_logic /d true
}
elseif ($test2){
reg add "HKLM\SOFTWARE\RAPTOR" /v reverse_loop_logic /d true
}