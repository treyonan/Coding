USE ROLE ACCOUNTADMIN;
USE SCHEMA DEMO_DB.DEMO_SCHEMA;
USE WAREHOUSE XSMALL_WAREHOUSE;

-- Reset session parameter
ALTER SESSION SET DATE_INPUT_FORMAT = 'AUTO';
-- Reset account parameter
ALTER ACCOUNT SET DATE_INPUT_FORMAT = 'AUTO';

USE ROLE SYSADMIN;


-- Single Row INSERT

INSERT INTO EMPLOYEE VALUES (1, 'Prakash', 'Das', '1987-01-02', 'IN');

INSERT INTO EMPLOYEE VALUES (1, 'Das', '1987-01-02', 'IN'); -- SQL Compilation error

INSERT INTO EMPLOYEE (EMP_ID, EMP_FIRST_NAME, EMP_LAST_NAME, EMP_DOB, EMP_COUNTRY_CODE) VALUES (2, 'Madiha', 'Bradford', '1975-10-02', 'GB');

INSERT INTO EMPLOYEE (EMP_ID, EMP_FIRST_NAME) VALUES (3, 'James');

SELECT * FROM EMPLOYEE WHERE EMP_ID = 3;

-- Multiple Row INSERT

INSERT INTO EMPLOYEE 
VALUES 
    (4, 'Amar', 'Krishnan', '2002-01-02', 'IN'), 
    (5, 'Inaaya', 'Andrews', '2001-01-02', 'US'), 
    (6, 'Randy', 'Caldwell', '1970-01-02', 'FI');

SELECT * FROM EMPLOYEE;

INSERT OVERWRITE INTO EMPLOYEE 
SELECT 7, 'Saral', 'Raman', '1982-01-19', 'IN';

SELECT * FROM EMPLOYEE;

-- VALUES supports limited expressions

INSERT INTO EMPLOYEE VALUES (RANDOM(), 'Hirota', 'Shigeru', '1961-11-29', 'JP');

INSERT INTO EMPLOYEE
SELECT RANDOM(), 'Hirota', 'Shigeru', '1961-11-29', 'JP';

SELECT * FROM EMPLOYEE;