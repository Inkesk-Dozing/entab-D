import os
import re
import subprocess
import glob

issues_dir = r"c:\Users\USER\Desktop\Extras\pending-projects\entab-D\docs\issues"
issue_files = sorted(glob.glob(os.path.join(issues_dir, "00*.md")) + glob.glob(os.path.join(issues_dir, "010*.md")))

print(f"Found {len(issue_files)} issue files to publish:")
for f in issue_files:
    print(os.path.basename(f))

created_issues = []

for file_path in issue_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    
    # Extract title from line 1
    raw_title = lines[0].replace("# ", "").strip()
    # E.g. "Issue 001: [FIX] Unify..." -> "fix: unify..."
    match = re.search(r"Issue\s+\d+:\s*\[(FIX|FEAT|SEC|PERF|UI/UX|CHORE|TEST|AI-FEAT)\]\s*(.*)", raw_title, re.IGNORECASE)
    if match:
        tag = match.group(1).lower()
        if tag == "ai-feat":
            tag = "feat(ai)"
        title = f"{tag}: {match.group(2)}"
    else:
        title = raw_title

    # Extract labels from line containing **Labels**:
    labels = []
    body_start_idx = 1
    for i, line in enumerate(lines[:10]):
        if "**Labels**:" in line:
            labels = re.findall(r"`([^`]+)`", line)
            body_start_idx = i + 1
            break
            
    # Clean body: strip leading horizontal rules or blank lines
    while body_start_idx < len(lines) and (lines[body_start_idx].strip() in ["---", ""] or not lines[body_start_idx].strip()):
        body_start_idx += 1
        
    body = "\n".join(lines[body_start_idx:]).strip()

    cmd = ["gh", "issue", "create", "--title", title, "--body", body, "--repo", "Inkesk-Dozing/entab-D"]
    for l in labels:
        cmd.extend(["--label", l])

    print(f"\nCreating issue: {title}")
    print(f"Labels: {labels}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        url = res.stdout.strip()
        print(f"Success: {url}")
        created_issues.append((title, url, labels))
    else:
        print(f"Error: {res.stderr.strip()}")

print("\n--- Summary of Created Issues ---")
for t, u, l in created_issues:
    print(f"- {t} -> {u} ({', '.join(l)})")
