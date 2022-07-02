DROP SCHEMA IF EXISTS store CASCADE;
CREATE SCHEMA store;
DROP TABLE IF EXISTS store.customers;
CREATE TABLE store.customers (
    userid      INT            not null,
    username    VARCHAR(20)    not null,
    name        VARCHAR(20)    not null,
    sex         VARCHAR(2)     not null,
    address     VARCHAR(50)    not null,
    mail        VARCHAR(30)    not null,
    birthdate   DATE           not null,
    
    PRIMARY KEY (userid)
);
DROP TABLE IF EXISTS store.orders;
CREATE TABLE store.orders(
    transactionid    INT         not null,
    custid           INT         not null,
    trandate         DATE        not null,
    store_nm         VARCHAR(15) not null,
    goods_id         INT         not null,
    gds_grp_nm       VARCHAR(30) not null,
    gds_grp_mclas_nm VARCHAR(30) not null,
    amount           INT         not null,
    
    PRIMARY KEY (transactionid),
    FOREIGN KEY (custid) REFERENCES store.customers(userid)
        ON DELETE CASCADE
);