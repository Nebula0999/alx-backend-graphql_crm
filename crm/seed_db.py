import requests

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:5000/graphql"

# Sample data to seed
users = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"},
]

def create_user(user):
    query = """
    mutation CreateUser($name: String!, $email: String!) {
      createUser(name: $name, email: $email) {
        id
        name
        email
      }
    }
    """
    variables = {
        "name": user["name"],
        "email": user["email"]
    }
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables}
    )
    return response.json()

if __name__ == "__main__":
    for user in users:
        result = create_user(user)
        print(result)