# Changelog

## v1.0.0 (2026-02-15)

**Initial Release**

### Features
- ✅ Automated PR reviews using Claude AI
- ✅ Inline comments on specific lines
- ✅ Configurable review depth (quick/balanced/deep)
- ✅ Multi-language support (EN, KO, ES, FR, DE)
- ✅ Context-aware reviews (reads PR description, commit messages)
- ✅ Rate limit handling with exponential backoff
- ✅ Customizable review prompts
- ✅ File ignore patterns
- ✅ Security, performance, and code quality checks

### Supported Languages
- Python
- JavaScript/TypeScript
- Go
- Rust
- Java
- C#
- PHP
- Ruby

### Models Supported
- Claude Sonnet 4
- Claude Opus 4
- Claude Haiku 4

### Cost Optimization
- Automatically skips PRs with > 10 files (configurable)
- Truncates large diffs to stay within token limits
- Uses efficient context window management

---

Built by **Jackson Studio**
