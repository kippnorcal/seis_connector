# seis_connector
ETL pipeline that pulls student demographic and services data from SEIS ([Special Education Information System](https://www.sjcoe.org/CodeStack/SEIS.aspx)) into the data warehouse. This code does a full truncate and reload of the database tables and does not track changes over time.

## Pre-requisites:
This connector iteratively pulls files from an SFTP server. In order to use this code, you will need to have an SFTP server that is already set up and contains the SEIS files.

In the SFTP directory, each school has its own sub-directory, and files are dropped into each school's folder nightly. This automated data file export is set up in partnership with the [San Joaquin County Office of Education (SJCOE) SEIS team](https://www.sjcoe.org/CodeStack/SEIS.aspx).

Note: SEIS drops three different file formats with the same data (.csv, .txt, .xml), and this script is only processing the .csv files.

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
