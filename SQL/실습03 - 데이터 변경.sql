/*
실습03 - 데이터 변경
*/

-- 데이터베이스 연결
USE MyShop2019;


-- Q01) 다음 쿼리문을 하나씩 실행해 vendor 테이블을 만들고 이후 쿼리문을 작성하세요.

-- 기존 테이블 제거
DROP TABLE IF EXISTS vendor;

-- 테이블 만들기
CREATE TABLE vendor (
	vendor_id char(03) NOT NULL,
    vendor_name varchar(20) NOT NULL,
    manager_name varchar(10) NOT NULL,
    phone varchar(20) NOT NULL,
    register_date datetime NOT NULL,
    PRIMARY KEY(vendor_id)
);

-- 데이터 추가
INSERT INTO vendor VALUES('V01', '우주전자', '김우주', '010-1234-5678', '1900-01-01');

-- 확인
SELECT * FROM vendor;


-- Q02) 위 쿼리문 중 데이터 추가 부분을 참고하여 'V02' ~ 'V05' 코드를 갖는 납품업체 4 곳을 임의 데이터로 등록하세요.

INSERT INTO vendor VALUES('V02', '좋은전산', '박전산', '010-1234-5678', '1900-01-01');
INSERT INTO vendor VALUES('V03', '가전천국', '오가전', '010-1235-4779', '1900-01-01');
INSERT INTO vendor VALUES('V04', '최고산업', '나최고', '010-1236-3870', '1900-01-01');
INSERT INTO vendor VALUES('V05', '문구대왕', '박문구', '010-1237-2971', '1900-01-01');


-- Q03) 납품업체의 이름, 아이디, 담당자이름, 전화번호를 이름순으로 오름차순 정렬해 조회하세요.

SELECT vendor_name, vendor_id, manager_name AS manager, phone
	FROM vendor 
    ORDER BY vendor_name ASC;
    
--
-- Q04) 'V01' 업체 담당자 이름을 '유명해'로 변경하세요.

UPDATE vendor
	SET manager_name = '유명해'
    WHERE vendor_id = 'V01';


-- Q05) 'V01' 업체 등록일을 '1997-01-01'로 변경하세요.   

UPDATE vendor
	SET register_date = '1997-01-01'
    WHERE vendor_id = 'V01';
  
  
-- Q06) 'V05' 납품업체 정보를 삭제하세요.
  
DELETE FROM vendor
	WHERE vendor_id = 'V05';


-- Q07) 납품업체 이름, 아이디, 담당자이름, 전화번호, 등록일을 이름순으로 오름차순 정렬해 조회하세요.

SELECT vendor_name, vendor_id, manager_name AS manager, phone, register_date
	FROM vendor 
    ORDER BY vendor_name ASC;


-- Q08) 다음 쿼리문을 실행해서 customer 테이블의 모든 데이터를 customer_new라는 새로운 테이블로 저장하세요.

DROP TABLE IF EXISTS customer_new;

CREATE TABLE customer_new
	SELECT *
		FROM customer;


-- Q09) customer_new 테이블을 대상으로 다음과 같이 조건에 따른 고객 등급이 표시되게 조회하세요.
--      단, 포인트가 0이거나 NULL이면 고객 등급이 NULL이 되게 하세요.
/*
1,000,000 이상 --> 'Platinum'
  600,000 이상 --> 'Gold'
  300,000 이상 --> 'Silver'
  100,000 이상 --> 'Bronze'
        0 초과 --> 'Family'
*/

SELECT customer_name, customer_id, gender, city, register_date, point,
       CASE WHEN point >= 1000000 THEN 'Platinum'
            WHEN point >= 600000  THEN 'Gold'
            WHEN point >= 300000  THEN 'Silver'
            WHEN point >= 100000  THEN 'Bronze'
            WHEN point > 0        THEN 'Family'
            ELSE NULL END AS level
    FROM customer_new;
    
    
-- Q10) 다음 구문을 실행해서 customer_new 테이블에 level 열을 추가하세요.

ALTER TABLE customer_new
    ADD level varchar(20) NULL;
    
    
-- Q11) customer_new 테이블의 level 열을 Q09에서 조회한 level 정보로 변경하세요.
--      참고: Safe mode 적용방법(Edit -> Preferences -> SQL Editor에서 Safe Updates 체크)

UPDATE customer_new
       SET level= CASE WHEN point >= 1000000 THEN 'Platinum'
                       WHEN point >= 600000  THEN 'Gold'
                       WHEN point >= 300000  THEN 'Silver'
                       WHEN point >= 100000  THEN 'Bronze'
                       WHEN point > 0        THEN 'Family'
                       ELSE NULL END;
                       

-- Q12) customer_new 테이블에서 고객의 이름, 아이디, 성별, 지역, 가입일, 포인트, 등급을 조회하세요.

SELECT customer_name, customer_id, gender, city, register_date, point, level
    FROM customer_new;