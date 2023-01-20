/*
00 - 데이터베이스와 테이블
*/

-- 1) 데이터베이스 만들기

-- 기존 데이터베이스 제거
DROP DATABASE IF EXISTS mydb;

-- 데이터베이스 만들기
CREATE DATABASE mydb;


-- 2) 테이블 만들기

-- 대상 데이터베이스로 연결
USE mydb;

-- 기존 테이블 제거
DROP TABLE IF EXISTS vacation;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS department;

-- department 테이블 만들기
CREATE TABLE department (
	dept_id CHAR(3) NOT NULL,
	dept_name VARCHAR(10) NOT NULL,
	start_date DATE NOT NULL,
    PRIMARY KEY(dept_id)
);

-- employee 테이블 만들기
CREATE TABLE employee (
	emp_id CHAR(5) NOT NULL,
	emp_name VARCHAR(4) NOT NULL,
	gender CHAR(1) NOT NULL,
	hire_date DATE NOT NULL,
	dept_id CHAR(3) NOT NULL,
	phone CHAR(13) NOT NULL,
	salary INT NULL,
    PRIMARY KEY(emp_id),
    FOREIGN KEY(dept_id) REFERENCES department(dept_id),
    UNIQUE(phone)
);

-- vacation 테이블 만들기
CREATE TABLE vacation (
	vacation_id INT NOT NULL AUTO_INCREMENT,
	emp_id CHAR(5) NOT NULL,
	begin_date DATE NOT NULL,
	end_date DATE NOT NULL,
	reason VARCHAR(50) NOT NULL DEFAULT '개인사유',
	duration INT AS (DATEDIFF(end_date, begin_date) + 1),
	CHECK (end_date >= begin_date),
    FOREIGN KEY(emp_id) REFERENCES employee(emp_id),
    PRIMARY KEY(vacation_id)
);


/*
[MySQL 데이터 형식]

1. 정수형

1) TINYINT: 
- 크기: 1 바이트
- 범위: -128 ~ 127 / UNSIGNED: 0 ~ 255

2) SMALLINT
- 크기: 2 바이트
- 범위: -32,768 ~ 32,767 / UNSIGNED: 0 ~ 65,535

3) MEDIUMINT
- 크기: 3 바이트
- 범위: -8,388,608 ~ 8,388,607 / UNSIGNED: 0 ~ 16,777,215

4) INT, INTEGER
- 크기: 4 바이트
- 범위: -2,147,483,648 ~ 2,147,483,647 / UNSIGNED: 0 ~ 4,294,967,295

5) BIGINT
- 크기: 8 바이트
- 범위: -9,223,372,036,854,775,808 ~ 9,223,372,036,854,775,807 / UNSIGNED: 0 ~ 18,446,744,073,709,551,615


2. 실수형

1) FLOAT
- 크기: 4 바이트
- 범위: -3.402823466E+38 ~ 3.402823466E+38
- 소수점 아래 7자리까지 표현

2) DOUBLE, REAL
- 크기: 8 바이트
- 범위: -1.7976931348623157E+308 ~ 1.7976931348623157E+308
- 소수점 아래 15자리까지 표현

3) DECIMAL(m, [d]), NUMERIC(m, [d])
- 크기: 5 ~ 17 바이트
- 범위: -10^38+1 ~ +10^38-1


3. 문자형 

1) CHAR(n)
- 크기: 1 ~ 255 바이트
- 고정길이 문자형, n: 1 ~ 255.

2) VARCHAR(n)
- 크기: 1 ~ 65,535 바이트
- 가변길이 문자형, n: 1 ~ 65,535

3) TINYINT
- 크기: 1 ~ 255 바이트

4) TEST
- 크기: 1 ~ 65,535 바이트

5) MEDIUMTEXT
- 크기: 1 ~ 16,777,215 바이트

6) LONGTEXT
- 크기: 1 ~ 4,294,967,295 바이트


4. 날짜 시간형

1) DATE
- 크기: 3 바이트
- 범위: 1001-01-01 ~ 9999-12-31까지 저장되며 날짜 형식만 사용

2) TIME
- 크기: 3 바이트
- 범위: -838:59:59.000000 ~ 838:59:59.000000

3) DATETIME
- 크기: 8 바이트
- 범위: 1001-01-01 00:00:00 ~ 9999-12-31 23:59:59

4) TIMESTAMP
- 크기: 4 바이트
- 범위: 1970-01-01 00:00:01 ~ 2038-01-19 03:14:07

5) YEAR
- 크기: 1 바이트
- 범위: 1901 ~ 2155
*/


-- 3) 데이터 추가

-- department 테이블
INSERT INTO department VALUES('SYS', '정보시스템', '2013-01-01');
INSERT INTO department VALUES('MKT', '영업', '2013-05-01');
INSERT INTO department VALUES('GEN', '총무', '2014-03-01');

-- employee 테이블
INSERT INTO employee VALUES('S0001', '홍길동', 'M', '2013-01-01', 'SYS', '010-1234-1234', 8500);
INSERT INTO employee VALUES('S0002', '일지매', 'M', '2013-01-12', 'GEN', '017-111-1222',  8200);
INSERT INTO employee VALUES('S0003', '강우동', 'M', '2014-04-01', 'SYS', '010-1222-2221', 6500);
INSERT INTO employee VALUES('S0004', '김삼순', 'F', '2014-08-01', 'MKT', '010-3212-3212', 7000);
INSERT INTO employee VALUES('S0005', '오삼식', 'M', '2015-01-01', 'MKT', '010-9876-5432', 6400);

-- vacation 테이블
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-01-12', '2013-01-12', '감기몸살');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-03-21', '2013-03-21', '글쎄요');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-06-13', '2013-06-14', '글쎄요');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-07-07', '2013-07-07', '중요 행사 준비');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0002', '2013-07-21', '2013-07-25', '놀고싶어서');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-08-01', '2013-08-01', '치통이 심해서');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-08-03', '2013-08-08', '놀고싶어서');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0002', '2013-11-17', '2013-11-17', '두통');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0001', '2013-12-01', '2013-12-15', '비밀');
INSERT INTO vacation(emp_id, begin_date, end_date, reason) VALUES('S0002', '2014-02-10', '2014-02-13', '두통');


-- 4) 테이블, 열 변경

SELECT * 
    FROM employee;

-- 테이블 정보 확인    
DESCRIBE 직원;

-- 테이블 이름 변경
ALTER TABLE employee 
    RENAME TO 직원;

-- 데이터 형식 바꾸기
ALTER TABLE 직원 
    MODIFY phone varchar(20) NOT NULL;

DESCRIBE 직원;  
 
-- 열 이름 바꾸기
ALTER TABLE 직원 
    RENAME COLUMN phone TO tel;

DESCRIBE 직원;  

-- 열 추가 
ALTER TABLE 직원 
    ADD retire_date date NULL;

DESCRIBE 직원;  

-- 열 삭제
ALTER TABLE 직원 
    DROP retire_date;

DESCRIBE 직원;



/*
실습: 테이블 다루기
*/


-- Q1) mydb에 친구 정보를 저장할 테이블 friend 테이블을 만드세요. 
--     단, 열은 5개 이상 만들어야 합니다.

USE mydb;

CREATE TABLE friend (
	friend_id int NOT NULL,
    friend_name varchar(20) NOT NULL,
    friend_type varchar(20) NOT NULL,
    birthdate date NULL,
    etc varchar(500) NOT NULL,
    PRIMARY KEY (friend_id)
);


-- Q2) mydb에 다음 쿼리를 수행하여 orders 테이블을 만드세요.

CREATE TABLE orders (
	order_id int NOT NULL,
    product_id char(5) NOT NULL,
    customer_id varchar(20) NOT NULL,
    qty int NOT NULL,
    unit_price int NOT NULL,
    PRIMARY KEY (order_id)
);


-- Q3) Orders 테이블 구조를 확인하세요.

DESCRIBE orders;


-- Q4) order_date 열을 datetime 형으로 추가하세요. 
--     단 NULL 값을 허용하지 않아야 합니다.

ALTER TABLE orders 
    ADD order_date datetime NOT NULL;
 
-- 확인
 DESCRIBE orders;


-- Q5) qty 열 이름을 quantity로 변경하세요.

ALTER TABLE orders 
    RENAME COLUMN qty TO quantity;
    
-- 확인
DESCRIBE orders;
 
 
-- Q6) amount 열을 int 형으로 추가하세요. 단 NULL 값을 허용하지 않아야 합니다. 
 
ALTER TABLE orders 
    ADD COLUMN amount int NOT NULL;
 
-- 확인
DESCRIBE orders;
 
 
-- Q7) orders 테이블 이름을 order_header로 변경하세요.
 
ALTER TABLE orders 
    RENAME order_header;
 
-- 테이을 목록 확인 
SHOW TABLES;
