""" Project tasks """
from invoke import task


@task
def setup(ctx, version="3"):
    """ Create pipenv with target python version and install dependencies """
    ctx.run("pipenv --python {}".format(version))
    ctx.run("pipenv install --dev")


@task
def fmt(ctx):
    """ Format code """
    ctx.run("pipenv run black pycodeflow tests tasks.py setup.py")


@task
def lint(ctx):
    """ Lint code """
    ctx.run("pipenv run pylint pycodeflow tasks.py setup.py")


@task
def unit_test(ctx):
    """ Run unit tests """
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")


@task
def clean(ctx):
    """ Remove dist """
    ctx.run("rm -rf dist/")


@task(clean)
def build(ctx):
    """ Build dist """
    ctx.run("pipenv run python setup.py sdist")


@task(build)
def release(ctx):
    """ Upload to pypi """
    ctx.run("pipenv run twine upload dist/*")


@task
def install_hooks(ctx):
    """ Install Pre-Commit pre-push hooks """
    ctx.run("pipenv run pre-commit install --hook-type pre-push")
