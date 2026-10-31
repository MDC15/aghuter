# Installation

1. Extract `aghuter-0.3.1.zip`.
2. From your repository root, install for your target agent using the agent's documented skill directory. For Codex with Skills CLI:

   ```bash
   npx skills add ./aghuter --agent codex --copy
   ```

3. Check discovery in the agent and invoke `aghuter` using that agent's supported syntax.
4. Keep the skill updated by replacing the installed folder with the new release.

Project-level directory examples:

|| Agent | Directory (verify against current version) |
||---|---|
|| Codex | `.agents/skills/aghuter/` |
|| Claude Code | `.claude/skills/aghuter/` |
|| GitHub Copilot | `.github/skills/aghuter/` where supported |
|| OpenCode | See `adapters/opencode.md` |
|| Cursor | See `adapters/cursor.md` |
|| Gemini CLI | See `adapters/gemini-cli.md` |

The adapters are guidance, not installers or executable plugins. Always use the target agent's own permission and trust settings.