# Connects to database, drops and builds table, displays tables.
source .env
export PGPASSWORD=$DB_PASSWORD
# psql --host $DB_IP -U $DB_USERNAME -p $DB_PORT -d $DB_NAME -f schema.sql
psql --host $DB_IP -U $DB_USERNAME -p $DB_PORT -d $DB_NAME -f queries.sql

