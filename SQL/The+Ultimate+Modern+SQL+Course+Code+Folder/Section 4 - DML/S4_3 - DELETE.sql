USE ROLE SYSADMIN;
USE WAREHOUSE XSMALL_WAREHOUSE;
USE SCHEMA DEMO_DB.DEMO_SCHEMA;

-- Delete all rows from a table

DELETE FROM EMPLOYEE;

SELECT * 
FROM EMPLOYEE;

-- Reinsert EMPLOYEE table rows
INSERT OVERWRITE INTO EMPLOYEE 
VALUES 
    (1, 'Prakash', 'Das', '1987-01-02', 'IN'),
    (2, 'Madiha', 'Bradford', '1975-10-02', 'GB'),
    (3, 'James', 'Lines', '1999-09-20', 'GB'),
    (4, 'Amar', 'Krishnan', '2002-01-02', 'IN'), 
    (5, 'Inaaya', 'Andrews', '2001-01-02', 'US'), 
    (6, 'Randy', 'Caldwell', '1970-01-02', 'FI');

SELECT LAST_QUERY_ID();

-- 01b56ad6-0000-f2c7-0001-b44200035166

-- Delete a single row from a table using WHERE
DELETE FROM EMPLOYEE
WHERE EMP_ID = 6;

SELECT * 
FROM EMPLOYEE;

-- Delete multiple rows from a table using WHERE

DELETE FROM EMPLOYEE
WHERE EMP_COUNTRY_CODE = 'GB';

SELECT * 
FROM EMPLOYEE;

-- USING

CREATE OR REPLACE TABLE GDPR_EMPLOYEE (
    EMP_ID NUMBER NOT NULL
);

INSERT INTO GDPR_EMPLOYEE 
VALUES
    (4),(5);

SELECT * 
FROM GDPR_EMPLOYEE;

DELETE FROM EMPLOYEE 
USING GDPR_EMPLOYEE
WHERE EMPLOYEE.EMP_ID = GDPR_EMPLOYEE.EMP_ID;

SELECT *
FROM EMPLOYEE;

-- Time Travel with AT & BEFORE

SELECT * 
FROM EMPLOYEE AT(STATEMENT => '01b56ad6-0000-f2c7-0001-b44200035166');

-- Clear-down table
DROP TABLE GDPR_EMPLOYEE;