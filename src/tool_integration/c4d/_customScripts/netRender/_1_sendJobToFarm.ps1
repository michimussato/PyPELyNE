# place this script to any output folder which contains a C4D project WITH ASSETS
# it copies all subelements (.c4d and tex) to the destination of a .lnk-file

$currentDir = $pwd

$directoryContents = Get-ChildItem -Path $currentDir
cls
foreach ($directoryContent in $directoryContents)
{
    #write-host($directoryContent)
    if($directoryContent.ToString().EndsWith(".lnk"))
    {
        $destinationDir = resolve-path $directoryContent
        write-host("dirContent is link: {0}" -f $directoryContent)
        #write-host("fullPath: {0}" -f $destinationDir)
        $shell = New-Object -COM WScript.Shell
        $link = $shell.CreateShortcut($directoryContent.fullname)
        $linkPath = $link.TargetPath
        #write-host("destination: {0}`n" -f $linkPath)
        
    }
    elseIf($directoryContent -is [System.IO.DirectoryInfo])
    {
        #write-host( write-host(Join-Path $currentDir $directoryContent) )
        write-host("dirContent is directory: {0}`n" -f $directoryContent)
        $fullSourcePath = Join-Path -path $currentDir -Childpath $directoryContent
        #write-host("full path directory: {0}`n" -f $fullSourcePath)
        
    }
    else
    {
        write-host("dirContent is something else: {0}" -f $directoryContent)
    }
}


#write-host("source:      {0}`n" -f $fullSourcePath)
#write-host("destination: {0}`n" -f $linkPath)

$sourceChildren = Get-ChildItem -Path $fullSourcePath

foreach ($sourceChild in $sourceChildren)
{
    write-host("copying :      {0}`n" -f $sourceChild)
    $fullChildPath = Join-Path -path $fullSourcePath -Childpath $sourceChild
    #write-host("child full : {0}`n" -f $fullChildPath)
    write-host("to:            {0}`n" -f $linkPath)
    Copy-Item -force $fullChildPath $linkPath -recurse
}

Read-Host -Prompt "Press Enter to continue"