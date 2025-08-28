#!/usr/bin/env python3
import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup logging
logging.basicConfig(
    filename="/tmp/order_reminders_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def main():
    # GraphQL endpoint
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Calculate last 7 days
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)

    # GraphQL query
    query = gql(
        """
        query GetRecentOrders($lastWeek: Date!, $today: Date!) {
          orders(filter: {orderDate_Gte: $lastWeek, orderDate_Lte: $today, status: "PENDING"}) {
            id
            customer {
              email
            }
          }
        }
        """
    )

    # Execute query
    params = {"lastWeek": str(last_week), "today": str(today)}
    result = client.execute(query, variable_values=params)

    # Log results
    for order in result.get("orders", []):
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")

    print("Order reminders processed!")

if __name__ == "__main__":
    main()
