FROM postgres:16.2-alpine
# ARG PSQL_HOST
# ARG PSQL_PORT
# ARG PSQL_USERNAME
# ARG PSQL_PASSWORD

COPY setup.sql /code/setup.sql

CMD psql -U $PSQL_USERNAME -h $PSQL_HOST -p $PSQL_PORT -f /code/setup.sql