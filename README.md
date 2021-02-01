# repo_name
ETL pipeline that pulls student demographic and services data from SEIS (SPED platform) into the data warehouse.

## Dependencies:

- Python3.8
- [Pipenv](https://pipenv.readthedocs.io/en/latest/)
- [Docker](https://www.docker.com/)

## Getting Started

### Setup Environment

1. Clone this repo

```
git clone https://github.com/kippnorcal/seis_connector.git
```

2. Create .env file with project secrets

The environment file should fit the following template:

```
# Database variables
DB_SERVER=
DB=
DB_USER=
DB_PWD=
DB_SCHEMA=

# FTP variables
FTP_HOST=
FTP_USER=
FTP_PWD=

# Email Credentials (Optional)
ENABLE_MAILER=1
SENDER_EMAIL=
SENDER_PWD=
RECIPIENT_EMAIL=

# Enable Debug Logging (Optional)
DEBUG=1
```

## Build the Docker image

```
$ docker build -t seis .
```

## Run the job
```
$ docker run --rm -it seis
```

## Run the job with volume mapping
```
$ docker run --rm -it -v ${PWD}:/code/ seis
```
