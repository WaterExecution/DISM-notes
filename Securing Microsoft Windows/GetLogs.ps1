# https://www.reddit.com/r/PowerShell/comments/69kbkd/getwinevent_vs_geteventlog_performance/
# https://powershellstation.com/2009/12/16/get-eventlog-and-get-wmiobject/

# https://stackoverflow.com/questions/16061681/pull-account-name-from-message-in-eventlog-powershell
# https://social.technet.microsoft.com/Forums/scriptcenter/en-US/be83c502-17b3-4831-aeb0-b0d904221b8c/time-format-question-when-capturing-event-log?forum=ITCG
# https://github.com/WaterExecution/vulnerable-AD-plus/blob/master/vulnadplus.ps1

# Timestamp,Security ID,Account Name,Object Type,Object Name,Audit Type (Success/Failure)
# 28/7/2022 10:37:44 am,Kitty\Mgr1,Mgr1,File,C:\Shares\SF3\smw_srv2016.txt,Success
# 28/7/2022 10:38:01 am,Kitty\user1,user1,File,C:\Shares\SF3\smw_srv2016.txt,Failure

$Global:computers = @("A2","A3");
$Global:eventlogs = @();
$Global:filename = "$((Get-Date).ToString('yyyy-MM-dd HH-mm-ss')).txt"
$Global:length = -7

# Remove duplicates for object name because c:\ C:\ is different
function Uppercase{
    Param(
        [string]$word
    )
    return $word.substring(0,1).ToUpper() + $word.substring(1)
}

# Detailed File Share events
foreach($computer in $Global:computers){
    $BeginDate=[System.Management.ManagementDateTimeConverter]::ToDMTFDateTime((get-date).AddDays($Global:length))
    Get-WmiObject -class win32_ntlogevent -computerName $computer -filter "(EventCode=5145) and (LogFile='Security') and (TimeGenerated >'$BeginDate')" |
    Where-Object {$_.Message -Like "*C:\Shares*"} |
    Where-Object {$_.InsertionStrings[1] -notlike "*$"} |
    Select @{n='Timestamp';e={[Management.ManagementDateTimeConverter]::ToDateTime($_.timeGenerated)}},
    @{n='Security ID';e={$_.InsertionStrings[2..1] -join "\" }},
    @{n='Account Name';e={$_.InsertionStrings[1]}},
    @{n='Object Type';e={$_.InsertionStrings[4]}},
    @{n='Object Name';e={$_.InsertionStrings[8..9] -join "\" -replace '\\\?\?\\', '' -replace '\\\\$', ''}},
    @{n='Audit Type (Success/Failure)';e={$_.Type -replace 'Audit ', ''}} |
    ForEach-Object{
        $Global:eventlogs += , @($_.Timestamp,$_.'Security ID',$_.'Account Name',$_.'Object Type',(Uppercase $_.'Object Name'),$_.'Audit Type (Success/Failure)')
    }
}

# File System events
foreach($computer in $Global:computers){
    $BeginDate=[System.Management.ManagementDateTimeConverter]::ToDMTFDateTime((get-date).AddDays($Global:length))
    Get-WmiObject -class win32_ntlogevent -computerName $computer -filter "(EventCode=4656) or (EventCode=4663) and (LogFile='Security') and (TimeGenerated >'$BeginDate')" |
    Where-Object {$_.Message -Like "*C:\Shares*"} |
    Where-Object {$_.InsertionStrings[1] -notlike "*$"} |
    Select @{n='Timestamp';e={[Management.ManagementDateTimeConverter]::ToDateTime($_.timeGenerated)}},
    @{n='Security ID';e={$_.InsertionStrings[2..1] -join "\" }},
    @{n='Account Name';e={$_.InsertionStrings[1]}},
    @{n='Object Type';e={$_.InsertionStrings[5]}},
    @{n='Object Name';e={$_.InsertionStrings[6]}},
    @{n='Audit Type (Success/Failure)';e={$_.Type -replace 'Audit ', ''}} |
    ForEach-Object{
        $Global:eventlogs += , @($_.Timestamp,$_.'Security ID',$_.'Account Name',$_.'Object Type',(Uppercase $_.'Object Name'),$_.'Audit Type (Success/Failure)')
    }
}

# Write to file and remove duplicates and display latest event on top
"Timestamp,Security ID,Account Name,Object Type,Object Name,Audit Type (Success/Failure)" | Out-File -FilePath $Global:filename
$Global:eventlogs | Sort-Object -Descending | Get-Unique | ForEach-Object{
    $_ -join "," >> $Global:filename
}