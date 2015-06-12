cls

$shot = ""
$start = ""
$stop = ""

$currentDir = $pwd

$fusion = "C:\Program Files\Blackmagic Design\Fusion\Fusion.exe"

$compDir = "\\SMSRV-001\Allgemein\Kunden\UBS\UBS_Artcontent_2014\tasks\0030__compositing"

$fullShotDir = Join-Path -path $compDir -Childpath $shot

$fullCompDir = Join-Path -path $fullShotDir -Childpath "project"

#write-host("fullCompDir is: {0}" -f $fullCompDir)

$latestComp = gci -Filter "*.comp" $fullCompDir | sort LastWriteTime | select -last 1

#write-host("latestComp is: {0}" -f $latestComp)

$fullCompPath = Join-Path -path $fullCompDir -Childpath $latestComp

#write-host("fullCompPath is: {0}" -f $fullCompPath)

$arguments = $fullCompPath + " /render /start " + $start + " /end " + $end + " /verbose /quiet /quit"

#write-host("arguments is: {0}" -f $arguments)



Start-Process -FilePath $fusion -ArgumentList $arguments

write-host("shot {0} finished" -f $shot)
Read-Host -Prompt "Press Enter to continue"