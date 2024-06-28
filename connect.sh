# Connects to database, drops and builds table, displays tables.
source .env
export PGPASSWORD=$DATABASE_PASSWORD
psql --host $DATABASE_IP -U $DATABASE_USERNAME -p $DATABASE_PORT -d $DATABASE_NAME -f schema.sql
