$currentDir = $pwd

$directoryContents = Get-ChildItem -Path $currentDir
cls
foreach ($directoryContent in $directoryContents)
{
    #write-host($directoryContent)
    if($directoryContent.ToString().EndsWith(".lnk"))
    {
        $shell = New-Object -COM WScript.Shell
        $link = $shell.CreateShortcut($directoryContent.fullname)
        $linkPath = $link.TargetPath
        
        $resultsPath = Join-Path -path $linkPath "results"
        
        write-host("results dir is: {0}" -f $resultsPath)
        
        $resultsDestination = Get-ChildItem -Path $linkPath
        
        foreach ($item in $resultsDestination)
        {
            if($item.ToString().EndsWith(".lnk"))
            {
                $shell = New-Object -COM WScript.Shell
                $link = $shell.CreateShortcut($item.fullname)
                $resultsTargetPath = $link.TargetPath
                write-host("target dir is: {0}" -f $resultsTargetPath)
            }
        }
        
        
        
        
        $resultsChildren = Get-ChildItem -Path $resultsPath
        
        foreach ($resultsChild in $resultsChildren)
        {
            write-host("working on: {0}" -f $resultsChild)
            $fullChildPath = Join-Path -path $resultsPath -Childpath $resultsChild
            Copy-Item -force $fullChildPath $resultsTargetPath
        }
        
        #Copy-Item -force
    }
}

Read-Host -Prompt "Press Enter to continue"