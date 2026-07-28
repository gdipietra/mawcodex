<#
.SYNOPSIS
Run MAW Codex maintenance commands with an available Windows Python runtime.

.DESCRIPTION
Prefers Python on PATH, then the Python bundled with the Codex desktop
runtime. This wrapper changes no global settings and installs no dependencies.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("all", "validate", "test", "init", "install", "source-status")]
    [string] $Command = "all",

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]] $Arguments = @()
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

function Find-MawPython {
    foreach ($name in @("python3.exe", "python.exe")) {
        $candidate = Get-Command $name -ErrorAction SilentlyContinue
        if ($null -ne $candidate -and -not [string]::IsNullOrWhiteSpace($candidate.Source)) {
            return @{
                Executable = $candidate.Source
                Prefix = @()
            }
        }
    }

    $launcher = Get-Command "py.exe" -ErrorAction SilentlyContinue
    if ($null -ne $launcher -and -not [string]::IsNullOrWhiteSpace($launcher.Source)) {
        return @{
            Executable = $launcher.Source
            Prefix = @("-3")
        }
    }

    if (-not [string]::IsNullOrWhiteSpace($env:USERPROFILE)) {
        $bundled = Join-Path $env:USERPROFILE (
            ".cache\codex-runtimes\codex-primary-runtime\" +
            "dependencies\python\python.exe"
        )
        if (Test-Path -LiteralPath $bundled -PathType Leaf) {
            return @{
                Executable = $bundled
                Prefix = @()
            }
        }
    }

    throw (
        "No Python 3 runtime was found on PATH or in the Codex desktop " +
        "runtime. Install Python 3 or run the scripts with an explicit " +
        "interpreter."
    )
}

function Invoke-MawPython {
    param(
        [hashtable] $Runtime,
        [string[]] $PythonArguments
    )

    $fullArguments = @($Runtime.Prefix) + $PythonArguments
    & $Runtime.Executable @fullArguments |
        ForEach-Object { [Console]::Out.WriteLine([string] $_) }
    $processExitCode = $LASTEXITCODE
    return $processExitCode
}

$runtime = Find-MawPython
$env:PYTHONUTF8 = "1"

switch ($Command) {
    "validate" {
        $code = Invoke-MawPython -Runtime $runtime -PythonArguments @(
            (Join-Path $root "scripts\validate_package.py"),
            "--release"
        )
        exit $code
    }
    "test" {
        Push-Location $root
        try {
            $code = Invoke-MawPython -Runtime $runtime -PythonArguments @(
                "-m", "unittest", "discover", "-v"
            )
        }
        finally {
            Pop-Location
        }
        exit $code
    }
    "init" {
        if ($Arguments.Count -eq 0) {
            throw "init requires a destination path."
        }
        $pythonArguments = @(
            (Join-Path $root "scripts\init_project.py")
        ) + @($Arguments)
        $code = Invoke-MawPython -Runtime $runtime -PythonArguments $pythonArguments
        exit $code
    }
    "install" {
        $pythonArguments = @(
            (Join-Path $root "scripts\install_local_plugin.py")
        ) + @($Arguments)
        $code = Invoke-MawPython -Runtime $runtime -PythonArguments $pythonArguments
        exit $code
    }
    "source-status" {
        $pythonArguments = @(
            (Join-Path $root "scripts\check_source_clone.py")
        ) + @($Arguments)
        $code = Invoke-MawPython -Runtime $runtime -PythonArguments $pythonArguments
        exit $code
    }
    "all" {
        $code = Invoke-MawPython -Runtime $runtime -PythonArguments @(
            (Join-Path $root "scripts\run_release_gates.py")
        )
        exit $code
    }
}
