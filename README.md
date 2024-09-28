# seis_connector
ETL pipeline that downloads student demographic and services files from an FTP server connected to SEIS ([Special Education Information System](https://www.sjcoe.org/CodeStack/SEIS.aspx)). Files are loaded into Google Cloud Storage.

## Pre-requisites:
This connector iteratively pulls files from an SFTP server. In order to use this code, you will need to have an SFTP server that is already set up and contains the SEIS files.

In the SFTP directory, each school has its own sub-directory, and files are dropped into each school's folder nightly. This automated data file export is set up in partnership with the [San Joaquin County Office of Education (SJCOE) SEIS team](https://www.sjcoe.org/CodeStack/SEIS.aspx).

Note: SEIS drops three different file formats with the same data (.csv, .txt, .xml), and this script is only processing the .csv files.

## Dependencies:

- Python3
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
# Google Cloud Credentials
GOOGLE_APPLICATION_CREDENTIALS=
GBQ_PROJECT=
BUCKET=

# FTP variables
FTP_HOST=
FTP_USER=
FTP_PWD=

# Email Credentials
FROM_ADDRESS=
TO_ADDRESS=
MG_API_KEY=
MG_API_URL=
MG_DOMAIN=
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
