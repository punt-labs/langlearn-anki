# Changelog

## [Unreleased]

### Changed

- Migrate MCP server from `FastMCP` (mcp 1.x) to `MCPServer` (mcp 2.x).
  The `mcp.server.fastmcp.FastMCP` entry point was removed in mcp 2.0;
  the server now constructs `MCPServer(name, version=...)` and no longer
  touches the removed private `_mcp_server.version` attribute. Tool
  decorators and `run()` are unchanged.

### Fixed

- Require `mcp>=2`: the server imports `mcp.server.mcpserver.MCPServer`
  (mcp 2.x only), but the constraint still permitted mcp 1.x, so a resolver
  could install an incompatible 1.x and break the import at runtime.
- Action pin comments now state the version actually pinned. The SHA is
  the security control, but the comment is the only part a human reads,
  so a wrong one hides a stale pin from every review — how
  `gh-action-pypi-publish` broke punt-kit's 0.12.0 release. Labels
  resolved against the GitHub API, and no SHA was changed.

- Initial scaffolding for langlearn-anki.
- Added ROADMAP.md and refreshed README/DESIGN documentation.
