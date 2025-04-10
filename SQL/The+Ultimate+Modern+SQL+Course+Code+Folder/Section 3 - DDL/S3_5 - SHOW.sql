USE ROLE SYSADMIN;

-- Account Objects
SHOW USERS;

SHOW DATABASES;

USE ROLE USERADMIN;

SHOW DATABASES;

USE ROLE SYSADMIN;

SHOW DATABASES LIKE 'DEMO_DB';

-- Schema Objects

SHOW VIEWS IN DATABASE SNOWFLAKE_SAMPLE_DATA LIMIT 10;

USE SCHEMA DEMO_DB.DEMO_SCHEMA;

SHOW TABLES;

-- Parameters

SHOW PARAMETERS;

SHOW PARAMETERS IN DATABASE DEMO_DB;