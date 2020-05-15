# Backend: Python Unit Test

Currently we uses Python Unit Test tools to create unit test.

## How it works

The directory `fixtures/tests` is a python module called `tests`.
It's primary focus is to run python unit tests.
The `tests.backend` module serves as a module to test the backend only.
The `tests.utils` module serve as helper library to aid unit testing.

This module is used by importing `fixtures/tests` directory in `PYTHONPATH` environment variable.
For backend testing, we mainly uses `psycopg2` module to connect to the database.
We want to test native functional tests of SQL functions, to make sure it works natively before other service tests it.

For common use case, we provided `DatabaseTestCase` class that inherits from `unittest.TestCase` class.
It contains some helpers method to make it easier to connect to the database, 
perform SQL operations and to validate it with JSON file.

## How to run the tests manually

The best way to run the test is from inside the container where all the 
environment variables are provided.

From the backend root dir `docker-osm/indonesia-buildings` you can execute:

```bash
make shell
```

To get inside the bash shell in `db` container.

You might already know that to run a `unittest` unit test, you need to run this command from the `fixtures`
directory:

```bash
python3 -m unittest discover -v
```

The `-v` flag is to display some verbose logs.

To run individual test, just specify the module or class or method name:

```bash
# run tests in `tests.backend.test_building_impact` module
python3 -m unittest tests.backend.test_building_impact -v

# run tests in `TestBuildingImpact` class in `tests.backend.test_building_impact` module
python3 -m unittest tests.backend.test_building_impact.TestBuildingImpact -v

# run tests for method name `test_building_summary` in a 
# class called `TestBuildingImpact` in a module called `tests.backend.test_building_impact`
python3 -m unittest tests.backend.test_building_impact.TestBuildingImpact.test_building_summary -v

```

If the test fails, it will print out the name of the failed tests and the failed assertions.
Refer to Python Unittest documentations for more detail and testing framework in general.

## Advanced testing inspections using PyCharm Debugger

For this advanced topic, if you have PyCharm Professional edition you could debug unittest 
using PyCharm Debug Configuration tools.

1. Setup Project Interpreters

In concept, your python interpreter is inside the `db` container. The container is equipped
with an SSH Daemon, so you add new Remote Interpreter using PyCharm with the following credentials

```ini
Host: localhost
Port: <value from SSHD_PORT, by default 222>
User: root
Password: docker
Python interpreter path: /usr/bin/python3

```

Additionally, to help you discover the source code, map your repo to container path.
In Path mappings, add mapping from `REPO ROOT` to `/opt/inasafe-fba`.
Put the actual path of `REPO ROOT`, not the text.
For example, in my computer, `REPO ROOT` is on `/Users/lucernae/Documents/WorkingDir/Projects/InaSAFE/inasafe-fba`
You get this path by exploring using file browser provided by PyCharm to locate your repo directory.
Or by typing

```bash
echo $PWD
```

in the command line, from the `REPO ROOT` directory.


2. Setup Run Configuration

To set it up quickly, right click over the name of the module, or class, or even method name.
It will open a context menu, click `Run <name of the object>`.
PyCharm will create a new Run profile.
It will not run, however because you don't yet provide necessary informations for it to run.

Go into Run > Edit configuration menu.
Pick you newly configured unittest profile.

Choose `Module name` target

Fill in the target that you want to test (Full module path of the object)

Fill in the environment variable.
For backend unit testing, these variables are needed:

```ini
PYTHONPATH=/opt/inasafe-fba/fixtures
POSTGRES_DB=gis
POSTGRES_USER=docker
POSTGRES_PASS=docker
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Remember for `POSTGRES_HOST` and `POSTGRES_PORT` the value is like that because 
we are connecting from inside the containers, not from our local machine.
Add more variables if you need it in your unittests.
You can Copy above lines and pasted it into PyCharm Environment Variables field.
PyCharm will reformat it for you.

When you finish, click Apply and Save.

3. Run the configurations

To run the configurations just select your profile from the toolbars and click Run icon.
If you want to debug it, click Debug Icon.
The Run window will show up and provides you with the list of unittest it found and run.
After it finished, you can check each individual test.
You can even click the stack trace to navigate you to the source code where the tests failed.
