# python-task-api

A task management API built with Python, exposing both a REST interface (Flask) and a GraphQL interface (Strawberry + Flask).

## Stack

- Python 3.11+
- Flask — REST endpoints
- Strawberry — GraphQL schema and resolvers

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the REST API

```bash
python app.py
# runs on http://localhost:5000
```

## REST Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks | List all tasks (optional ?status= filter) |
| GET | /tasks/<id> | Get a single task |
| POST | /tasks | Create a task |
| PATCH | /tasks/<id> | Update a task |
| DELETE | /tasks/<id> | Delete a task |

## Run the GraphQL API

```bash
python graphql_app.py
# runs on http://localhost:5001/graphql
```

## GraphQL Examples

```graphql
query {
  tasks {
    id
    title
    status
    priority
  }
}

mutation {
  createTask(title: "Review PR", priority: "high") {
    id
    title
    status
  }
}
```
