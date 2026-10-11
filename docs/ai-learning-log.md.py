# AI Learning Log

## Fellow: Daniel Okoh (Engineer B)

### Interaction #1 - .gitignore and git status
Problem: I didn't know what .gitignore actually does.
My initial understanding: I thought it was only a list of files, and I wasn't sure what it changed.
Prompt to AI: Asked how to configure the repo and what goes in .gitignore.
Useful AI guidance: Git skips files named in .gitignore, so they don't show up in git status.
My independent experiment/test: I created data/tickets.json and ran git status twice, once with the line in .gitignore and once with it removed.
Verification source or result: With the line, only .gitignore was listed. Without it, data/ appeared as untracked.
Decision: Accepted. I put the line back and committed .gitignore.
Related file/commit: .gitignore, commit ecef2ec
What I can now explain without AI: Git ignores any file or folder named in .gitignore, so each person's tickets.json stays on their own computer.

### Interaction #2 - for loops and return in find_ticket
Problem: My find_ticket function returned None even though the ticket existed.
My initial understanding: I