$docs = Get-ChildItem -Filter '*.md'
foreach ($f in $docs) {
    $file = $f.FullName
    $text = Get-Content -Raw $file
    $rx = [regex]::Matches($text, '```mermaid([\s\S]*?)```')
    if ($rx.Count -eq 0) {
        Write-Host "No mermaid block in $($f.Name)"
        continue
    }
    $i = 0
    foreach ($m in $rx) {
        $i++
        $content = $m.Groups[1].Value.Trim()
        $mmd = [System.IO.Path]::ChangeExtension($file, ".mmd")
        if ($i -gt 1) {
            $mmd = [System.IO.Path]::ChangeExtension($file, "-$i.mmd")
        }
        Set-Content -Path $mmd -Value $content
        Write-Host "Generated $mmd"
        npx -y @mermaid-js/mermaid-cli -i $mmd -o ([System.IO.Path]::ChangeExtension($mmd,'.svg'))
    }
}
