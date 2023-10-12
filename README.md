# DDaT Capability Assessment

## Prerequisites

### Required

- Docker

## Getting started

### Set local environment variables

In the `Dockerfile` file you will find a number of environment variables. These are injected as global variables into the app and pre-populated into page templates as appropriate. Enter your specific information for the following:

- CONTACT_EMAIL
- CONTACT_PHONE
- DEPARTMENT_NAME
- DEPARTMENT_URL
- SERVICE_NAME
- SERVICE_PHASE
- SERVICE_URL

### Get the latest GOV.UK Frontend assets

```shell
./build.sh
```

### Run containers

```shell
docker compose up
```

You should now have the app running on <https://localhost:8000/>.

## Testing

To run the tests:

```shell
docker compose exec web python -m pytest --cov=app --cov-report=term-missing --cov-branch
```

## Development environment

```mermaid
C4Container
    title C4 Container diagram for DDaT Capability Assessment

    Person(user, User, "A person in a DDaT Capability Framework defined role", $tags="v1.0")

    Container_Boundary(c1, "DDaT Capability Assessment") {
        Container(web_app, "Web Application", "Python, Flask", "Provides all the functionality to users via their web browser")
        ContainerDb(database, "Database", "PostgreSQL, Docker Container", "Stores data relating to roles, skills, levels and assessments")
        ContainerDb(cache, "Cache", "Redis, Docker Container", "Stores temporary cached data to improve performance")
    }

    Rel(user, web_app, "Uses", "HTTPS")
    Rel(web_app, database, "Reads from and writes to", "sync, SQL")
    Rel(web_app, cache, "Reads from and writes to", "sync")
```

## Data model

```mermaid
erDiagram
    ROLE }|--|| ROLE_SKILL : "has"
    ROLE_SKILL ||--|{ SKILL : "has"

    ROLE {
        uuid id PK
        string title
        timestamp created_at
        timestamp updated_at
    }
    SKILL {
        uuid id PK
        string description
        string level
        timestamp created_at
        timestamp updated_at
    }
    ROLE_SKILL {
        uuid role_id FK
        uuid skill_id FK
    }
```

## Contributors

- [Matt Shaw](https://github.com/matthew-shaw) (Primary maintainer)

## Support

This software is provided _"as-is"_ without warranty. Support is provided on a _"best endeavours"_ basis by the maintainers and open source community.

Please see the [contribution guidelines](CONTRIBUTING.md) for how to raise a bug report or feature request.
