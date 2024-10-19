# Testing
Tests are set up to use nox - see `noxfile.py` for details
- These parametrise over python versions
- These parametrise over a subset of pandas versions
- Tests can be run on a discrete environment directly to investigate specific compatibility
- Tests are written in unit test style as backwards compatibility for an internal codebase which still uses unittest

# Release process

Releases are done using (Flit)[https://flit.pypa.io/en/latest/] and normally consist of the following steps
1. Merge all release PRs into master
2. Update CHANGELOG.md
3. Run nox based test suite
4. Run ruff format over codebase (uvx ruff format --line-length=120 .)
5. Make release commit by updating `__version__` in `table_builer_io.__init__.py` e.g. "RLS: release 0.x.y"
6. Run `flit publish` - this builds an sdist and wheel and uploads the package to PyPI
7. Tag the release locally: `git tag vx.x.x`
8. Upload commit and tags: `git push` and `git push origin <vx.x.x>`