# Chat on Channels

This project is a chat application built with Django and Channels, allowing real-time communication. This project is configured to run with Docker.

## Running with Docker

This is the only supported way to run the project, as it automatically sets up all required services (Django, PostgreSQL, Redis).

### 1. Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

### 2. Configuration

All necessary configuration is already hardcoded into the project for ease of use. You do not need to configure anything.

The database credentials and other settings are set directly in `docker-compose.yml` and `project/settings.py`.

### 3. Running

1.  **Build and run the containers in the background:**

    ```bash
    docker compose up -d --build
    ```

2.  **Run database migrations to create the necessary tables:**

    ```bash
    docker compose exec web python manage.py migrate
    ```

3.  **The project will be available at [http://localhost:8000](http://localhost:8000).**

    To connect to the PostgreSQL database from your local machine (e.g., using DBeaver or DataGrip), use the following credentials:
    *   **Host:** `localhost`
    *   **Port:** `5433`
    *   **Database:** `chat`
    *   **Username:** `postgres`
    *   **Password:** `postgres`


## Test Data

To populate the database with test users and a chat room, run the following management command:

```bash
docker compose exec web python manage.py create_test_data
```

This command is safe to run multiple times. It will create the following users if they don't already exist:

| Role      | Login (email)       | Password |
|-----------|---------------------|----------|
| Admin     | `admin@example.com` | `admin`    |
| User 1    | `user1@example.com` | `user1`    |
| User 2    | `user2@example.com` | `user2`    |

It also creates a room named **"Test Room"** and adds all the above users to it.

