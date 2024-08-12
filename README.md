# Installation

The installation guide assumes an existing Python installation.
If you need to install Python, please visit the [Python website](https://www.python.org/).

The tool used to manage the Python project is `poetry`.
Find more information on the [Poetry website](https://python-poetry.org/).
It is recommended to install `poetry` via `pipx` (which isolates dedicated python tools like `poetry`) 
`pipx` can in turn be installed via `pip`:

```bash
pip install pipx
pipx install poetry
```

After installing `poetry`, navigate to the root of the repository and run:

```bash
poetry install
```

This will install all dependencies required for the project in a dedicated virtual environment.

## Note:
This project was built on a Linux machine and has not been tested on Windows or MacOS.


# Usage

Execute the following command to get a list of available commands:

```bash
python -m genesis --help
```

## Testing the API

To test the API, run the command without any arguments, which will call the `helloworld/whoami` endpoint:

```bash
python -m genesis
```

To test your login data, run the command just with your username and password:

```bash
python -m genesis MYUSERNAME MYPASSWORD
```

## Downloading a table:

To call the `data/table` endpoint, which allows you to download a table from the GENESIS database, run the command 
with your username and password and specify the table name and other parameters as key-value pairs, e.g.:

```bash
python -m genesis MYUSERNAME MYPASSWORD table name=12411-0001 area=all values=true additionals=false
```

The command above will download the table `12411-0001` for all areas.

Note that per default, the language is set to `de`, but you can override this by specifying the `language` parameter
like this: `language=en`.

There are a lot of other parameters you can specify, which are all documented in the GENESIS API documentation:
https://www-genesis.destatis.de/genesis/misc/GENESIS-Webservices_Einfuehrung.pdf (section 2.5.11)

Here's a list of all parameters you can specify:
 * name
 * area
 * values
 * compress
 * transpose
 * additionals
 * content
 * startyear
 * endyear
 * timeslices
 * regionalvariable
 * regionalkey
 * classifyingvariable1
 * classifyingkey1
 * classifyingvariable2
 * classifyingkey2
 * classifyingvariable3
 * classifyingkey3
 * classifyingvariable4
 * classifyingkey4
 * classifyingvariable5
 * classifyingkey5
 * format
 * stand
 * language


# How does it work?

The `genesis` module is a Python package that provides a command-line interface to interact with the GENESIS API.
It uses the `requests` library to send HTTP requests to the GENESIS API.
Find out more about the `requests` library [here](https://docs.python-requests.org/en/master/).

The `pandas` library is often used in data science (e.g., data cleaning, data transformation, and data analysis).
Here it is used to handle the data we got from the API.
Find out more about the `pandas` library [here](https://pandas.pydata.org/).

The user interacts with the package via the command-line interface, which is implemented using the `typer` library.
Find out more about the `typer` library [here](https://typer.tiangolo.com/).

The plot at the very end of the script is created using the `matplotlib` library, which is a plotting library
for Python often used in scientific computing.
Find out more about the `matplotlib` library [here](https://matplotlib.org/).

Logging is not done via the typical `logging` module, but via the `structlog` library,
which is a structured logging library. It is used for convenience, but the normal logging module could be used as well.
Find out more about the `structlog` library [here](https://www.structlog.org/en/stable/).
