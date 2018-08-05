""" Project tasks """
from invoke import task, Collection
from invoke.tasks import call

NS = Collection()


@task
def setup(ctx, version="3", skip_lock=False):
    """ Create pipenv with target python version and install dependencies """
    skip_lock = "--skip-lock" if skip_lock else ""
    ctx.run("pipenv --python {}".format(version))
    ctx.run("pipenv install {} --dev".format(skip_lock))


NS.add_task(setup)


@task
def fmt(ctx):
    """ Format code """
    ctx.run("pipenv run black pycodeflow tests tasks.py setup.py")


NS.add_task(fmt)


@task
def lint(ctx):
    """ Lint code """
    ctx.run("pipenv run pylint pycodeflow tasks.py setup.py")


NS.add_task(lint)


@task(pre=[call(setup, version="2.7", skip_lock=True)])
def unit_test_two(ctx):
    """ Run unit tests in a 2.7 environment """
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")


@task(setup)
def unit_test_three(ctx):
    """ Run unit tests in a Python 3.x environment """
    ctx.run("pipenv run pytest --cov-report term-missing --cov=pycodeflow tests/")


UT = Collection("unit_test")
UT.add_task(unit_test_two, "two")
UT.add_task(unit_test_three, "three", default=True)
NS.add_collection(UT)


@task
def clean(ctx):
    """ Remove dist """
    ctx.run("rm -rf dist/")


NS.add_task(clean)


@task(clean)
def build(ctx):
    """ Build dist """
    ctx.run("pipenv run python setup.py sdist")


NS.add_task(build)


@task(build)
def release(ctx):
    """ Upload to pypi """
    ctx.run("pipenv run twine upload dist/*")


NS.add_task(release)


@task
def install_hooks(ctx):
    """ Install Pre-Commit pre-push hooks """
    ctx.run("pipenv run pre-commit install --hook-type pre-push")


NS.add_task(install_hooks)
