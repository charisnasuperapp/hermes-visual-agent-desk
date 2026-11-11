param()

$ErrorActionPreference = 'Stop'
$officeUrl = 'http://127.0.0.1:3100/CHA/agent-pixels'
Write-Host "Paperclip: $officeUrl"
Write-Host 'Tutup jendela ini untuk menghentikan server.'
& npx --yes --registry https://registry.npmjs.org paperclipai run
