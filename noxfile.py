import nox


@nox.session(python=["3.6", "3.8", "3.10"], venv_backend="conda")
@nox.parametrize("pandas", ["1.1", "1.4.2"])
def tests(session, pandas):
    session.install(f'pandas=={pandas}')
    session.install("pytest") # could use raw unittest, pytest is much easier to read output of
    session.run('pytest')