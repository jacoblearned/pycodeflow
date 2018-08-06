""" Project tasks """
from invoke import task, Collection
from invoke.tasks import call

ns = Collection()   # pylint: disable=invalid-name

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


@task(pre=[call(setup, version="2.7", skip_lock=True)])
def unit_test_two(ctx):
    """ Run unit tests in a 2.7 environment """
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")

@task(setup)
def unit_test_three(ctx):
    """ Run unit tests in a Python 3.x environment """
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")

unit_test = Collection('unit_test') # pylint: disable=invalid-name
unit_test.add_task(unit_test_two, "two")
unit_test.add_task(unit_test_three, "three", default=True)
ns.add_collection(unit_test)

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
