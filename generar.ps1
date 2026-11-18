# generar.ps1 - Compila euler.cpp y genera las 3 trazas JSON con un solo comando.
#
# Uso (desde PowerShell, en la carpeta del proyecto):
#   .\generar.ps1
#   .\generar.ps1 -Cxx "C:\ruta\a\g++.exe"     # solo si no encuentra g++ solo
#
# Busca g++ en este orden: -Cxx, PATH, CLion (cualquier version), MSYS2,
# w64devkit, Chocolatey y WinLibs.
#
# Si Windows bloquea el script:
#   powershell -ExecutionPolicy Bypass -File .\generar.ps1

param(
    [string]$Cxx = ""
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
[Environment]::CurrentDirectory = $PSScriptRoot   # carpeta que hereda cmd /c

function Find-Gpp {
    $enPath = Get-Command g++ -ErrorAction SilentlyContinue
    if ($enPath) { return $enPath.Source }
    $patrones = @(
        "$env:ProgramFiles\JetBrains\CLion*\bin\mingw\bin\g++.exe",
        "$env:LOCALAPPDATA\Programs\CLion*\bin\mingw\bin\g++.exe",
        "$env:LOCALAPPDATA\JetBrains\Toolbox\apps\CLion\*\*\bin\mingw\bin\g++.exe",
        "C:\msys64\ucrt64\bin\g++.exe",
        "C:\msys64\mingw64\bin\g++.exe",
        "C:\w64devkit\bin\g++.exe",
        "$env:ProgramData\mingw64\mingw64\bin\g++.exe",
        "C:\mingw64\bin\g++.exe",
        "C:\MinGW\bin\g++.exe"
    )
    foreach ($p in $patrones) {
        # Si hay varias versiones (p. ej. de CLion), usar la mas reciente.
        $hallado = Get-ChildItem -Path $p -ErrorAction SilentlyContinue |
                   Sort-Object FullName -Descending | Select-Object -First 1
        if ($hallado) { return $hallado.FullName }
    }
    return $null
}

if ($Cxx) {
    $cmd = Get-Command $Cxx -ErrorAction SilentlyContinue
    if (-not $cmd) { Write-Error "No existe el compilador '$Cxx'." }
    $Cxx = $cmd.Source
} else {
    $Cxx = Find-Gpp
    if (-not $Cxx) {
        Write-Error ("No se encontro g++. Instala MinGW-w64 (o CLion) y agregalo al PATH, " +
                     "o indica la ruta: .\generar.ps1 -Cxx <ruta a g++.exe>")
    }
}
Write-Host "Usando $Cxx"
# MinGW necesita su carpeta bin en el PATH (DLLs de cc1plus); si no, falla sin mensaje.
$env:PATH = (Split-Path -Parent $Cxx) + ";" + $env:PATH

Write-Host "Compilando euler.cpp..."
& $Cxx -std=c++17 -O2 -Wall -Wextra euler.cpp -o euler.exe
if ($LASTEXITCODE -ne 0) { Write-Error "Fallo la compilacion de euler.cpp." }

# grafo de entrada -> traza de salida
$trazas = [ordered]@{
    "grafo_ejemplo.txt"   = "trace.json"
    "grafo_borde.txt"     = "trace_borde.json"
    "grafo_retroceso.txt" = "trace_retroceso.json"
}

foreach ($grafo in $trazas.Keys) {
    $traza = $trazas[$grafo]
    # cmd /c para que la redireccion no cambie la codificacion (PowerShell 5.1 escribiria UTF-16).
    cmd /c ".\euler.exe < $grafo > $traza"
    if ($LASTEXITCODE -ne 0) { Write-Error "euler.exe fallo con $grafo." }
    Write-Host "  $grafo -> $traza"
}

Write-Host "Listo. Renderiza con: python -m manim -pql animacion.py GrafoEuleriano"
