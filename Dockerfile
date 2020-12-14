FROM python:3.7
WORKDIR /app
COPY ./.env /app/
COPY ./Pipfile* /app/
RUN mkdir output
RUN wget https://packages.microsoft.com/debian/9/prod/pool/main/m/msodbcsql17/msodbcsql17_17.6.1.1-1_amd64.deb 
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y unixodbc unixodbc-dev
RUN pip install pipenv
RUN pipenv install
RUN yes | dpkg -i msodbcsql17_17.6.1.1-1_amd64.deb
COPY ./*.py /app/
CMD ["pipenv", "run", "python", "main.py"]