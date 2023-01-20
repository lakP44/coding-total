/*
07 - SQLite 참고사항
*/

-- 1) 테이블 만들기

DROP TABLE IF EXISTS vacation;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS department;

CREATE TABLE department (
	dept_id TEXT NOT NULL,
	dept_name TEXT NOT NULL,
	start_date TEXT NOT NULL,
    PRIMARY KEY(dept_id)
);

-- employee 테이블 만들기
CREATE TABLE employee (
	emp_id TEXT NOT NULL,
	emp_name TEXT NOT NULL,
	gender TEXT NOT NULL,
	hire_date TEXT NOT NULL,
	dept_id TEXT NOT NULL,
	phone TEXT NOT NULL,
	salary INTEGER NULL,
    PRIMARY KEY(emp_id),
    FOREIGN KEY(dept_id) REFERENCES department(dept_id),
    UNIQUE(phone)
);

-- vacation 테이블 만들기
CREATE TABLE vacation (
    vacation_id INTEGER NOT NULL,
    emp_id TEXT NOT NULL,
    begin_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    reason TEXT NOT NULL DEFAULT '개인사유',
    duration AS (((julianday(end_date) - julianday(begin_date)) + 1)) VIRTUAL,
    PRIMARY KEY(vacation_id AUTOINCREMENT)
    FOREIGN KEY(emp_id) REFERENCES employee(emp_id),
    CHECK (end_date >= begin_date)
);

-- 2) 데이터 추가

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


-- 3) 테이블 정보 확인

SELECT * FROM pragma_table_info('직원') ORDER BY cid;
 
 
 -- 4) 테이블 변경
 
 -- 테이블 이름 변경
ALTER TABLE employee 
    RENAME TO 직원;
    
-- 데이터 형식 바꾸기
-- MODIFY 문이 제공되지 않음

-- 열 이름 바꾸기
ALTER TABLE 직원 
    RENAME COLUMN phone TO tel;

-- 열 추가 
ALTER TABLE 직원 
    ADD retire_date date NULL;

-- 열 삭제
ALTER TABLE 직원 
    DROP retire_date;
    
    
-- 5) 날짜와 시간 관련 함수 예

SELECT date('now') AS Today;
SELECT time('now', 'localtime') AS NowTime;
SELECT datetime('now', 'localtime') AS Now;


-- 6) CONCAT 함수 대신 ||를 사용해 연결

SELECT '10' || '20';
SELECT 10 || '20'; 
SELECT 10 || '20AX';
SELECT 10 || 'LX20';


-- 7) IF 함수 대신 IIF 함수 사용

SELECT emp_name, emp_id, 
       IIF(gender = 'M', '남자', '여자') AS gender, 
	   hire_date, retire_date, salary
	FROM employee;


-- 8) VACUUM 문을 실행하여 사용하지 않는 공간을 확보하고 파일 크기를 줄일 수 있음

DELETE FROM vacation;
VACUUM;


-- 9) TRUNCATE TABLE 문을 지원하지 않음
