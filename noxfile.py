# Default invocation to run tests:  nox -r -db mamba (re-use environments, using mamba to supply virtualenvs)
# Note virtualenv will need python 3.6, 3.8, 3.10 on path to work, hence mamba is easier

import nox
from nox import Session

USE_CONDA = True


def install_wrapper(session: Session, *args, **kwargs):
    if USE_CONDA:
        session.conda_install(*args, **kwargs, channel="conda-forge")
    else:
        session.install(*args, **kwargs)


# @nox.session(python=["3.6", "3.8", "3.10"], reuse_venv=True)
@nox.session(reuse_venv=True)
@nox.parametrize(
    "python,pandas",
    [
        ("3.6", "1.0.5"),
        ("3.8", "1.4.4"),
        ("3.8", None),
        ("3.10", "1.4.4"),
        ("3.10", None),
    ],
)
def tests(session: Session, pandas):  # Note python not in args, this is correct, intercepted by nox
    print(session.python)
    if pandas is None:
        install_wrapper(session, "pandas")  # 1.4.2 and (1.1.5 for python 3.6)
    else:
        install_wrapper(session, f"pandas=={pandas}")
    session.install(".")
    install_wrapper(session, "pytest")
    session.run("pytest")
