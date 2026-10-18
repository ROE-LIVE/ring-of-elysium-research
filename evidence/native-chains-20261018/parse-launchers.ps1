param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Paths)
$ErrorActionPreference = 'Stop'
foreach ($path in $Paths) {
    $tokens = $null
    $parseErrors = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$parseErrors)
    if ($parseErrors.Count -ne 0) { throw ($parseErrors | Out-String) }
    if ([System.IO.Path]::GetFileName($path) -eq 'bootstrap.ps1') {
        $parameter = $ast.ParamBlock.Parameters | Where-Object { $_.Name.VariablePath.UserPath -eq 'PracticeTargets' }
        if ($null -eq $parameter) { throw 'PracticeTargets parameter missing' }
        $block = [scriptblock]::Create('param(' + $parameter.Extent.Text + ') $PracticeTargets')
        if ((& $block -PracticeTargets 10) -ne 10) { throw 'Ten targets binding failed' }
        foreach ($bad in @(0, 11)) {
            $rejected = $false
            try { & $block -PracticeTargets $bad | Out-Null } catch { $rejected = $true }
            if (-not $rejected) { throw 'Invalid target count accepted' }
        }
    }
    Write-Output ('PARSE_OK ' + $path)
}
