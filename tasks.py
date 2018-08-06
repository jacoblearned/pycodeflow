""" Project tasks """
from invoke import task, Collection
from invoke.executor import Executor

ns = Collection()  # pylint: disable=invalid-name


@task
def setup(ctx, version="3", skip_lock=False):
    """ Create pipenv with target python version and install dependencies """
    skip_lock = "--skip-lock" if skip_lock else ""
    ctx.run("pipenv --python {}".format(version))
    ctx.run("pipenv install {} --dev".format(skip_lock))


ns.add_task(setup)


@task
def fmt(ctx):
    """ Format code """
    ctx.run("pipenv run black pycodeflow tests tasks.py setup.py")


ns.add_task(fmt)


@task
def lint(ctx):
    """ Lint code """
    ctx.run("pipenv run pylint pycodeflow tasks.py setup.py")


ns.add_task(lint)


@task
def unit_test(ctx, version="3", setup=False):  # pylint: disable=redefined-outer-name
    """ Run unit tests for the desired python version """
    if setup:
        Executor(ns).execute(("setup", {"version": version, "skip_lock": True}))
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")


ns.add_task(unit_test)


@task
def clean(ctx):
    """ Remove dist """
    ctx.run("rm -rf dist/")


ns.add_task(clean)


@task(clean)
def build(ctx):
    """ Build dist """
    ctx.run("pipenv run python setup.py sdist")


ns.add_task(build)


@task(build)
def release(ctx):
    """ Upload to pypi """
    ctx.run("pipenv run twine upload dist/*")


ns.add_task(release)


@task
def install_hooks(ctx):
    """ Install Pre-Commit pre-push hooks """
    ctx.run("pipenv run pre-commit install --hook-type pre-push")


ns.add_task(install_hooks)
