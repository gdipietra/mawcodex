# Cross-platform Windows hook runner for MAW Codex.
#
# The POSIX-equivalent implementation is maw_hook.py. These hooks are
# defense-in-depth and fail open on internal errors. Denials are limited to a
# small, reviewable set of destructive Git commands.

$ErrorActionPreference = "Stop"

$script:CodeExtensions = @(".r", ".rmd", ".qmd", ".do", ".py", ".jl")
$script:AnalysisPath = '(?i)(^|/)scripts/.*\.(r|rmd|do|py|jl)$|(^|/)scripts/.*/_outputs/'
$script:MachinePath = '(/Users/[^/\s''"\)]+|/home/[^/\s''"\)]+|[A-Za-z]:\\Users\\[^\\\s''"]+)'
$script:PatchPath = '(?m)^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$'
$script:ThrottleSeconds = 300
$script:GitDenials = @{
    reset = @{
        Reason = "git reset --hard irreversibly discards uncommitted work."
        Alternative = "Use a stash or reset only explicitly named paths."
    }
    clean = @{
        Reason = "git clean with force deletes untracked files, including untracked data."
        Alternative = "Inspect with git clean -n and remove only verified targets."
    }
    push = @{
        Reason = "git push --force can clobber remote history."
        Alternative = "Use --force-with-lease only after reviewing the exact branch state."
    }
    add = @{
        Reason = "Blanket staging can include data, secrets, or local settings."
        Alternative = "Stage explicit reviewed paths."
    }
    restore = @{
        Reason = "Mass working-tree discard is difficult to recover."
        Alternative = "Restore explicit files or preserve changes in a stash."
    }
}
$script:GlobalGitOptionsWithValue = @(
    "-c",
    "--config-env",
    "--exec-path",
    "--git-dir",
    "--namespace",
    "--super-prefix",
    "--work-tree"
)

function Write-HookJson {
    param([Parameter(Mandatory = $true)] [hashtable] $Payload)

    [Console]::Out.Write(($Payload | ConvertTo-Json -Depth 10 -Compress))
}

function Test-Property {
    param(
        [object] $Object,
        [string] $Name
    )

    return $null -ne $Object -and
        $null -ne $Object.PSObject.Properties[$Name]
}

function Get-PropertyText {
    param(
        [object] $Object,
        [string] $Name
    )

    if (-not (Test-Property -Object $Object -Name $Name)) {
        return ""
    }
    $value = $Object.PSObject.Properties[$Name].Value
    if ($value -is [string]) {
        return $value
    }
    return ""
}

function Get-ProjectRoot {
    param([string] $Start)

    if ([string]::IsNullOrWhiteSpace($Start)) {
        $Start = (Get-Location).Path
    }
    $current = [IO.DirectoryInfo]::new([IO.Path]::GetFullPath($Start))
    while ($null -ne $current) {
        if (Test-Path -LiteralPath (Join-Path $current.FullName ".git")) {
            return $current.FullName
        }
        $current = $current.Parent
    }
    return [IO.Path]::GetFullPath($Start)
}

function Get-StateDirectory {
    param([string] $Root)

    $base = $env:PLUGIN_DATA
    if ([string]::IsNullOrWhiteSpace($base)) {
        $base = Join-Path ([IO.Path]::GetTempPath()) "mawcodex-plugin-data"
    }
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [Text.Encoding]::UTF8.GetBytes($Root)
        $hash = [BitConverter]::ToString($sha.ComputeHash($bytes)).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
    $directory = Join-Path (Join-Path $base "sessions") $hash.Substring(0, 16)
    [IO.Directory]::CreateDirectory($directory) | Out-Null
    return $directory
}

function Get-ChangedPaths {
    param([object] $ToolInput)

    $paths = [Collections.Generic.List[string]]::new()
    $explicit = Get-PropertyText -Object $ToolInput -Name "file_path"
    if (-not [string]::IsNullOrWhiteSpace($explicit)) {
        $paths.Add($explicit.Trim())
    }
    $command = Get-PropertyText -Object $ToolInput -Name "command"
    if (-not [string]::IsNullOrWhiteSpace($command)) {
        foreach ($match in [regex]::Matches($command, $script:PatchPath)) {
            $paths.Add($match.Groups[1].Value.Trim())
        }
    }

    $normalized = [Collections.Generic.List[string]]::new()
    foreach ($path in $paths) {
        $portable = $path.Replace("\", "/")
        while ($portable.StartsWith("./")) {
            $portable = $portable.Substring(2)
        }
        if (-not [string]::IsNullOrWhiteSpace($portable) -and
            -not $normalized.Contains($portable)) {
            $normalized.Add($portable)
        }
    }
    return $normalized.ToArray()
}

function Get-AddedPatchText {
    param([string] $Command)

    $added = foreach ($line in ($Command -split "`r?`n")) {
        if ($line.StartsWith("+") -and -not $line.StartsWith("+++")) {
            $line.Substring(1)
        }
    }
    return ($added -join "`n")
}

function Split-ShellSegments {
    param([string] $Command)

    $segments = [Collections.Generic.List[string]]::new()
    $current = [Text.StringBuilder]::new()
    $quote = $null
    $escaped = $false
    foreach ($character in $Command.ToCharArray()) {
        if ($escaped) {
            [void] $current.Append($character)
            $escaped = $false
            continue
        }
        if ($character -eq "\" -or $character -eq "``") {
            [void] $current.Append($character)
            $escaped = $true
            continue
        }
        if ($null -ne $quote) {
            [void] $current.Append($character)
            if ($character -eq $quote) {
                $quote = $null
            }
            continue
        }
        if ($character -eq "'" -or $character -eq '"') {
            [void] $current.Append($character)
            $quote = $character
            continue
        }
        if (";&|`r`n()".Contains([string] $character)) {
            $segment = $current.ToString().Trim()
            if (-not [string]::IsNullOrWhiteSpace($segment)) {
                $segments.Add($segment)
            }
            [void] $current.Clear()
            continue
        }
        [void] $current.Append($character)
    }
    $segment = $current.ToString().Trim()
    if (-not [string]::IsNullOrWhiteSpace($segment)) {
        $segments.Add($segment)
    }
    return $segments.ToArray()
}

function ConvertTo-ShellTokens {
    param([string] $Segment)

    $tokens = [Collections.Generic.List[string]]::new()
    $current = [Text.StringBuilder]::new()
    $quote = $null
    $escaped = $false
    foreach ($character in $Segment.ToCharArray()) {
        if ($escaped) {
            [void] $current.Append($character)
            $escaped = $false
            continue
        }
        if ($character -eq "\" -or $character -eq "``") {
            $escaped = $true
            continue
        }
        if ($null -ne $quote) {
            if ($character -eq $quote) {
                $quote = $null
            }
            else {
                [void] $current.Append($character)
            }
            continue
        }
        if ($character -eq "'" -or $character -eq '"') {
            $quote = $character
            continue
        }
        if ([char]::IsWhiteSpace($character)) {
            if ($current.Length -gt 0) {
                $tokens.Add($current.ToString())
                [void] $current.Clear()
            }
            continue
        }
        [void] $current.Append($character)
    }
    if ($current.Length -gt 0) {
        $tokens.Add($current.ToString())
    }
    return $tokens.ToArray()
}

function Test-GitExecutable {
    param([string] $Token)

    $parts = $Token.Replace("\", "/").Split("/")
    $leaf = $parts[$parts.Length - 1].ToLowerInvariant()
    return $leaf -in @("git", "git.exe")
}

function Get-GitInvocation {
    param(
        [string[]] $Tokens,
        [int] $GitIndex
    )

    $index = $GitIndex + 1
    while ($index -lt $Tokens.Count) {
        $token = $Tokens[$index]
        $lowered = $token.ToLowerInvariant()
        if ($script:GlobalGitOptionsWithValue -contains $lowered) {
            $index += 2
            continue
        }
        $hasAttachedValue = (
            $lowered.StartsWith("-c") -and $token.Length -gt 2
        )
        if (-not $hasAttachedValue) {
            foreach ($option in $script:GlobalGitOptionsWithValue) {
                if ($option.StartsWith("--") -and
                    $lowered.StartsWith($option + "=")) {
                    $hasAttachedValue = $true
                    break
                }
            }
        }
        if ($hasAttachedValue) {
            $index += 1
            continue
        }
        if ($token.StartsWith("-")) {
            $index += 1
            continue
        }
        $arguments = if ($index + 1 -lt $Tokens.Count) {
            @($Tokens[($index + 1)..($Tokens.Count - 1)])
        }
        else {
            @()
        }
        return [pscustomobject] @{
            Subcommand = $lowered
            Arguments = $arguments
        }
    }
    return $null
}

function Test-ShortFlag {
    param(
        [string[]] $Arguments,
        [string] $Flag
    )

    foreach ($argument in $Arguments) {
        if ($argument.StartsWith("-") -and
            -not $argument.StartsWith("--") -and
            $argument.Substring(1).ToLowerInvariant().Contains(
                $Flag.ToLowerInvariant()
            )) {
            return $true
        }
    }
    return $false
}

function Get-GitDenial {
    param([string] $Command)

    foreach ($segment in @(Split-ShellSegments -Command $Command)) {
        $tokens = @(ConvertTo-ShellTokens -Segment $segment)
        for ($index = 0; $index -lt $tokens.Count; $index++) {
            if (-not (Test-GitExecutable -Token $tokens[$index])) {
                continue
            }
            $invocation = Get-GitInvocation -Tokens $tokens -GitIndex $index
            if ($null -eq $invocation) {
                continue
            }
            $arguments = @($invocation.Arguments)
            $loweredArguments = @(
                $arguments | ForEach-Object { $_.ToLowerInvariant() }
            )
            switch ($invocation.Subcommand) {
                "reset" {
                    if ($loweredArguments -contains "--hard") {
                        return $script:GitDenials.reset
                    }
                }
                "clean" {
                    if ($loweredArguments -contains "--force" -or
                        (Test-ShortFlag -Arguments $arguments -Flag "f")) {
                        return $script:GitDenials.clean
                    }
                }
                "push" {
                    if ($loweredArguments -contains "--force" -or
                        (Test-ShortFlag -Arguments $arguments -Flag "f")) {
                        return $script:GitDenials.push
                    }
                }
                "add" {
                    if (@(
                        $loweredArguments |
                            Where-Object { $_ -in @("-a", "--all", ".", ":/") }
                    ).Count -gt 0) {
                        return $script:GitDenials.add
                    }
                }
                { $_ -in @("checkout", "restore") } {
                    if ($arguments -contains ".") {
                        return $script:GitDenials.restore
                    }
                }
            }
        }
    }
    return $null
}

function Write-Denial {
    param([string] $Reason)

    Write-HookJson @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "deny"
            permissionDecisionReason = $Reason
        }
    }
}

function Invoke-PreToolUse {
    param([object] $Data)

    $tool = Get-PropertyText -Object $Data -Name "tool_name"
    $toolInput = if (Test-Property -Object $Data -Name "tool_input") {
        $Data.tool_input
    }
    else {
        [pscustomobject] @{}
    }
    $command = Get-PropertyText -Object $toolInput -Name "command"

    if ($tool -eq "Bash") {
        $guardrail = Get-GitDenial -Command $command
        if ($null -ne $guardrail) {
            Write-Denial -Reason (
                "Blocked by MAW Codex guardrails: " +
                $guardrail.Reason + " " + $guardrail.Alternative
            )
            return
        }
    }

    if ($tool -notin @("apply_patch", "Edit", "Write")) {
        return
    }

    $candidates = @(Get-ChangedPaths -ToolInput $toolInput)
    $parts = [Collections.Generic.List[string]]::new()
    foreach ($key in @("content", "new_string")) {
        $value = Get-PropertyText -Object $toolInput -Name $key
        if (-not [string]::IsNullOrWhiteSpace($value)) {
            $parts.Add($value)
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($command)) {
        $parts.Add((Get-AddedPatchText -Command $command))
    }
    $content = $parts -join "`n"
    $pathMatch = [regex]::Match($content, $script:MachinePath)
    $codeTargets = @(
        $candidates | Where-Object {
            $script:CodeExtensions -contains [IO.Path]::GetExtension($_).ToLowerInvariant()
        }
    )
    if (-not $pathMatch.Success -or $codeTargets.Count -eq 0) {
        return
    }

    $message = (
        "Hardcoded machine path '{0}' in {1} breaks portable replication. " +
        "Use project-relative paths or a documented configuration."
    ) -f $pathMatch.Value, ($codeTargets -join ", ")
    if ($env:MAWCODEX_STRICT_PATHS -eq "1") {
        Write-Denial -Reason ("Blocked by MAWCODEX_STRICT_PATHS=1: " + $message)
    }
    else {
        Write-HookJson @{
            hookSpecificOutput = @{
                hookEventName = "PreToolUse"
                additionalContext = $message
            }
        }
    }
}

function Get-RelativePath {
    param(
        [string] $Path,
        [string] $Root
    )

    if ([IO.Path]::IsPathRooted($Path)) {
        $rootPrefix = [IO.Path]::GetFullPath($Root).TrimEnd("\", "/") + [IO.Path]::DirectorySeparatorChar
        $full = [IO.Path]::GetFullPath($Path)
        if ($full.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
            return $full.Substring($rootPrefix.Length).Replace("\", "/")
        }
    }
    $portable = $Path.Replace("\", "/")
    while ($portable.StartsWith("./")) {
        $portable = $portable.Substring(2)
    }
    return $portable
}

function Invoke-PostToolUse {
    param([object] $Data)

    if (-not (Test-Property -Object $Data -Name "tool_input")) {
        return
    }
    $root = Get-ProjectRoot -Start (Get-PropertyText -Object $Data -Name "cwd")
    $paths = @(
        Get-ChangedPaths -ToolInput $Data.tool_input |
            ForEach-Object { Get-RelativePath -Path $_ -Root $root }
    )
    $watched = @($paths | Where-Object { $_ -match $script:AnalysisPath })
    if ($watched.Count -eq 0) {
        return
    }

    $passportDirectory = Join-Path (Join-Path $root "quality_reports") "passports"
    if (-not (Test-Path -LiteralPath $passportDirectory)) {
        return
    }
    $passports = @(Get-ChildItem -LiteralPath $passportDirectory -Filter "*.yaml" -File)
    if ($passports.Count -eq 0) {
        return
    }

    $stateFile = Join-Path (Get-StateDirectory -Root $root) "claim-reconcile-state.json"
    $throttle = @{}
    if (Test-Path -LiteralPath $stateFile) {
        try {
            $loaded = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
            foreach ($property in $loaded.PSObject.Properties) {
                $throttle[$property.Name] = [double] $property.Value
            }
        }
        catch {
            $throttle = @{}
        }
    }

    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    $messages = [Collections.Generic.List[string]]::new()
    foreach ($changed in $watched) {
        if ($throttle.ContainsKey($changed) -and
            ($now - [double] $throttle[$changed]) -lt $script:ThrottleSeconds) {
            continue
        }
        $affected = [Collections.Generic.List[string]]::new()
        $total = 0
        foreach ($passport in $passports) {
            $hits = 0
            foreach ($line in [IO.File]::ReadLines($passport.FullName)) {
                if (($line.Contains("source_file") -or $line.Contains("output_file")) -and
                    $line.Contains($changed)) {
                    $hits += 1
                }
            }
            if ($hits -gt 0) {
                $affected.Add(("{0} ({1})" -f $passport.Name, $hits))
                $total += $hits
            }
        }
        if ($affected.Count -eq 0) {
            continue
        }
        $throttle[$changed] = $now
        $messages.Add(
            ("{0} changed; {1} passport claim(s) may be STALE in {2}." -f
                $changed, $total, ($affected -join ", "))
        )
    }
    if ($messages.Count -eq 0) {
        return
    }

    try {
        [IO.File]::WriteAllText(
            $stateFile,
            ($throttle | ConvertTo-Json -Depth 4),
            [Text.UTF8Encoding]::new($false)
        )
    }
    catch {
        # The warning is still useful when persistence is unavailable.
    }
    $message = $messages -join " "
    Write-HookJson @{
        systemMessage = $message
        hookSpecificOutput = @{
            hookEventName = "PostToolUse"
            additionalContext = (
                $message +
                " Run `$audit-reproducibility before relying on or publishing " +
                "affected numeric claims."
            )
        }
    }
}

function Get-ActivePlan {
    param([string] $Root)

    $directory = Join-Path (Join-Path $Root "quality_reports") "plans"
    if (-not (Test-Path -LiteralPath $directory)) {
        return $null
    }
    $plans = @(
        Get-ChildItem -LiteralPath $directory -Filter "*.md" -File |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 5
    )
    foreach ($plan in $plans) {
        $content = Get-Content -Raw -LiteralPath $plan.FullName
        $statusMatch = [regex]::Match(
            $content,
            '(?im)^\s*\**\s*status\s*\**\s*:\s*\**\s*(draft|approved|completed|implemented|in[ -]?progress)'
        )
        $status = if ($statusMatch.Success) {
            $statusMatch.Groups[1].Value.ToLowerInvariant().Replace(" ", "_")
        }
        else {
            "in_progress"
        }
        if ($status -in @("completed", "implemented")) {
            continue
        }
        $taskMatch = [regex]::Match($content, '(?m)^.*- \[ \]\s*(.+)$')
        $task = if ($taskMatch.Success) { $taskMatch.Groups[1].Value.Trim() } else { $null }
        return @{
            path = $plan.FullName
            name = $plan.Name
            status = $status
            current_task = $task
        }
    }
    return $null
}

function Get-RecentSessionLog {
    param([string] $Root)

    $directory = Join-Path (Join-Path $Root "quality_reports") "session_logs"
    if (-not (Test-Path -LiteralPath $directory)) {
        return $null
    }
    $log = Get-ChildItem -LiteralPath $directory -Filter "*.md" -File |
        Sort-Object LastWriteTimeUtc -Descending |
        Select-Object -First 1
    if ($null -ne $log) {
        return $log.FullName
    }
    return $null
}

function Invoke-PreCompact {
    param([object] $Data)

    $root = Get-ProjectRoot -Start (Get-PropertyText -Object $Data -Name "cwd")
    $state = @{
        saved_at = [DateTimeOffset]::UtcNow.ToString("o")
        trigger = Get-PropertyText -Object $Data -Name "trigger"
        plan = Get-ActivePlan -Root $root
        session_log = Get-RecentSessionLog -Root $root
    }
    $stateFile = Join-Path (Get-StateDirectory -Root $root) "pre-compact-state.json"
    [IO.File]::WriteAllText(
        $stateFile,
        ($state | ConvertTo-Json -Depth 8),
        [Text.UTF8Encoding]::new($false)
    )
    Write-HookJson @{
        continue = $true
        systemMessage = (
            "MAW Codex saved the active plan and session-log pointers " +
            "before compaction."
        )
    }
}

function Invoke-SessionStart {
    param([object] $Data)

    $source = Get-PropertyText -Object $Data -Name "source"
    if ($source -notin @("compact", "resume")) {
        return
    }
    $root = Get-ProjectRoot -Start (Get-PropertyText -Object $Data -Name "cwd")
    $stateFile = Join-Path (Get-StateDirectory -Root $root) "pre-compact-state.json"
    $saved = $null
    if (Test-Path -LiteralPath $stateFile) {
        try {
            $saved = Get-Content -Raw -LiteralPath $stateFile | ConvertFrom-Json
            Remove-Item -LiteralPath $stateFile -Force
        }
        catch {
            $saved = $null
        }
    }

    $plan = Get-ActivePlan -Root $root
    if ($null -eq $plan -and $null -ne $saved -and
        (Test-Property -Object $saved -Name "plan")) {
        $plan = $saved.plan
    }
    $sessionLog = Get-RecentSessionLog -Root $root
    $savedLog = if ($null -ne $saved) {
        Get-PropertyText -Object $saved -Name "session_log"
    }
    else {
        ""
    }
    if ($null -eq $plan -and
        [string]::IsNullOrWhiteSpace($sessionLog) -and
        [string]::IsNullOrWhiteSpace($savedLog)) {
        return
    }

    $lines = [Collections.Generic.List[string]]::new()
    $lines.Add("MAW Codex context restoration:")
    $lines.Add("- Re-read the applicable AGENTS.md and active workflow skill.")
    if ($null -ne $plan) {
        if ($plan -is [Collections.IDictionary]) {
            $planPath = if ($plan["path"]) { $plan["path"] } else { $plan["name"] }
            $planStatus = if ($plan["status"]) { $plan["status"] } else { "unknown" }
            $currentTask = $plan["current_task"]
        }
        else {
            $planPath = if ($plan.path) { $plan.path } else { $plan.name }
            $planStatus = if ($plan.status) { $plan.status } else { "unknown" }
            $currentTask = $plan.current_task
        }
        $lines.Add(("- Active plan: {0} ({1})." -f $planPath, $planStatus))
        if (-not [string]::IsNullOrWhiteSpace([string] $currentTask)) {
            $lines.Add(("- Next unchecked item: {0}" -f $currentTask))
        }
    }
    if (-not [string]::IsNullOrWhiteSpace($sessionLog)) {
        $lines.Add(("- Most recent session log: {0}" -f $sessionLog))
    }
    elseif (-not [string]::IsNullOrWhiteSpace($savedLog)) {
        $lines.Add(("- Saved session-log pointer: {0}" -f $savedLog))
    }
    $lines.Add(
        "- Inspect current git status and diff before continuing; do not " +
        "assume saved state is current."
    )

    Write-HookJson @{
        hookSpecificOutput = @{
            hookEventName = "SessionStart"
            additionalContext = $lines -join "`n"
        }
    }
}

try {
    $raw = [Console]::In.ReadToEnd()
    $data = if ([string]::IsNullOrWhiteSpace($raw)) {
        [pscustomobject] @{}
    }
    else {
        $raw | ConvertFrom-Json
    }
    $event = Get-PropertyText -Object $data -Name "hook_event_name"
    switch ($event) {
        "PreToolUse" { Invoke-PreToolUse -Data $data }
        "PostToolUse" { Invoke-PostToolUse -Data $data }
        "PreCompact" { Invoke-PreCompact -Data $data }
        "SessionStart" { Invoke-SessionStart -Data $data }
    }
}
catch {
    # Fail open: a helper malfunction must not block Codex.
}

exit 0
