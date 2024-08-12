import io
import logging

import matplotlib.pyplot as plt
import pandas as pd
import requests
import structlog
import typer

app = typer.Typer()

logger = structlog.get_logger()

logging.basicConfig(level=logging.INFO)

BASE_URL = "https://www-genesis.destatis.de/genesisWS/rest/2020"


def get_request(endpoint: str, params: dict = None):
    url = f"{BASE_URL}/{endpoint}"
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()]) if params else ""
    response = requests.get(f"{url}?{query_string}")
    response.raise_for_status()
    return response


@app.command()
def genesis(
        username: str = typer.Argument(None),
        password: str = typer.Argument(None),
        options: list[str] = typer.Argument(None),
):
    # If no arguments are given, test the API with the helloworld/whoami endpoint:
    if not username and not password:
        response = get_request("helloworld/whoami")
        logger.info("WhoAmI result:", **response.json())
        return

    # If no options are given, simply test the helloworld/login with the provided username and password:
    if not options:
        response = get_request(
            "helloworld/logincheck",
            {"username": username, "password": password, "language": "de"}
        )
        logger.info("Login test result:", **response.json())
        return

    # Initialize an empty dictionary for parsed options
    options_dict = {}
    # Parse the provided options into key-value pairs and store in the dictionary
    for option in options:
        try:
            key, value = option.split("=", 1)
            options_dict[key] = value
        except ValueError:
            typer.echo(f"Invalid option format: {option}. Expected format 'key=value'.")
            raise typer.Exit(code=1)

    # Make the request to the data/table endpoint with the provided options:
    logger.info(f"User: {username} calling data/table API endpoint with options:", **options_dict)
    params = {
        "username": username,
        "password": password,
        "language": "de",
        **options_dict
    }
    response = get_request("data/table", params)
    logger.debug("Data loaded successfully!")
    response_dict = response.json()
    logger.debug("Data response:", **response_dict)

    # Extract the content from the response and create a Pandas dataframe:
    content = response_dict["Object"]["Content"]
    csv_data = io.StringIO(content)
    dataframe = pd.read_csv(csv_data, sep=';')
    logger.debug("Dataframe created successfully", dataframe_info=dataframe.info, dataframe_head=dataframe.head())

    # Save the dataframe to an Excel file:
    dataframe.to_excel("data.xlsx")
    logger.info("Data saved to data.xlsx")

    # Extract the first column of the dataframe as numeric data and plot it:
    numeric_dataframe = pd.to_numeric(dataframe.iloc[:, 0], errors='coerce').dropna()
    logger.debug("Numeric data extracted", numeric_data=numeric_dataframe)
    numeric_dataframe.plot.line()
    plt.show()


if __name__ == "__main__":
    app()
