/*
실습04 - 조인과 하위 쿼리
*/

-- 데이터베이스 연결
USE myshop2019;


-- Q01) 전체금액이 8,500,000 이상인 주문의 주문번호, 고객아이디, 사원번호, 주문일시, 전체금액을 조회하세요.

SELECT order_id, customer_id, employee_id, order_date, total_due
	FROM order_header
    WHERE total_due >= 8500000;


-- Q02) 위에서 작성한 쿼리문을 복사해 붙여 넣은 후 고객이름도 같이 조회되게 수정하세요.

SELECT o.order_id, o.customer_id, c.customer_name, o.employee_id, o.order_date, o.total_due
	FROM order_header AS o
    INNER JOIN customer AS c ON o.customer_id = c.customer_id
    WHERE o.total_due >= 8500000;


-- Q03) Q01 쿼리를 복사해 붙여 넣은 후 직원이름도 같이 조회되게 수정하세요.

SELECT o.order_id, o.customer_id, o.employee_id, e.employee_name, o.order_date, o.total_due
	FROM order_header AS o
    INNER JOIN employee AS e ON o.employee_id = e.employee_id
    WHERE o.total_due >= 8500000;


-- Q04) 위에서 작성한 쿼리문을 복사해 붙여 넣은 후 고객이름, 직원이름도 같이 조회되게 수정하세요.
 
SELECT o.order_id, o.customer_id, c.customer_name, c.gender, c.city, e.employee_name, o.order_date, o.total_due
	FROM order_header AS o
    INNER JOIN customer AS c ON o.customer_id = c.customer_id    
    INNER JOIN employee AS e ON o.employee_id = e.employee_id
    WHERE o.total_due >= 8500000;


-- Q05) 위에서 작성한 쿼리문을 복사해 붙여 넣은 후 전체금액이 8,500,000 이상인 '서울' 지역 고객만 조회되게 수정하세요.

SELECT o.order_id, o.customer_id, c.customer_name, c.gender, c.city, e.employee_name, o.order_date, o.total_due
	FROM order_header AS o
    INNER JOIN customer AS c ON o.customer_id = c.customer_id    
    INNER JOIN employee AS e ON o.employee_id = e.employee_id
    WHERE o.total_due >= 8500000 AND city = '서울';


-- Q06) 위에서 작성한 쿼리문을 복사해 붙여 넣은 후 전체금액이 8,500,000 이상인 '서울' 지역 '남자' 고객만 조회되게 수정하세요.

SELECT o.order_id, o.customer_id, c.customer_name, c.gender, c.city, e.employee_name, o.order_date, o.total_due
	FROM order_header AS o
    INNER JOIN customer AS c ON o.customer_id = c.customer_id    
    INNER JOIN employee AS e ON o.employee_id = e.employee_id
    WHERE o.total_due >= 8500000 AND c.city = '서울' AND c.gender = 'M';


-- Q07) 주문수량이 30개 이상인 주문의 주문번호, 상품코드, 주문수량, 단가, 지불금액을 조회하세요.
    
SELECT order_id, product_id, order_qty, unit_price, line_total
	FROM order_detail
    WHERE order_qty >= 30;
    

-- Q08) 위에서 작성한 쿼리문을 복사해서 붙여 넣은 후 상품이름도 같이 조회되도록 수정하세요.

SELECT o.order_id, p.product_name, o.product_id, o.order_qty, o.unit_price, o.line_total
	FROM order_detail AS o
    INNER JOIN product AS p ON o.product_id = p.product_id
    WHERE o.order_qty >= 30;


-- Q09) 상품코드, 상품이름, 소분류아이디를 조회하세요.

SELECT product_id, product_name, sub_category_id 
    FROM product;


-- Q10) 위에서 작성한 쿼리문을 복사해서 붙여 넣은 후 소분류이름, 대분류아이디가 조회되게 수정하세요.
    
SELECT pr.product_id, pr.product_name, pr.sub_category_id, sc.sub_category_name, sc.category_id
    FROM product AS pr
    INNER JOIN sub_category AS sc ON pr.sub_category_id = sc.sub_category_id;


-- Q11) 위에서 작성한 쿼리문을 복사해서 붙여 넣은 후 대분류이름이 조회되게 수정하세요.

SELECT pr.product_id, pr.product_name, pr.sub_category_id, sc.sub_category_name, sc.category_id, ct.category_name
    FROM product AS pr
    INNER JOIN sub_category AS sc ON pr.sub_category_id = sc.sub_category_id
    INNER JOIN category AS ct ON sc.category_id = ct.category_id;
    

-- Q12) 위에서 작성한 쿼리문을 복사해서 붙여 넣은 후 대분류이름, 소분류이름, 상품이름, 상품코드가 조회되게 수정하세요.
    
SELECT ct.category_name, sc.sub_category_name, pr.product_name, pr.product_id
    FROM product AS pr
    INNER JOIN sub_category AS sc ON pr.sub_category_id = sc.sub_category_id
    INNER JOIN category AS ct ON sc.category_id = ct.category_id;
    
    
-- Q13) 'mtkim', 'odoh', 'soyoukim', 'winterkim' 고객 주문의 주문번호, 고객아이디, 주문일시, 전체금액을 조회하세요.

SELECT order_id, customer_id, order_date, total_due
	FROM order_header
    WHERE customer_id IN ('mtkim', 'odoh', 'soyoukim', 'winterkim');

    
-- Q14) '전주' 지역 고객의 아이디를 조회하세요.    

SELECT customer_id
	FROM customer
    WHERE city = '전주';


-- Q15) 위 두 쿼리문을 조합해서 하위 쿼리를 사용해 '전주' 지역 고객 주문의 주문번호, 고객아이디, 주문일시, 전체금액을 조회하세요.
  
SELECT order_id, customer_id, order_date, total_due
	FROM order_header
    WHERE customer_id IN (SELECT customer_id
							FROM customer
							WHERE city = '전주'
	);    


-- Q16) 고객의 포인트 최댓값을 조회하세요.

SELECT MAX(point) AS max_point FROM customer;


-- Q17) 하위 쿼리를 사용해 가장 포인트가 많은 고객의 이름, 아이디, 등록일, 포인트를 조회하세요.

SELECT customer_name, customer_id, register_date, point
	FROM customer
    WHERE point = (SELECT MAX(point) FROM customer);


-- Q18) 하위 쿼리를 사용해 홍길동(gdhong) 고객보다 포인트가 많은 고객 이름, 아이디, 등록일, 포인트를 조회하세요.

SELECT customer_name, customer_id, register_date, point
	FROM customer
    WHERE point > (SELECT point 
					   FROM customer 
                       WHERE customer_id = 'gdhong'
	);    
    

-- Q19) 하위 쿼리를 사용해 홍길동(gdhong) 고객과 같은 지역의 고객 이름, 아이디, 지역, 등록일, 포인트를 조회하세요.
--      단, 고객 이름을 기준으로 오름차순 정렬해서 조회하세요.

SELECT customer_name, customer_id, city, register_date, point
	FROM customer
    WHERE city = (SELECT city 
					   FROM customer 
                       WHERE customer_id = 'gdhong'
	)
    ORDER BY customer_name ASC;    
    