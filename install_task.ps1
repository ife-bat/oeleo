#Requires -RunAsAdministrator

param(
    [string]$TaskName = "OeleoRunner",
    [string]$DelayMinutes = "5"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$exePath = Join-Path $scriptDir "dist\oeleo_runner.exe"

if (-not (Test-Path $exePath)) {
    Write-Error "Cannot find executable at: $exePath"
    exit 1
}

$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Task '$TaskName' already exists. Removing it first..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# AtStartup runs the worker even before any user logs on.
# The app detects whether a desktop is available and falls back
# to headless (LogReporter) when there is no interactive session.
$trigger = New-ScheduledTaskTrigger -AtStartup
$trigger.Delay = "PT${DelayMinutes}M"

$action = New-ScheduledTaskAction `
    -Execute $exePath `
    -WorkingDirectory $scriptDir

# S4U logon lets the task run whether the user is logged on or not,
# without needing to store the password.
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Days 0)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Trigger $trigger `
    -Action $action `
    -Principal $principal `
    -Settings $settings `
    -Description "Runs oeleo file-transfer service at system startup (headless if no user is logged on)." |
    Out-Null

Write-Host ""
Write-Host "Scheduled task '$TaskName' created successfully." -ForegroundColor Green
Write-Host "  Trigger : at startup with ${DelayMinutes}-minute delay"
Write-Host "  Action  : $exePath"
Write-Host "  Work dir: $scriptDir"
Write-Host ""
Write-Host "The app runs headless (log only) when no desktop session is available,"
Write-Host "and shows the system tray icon when started interactively."
Write-Host ""
Write-Host "You can verify in Task Scheduler or run:"
Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Format-List"
