import datetime
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    """Generate a weekly CRM report and log results."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
          customers {
            id
          }
          orders {
            id
            totalAmount
          }
        }
        """
    )

    try:
        result = client.execute(query)

        customers = result.get("customers", [])
        orders = result.get("orders", [])
        total_customers = len(customers)
        total_orders = len(orders)
        total_revenue = sum(o["totalAmount"] for o in orders if o.get("totalAmount"))

        report = (
            f"{timestamp} - Report: "
            f"{total_customers} customers, {total_orders} orders, {total_revenue} revenue"
        )

        with open(LOG_FILE, "a") as f:
            f.write(report + "\n")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{timestamp} - Report generation failed: {e}\n")
