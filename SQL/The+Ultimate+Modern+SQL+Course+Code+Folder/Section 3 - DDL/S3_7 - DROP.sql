USE ROLE SYSADMIN;
USE SCHEMA DEMO_DB.DEMO_SCHEMA;
USE WAREHOUSE XSMALL_WAREHOUSE;

-- DROP OBJECTS

DROP TABLE EMPLOYEE;

DROP TABLE IF EXISTS EMPLOYEE;

DROP DATABASE IF EXISTS DEMO_DB;

-- UNDROP OBJECTS

UNDROP DATABASE DEMO_DB;

USE SCHEMA DEMO_DB.DEMO_SCHEMA;

UNDROP TABLE EMPLOYEE;

SHOW TABLES;

-- DROP Unrequired Tables 

DROP TABLE EMPLOYEE_US;
DROP TABLE EMPLOYEE_DEV;
DROP TABLE EMPLOYEE_CLONE;


