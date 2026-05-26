# Changelog

All notable changes to the Strategic Consulting Harness are documented here.

## [0.2.0] - 2026-05-25

### Fixed
- `validator/_util.py` `body_lines()` now skips HTML comment blocks (`<!-- ... -->`),
  eliminating false-positive `claim_label_present` and `label_producer_binding` violations
  when artifacts are drafted directly from templates (CR-2026-001)

### Changed
- `templates/situation.template.md` and `templates/retro.template.md` now include a visible
  author note warning against using claim-label names inside square brackets in descriptive
  prose (CR-2026-002)

## [0.1.0] - 2026-05-25

### Added
- Harness repo skeleton: directories for templates, prompts, validator, mcp, harness, backlog
- CHANGELOG.md and README.md
- design-principles.md as the binding design contract (repo root)
