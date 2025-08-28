import datetime
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

def log_crm_heartbeat():
    """Logs CRM heartbeat every 5 minutes and checks GraphQL hello field."""

    # Current timestamp
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Default message
    message = f"{timestamp} CRM is alive"

    # Optional GraphQL check
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=2,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql(
            """
            query {
                hello
            }
            """
        )
        result = client.execute(query)
        hello_value = result.get("hello", "No response")
        message += f" | GraphQL hello: {hello_value}"
    except Exception as e:
        message += f" | GraphQL check failed: {e}"

    # Append to log file
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")
