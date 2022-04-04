# Default invocation to run tests:  nox -r -db mamba (re-use environments, using mamba to supply virtualenvs)
# Note virtualenv will need python 3.6, 3.8, 3.10 on path to work, hence mamba is easier

import nox
from nox import Session


@nox.session(python=["3.6", "3.8", "3.10"], reuse_venv=True)
@nox.parametrize("pandas", ["1.1", None], ids=['pd11', 'pd_latest']
                 )
def tests(session: Session, pandas):
    print(session.python)
    if pandas is None:
        session.install("pandas")  # 1.4.2 and (1.1.5 for python 3.6)
    else:
        session.install(f'pandas=={pandas}')
    session.install(".")
    session.install("pytest") # could use raw unittest, pytest is much easier to read output of
    session.run('pytest')