# scan_containment.sh - The lockdown every local `claude -p` session runs under.
# Source, don't run. Shared by run_scan_local.sh (the daily scan) and
# run_golden_local.sh (the weekly golden-set analyzer run), so both sessions
# get exactly the same tools, allow rules and denies. Rationale per rule:
# the header of run_scan_local.sh.

TOOLS="Read,Edit,Write,Glob,Grep,Bash,Task"
ALLOWED_TOOLS=(
  "Read" "Glob" "Grep" "Task" "Edit(data/**)"
  "Bash(python scripts/fetch_raw.py *)"
  "Bash(python scripts/merge_analysis.py)" "Bash(python scripts/verify_citations.py)"
  "Bash(python scripts/importance.py *)" "Bash(python scripts/promote_editorial.py)"
  "Bash(python scripts/readability.py --analysis)"
)
SETTINGS='{"permissions": {
  "blockReadsOutsideWorkingDirectories": true,
  "deny": [
    "Edit(scripts/**)", "Edit(.claude/**)", "Edit(.github/**)", "Edit(.git/**)",
    "Edit(.venv/**)", "Edit(tests/**)", "Edit(**/*.pth)", "Edit(*.toml)", "Edit(*.cfg)",
    "Edit(config.yaml)", "Edit(ISA.md)", "Edit(CLAUDE.md)", "Edit(AGENTS.md)",
    "Edit(data/_scan*)", "Edit(data/candidates.json)", "Edit(data/_raw/**)",
    "Edit(data/evals/**)", "Edit(data/_golden*)",
    "Edit(data/taxonomy.yaml)", "Edit(data/taxonomy_migration.json)",
    "Edit(data/taxonomy_proposals.json)",
    "Edit(data/news_stories.json)", "Edit(data/story_shortlist.json)",
    "Edit(data/_story_outcomes.md)", "Edit(data/_merge_outcomes.json)",
    "Edit(data/_editorial_outcomes.md)", "Edit(data/_curator_arxiv.json)",
    "Read(~/.ssh/**)", "Read(~/.claude/**)", "Read(~/.config/**)", "Read(~/.aws/**)",
    "Read(~/.gnupg/**)", "Read(.env)", "Read(.env.*)", "Read(data/_scan_backlog.json)",
    "Bash(curl *)", "Bash(wget *)", "Bash(git *)", "Bash(gh *)",
    "Bash(scripts/*)", "Bash(bash *)", "Bash(sh *)",
    "WebFetch", "WebSearch", "mcp__*"
  ]
}}'

# contained_claude <prompt> <system-prompt-file> <max_usd> <max_turns>
# Runs $CLAUDE locked down, SCAN_LOCKED=1, subscription billing only; its JSON
# result goes to stdout. A caller may tighten (never loosen) the settings by
# setting CONTAINED_SETTINGS to $SETTINGS with more denies (the golden run does).
contained_claude() {
  env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN SCAN_LOCKED=1 "$CLAUDE" -p "$1" \
    --append-system-prompt-file "$2" \
    --output-format json --permission-mode dontAsk \
    --setting-sources local --strict-mcp-config --mcp-config '{"mcpServers": {}}' \
    --tools "$TOOLS" --settings "${CONTAINED_SETTINGS:-$SETTINGS}" \
    --allowedTools "${ALLOWED_TOOLS[@]}" \
    --disallowedTools "mcp__*" \
    --max-budget-usd "$3" --max-turns "$4"
}
