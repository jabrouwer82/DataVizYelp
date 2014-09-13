-- Generated by Oracle SQL Developer Data Modeler 4.0.0.833
--   at:        2014-09-11 00:39:21 CDT
--   site:      Oracle Database 12c
--   type:      Oracle Database 12c




DROP TABLE Business_neighorhoor CASCADE CONSTRAINTS ;

DROP TABLE Attribute_business CASCADE CONSTRAINTS ;

DROP TABLE Review_vote CASCADE CONSTRAINTS ;

DROP TABLE Yelper_vote CASCADE CONSTRAINTS ;

DROP TABLE Elite_year_yelper CASCADE CONSTRAINTS ;

DROP TABLE Business_category CASCADE CONSTRAINTS ;

DROP TABLE Yelper_friend CASCADE CONSTRAINTS ;

DROP TABLE attribute CASCADE CONSTRAINTS ;

DROP TABLE business CASCADE CONSTRAINTS ;

DROP TABLE category CASCADE CONSTRAINTS ;

DROP TABLE checkin CASCADE CONSTRAINTS ;

DROP TABLE checkin_info CASCADE CONSTRAINTS ;

DROP TABLE complement CASCADE CONSTRAINTS ;

DROP TABLE elite_year CASCADE CONSTRAINTS ;

DROP TABLE hours CASCADE CONSTRAINTS ;

DROP TABLE neighborhood CASCADE CONSTRAINTS ;

DROP TABLE review CASCADE CONSTRAINTS ;

DROP TABLE tip CASCADE CONSTRAINTS ;

DROP TABLE yelper CASCADE CONSTRAINTS ;

DROP TABLE vote CASCADE CONSTRAINTS ;

CREATE TABLE Business_neighorhoor
  (
    business_id     NUMBER NOT NULL ,
    neighborhood_id NUMBER NOT NULL
  ) ;
ALTER TABLE Business_neighorhoor ADD CONSTRAINT Business_neighorhoor__IDX PRIMARY KEY ( business_id, neighborhood_id ) ;

CREATE TABLE Attribute_business
  (
    attribute_id NUMBER NOT NULL ,
    business_id  NUMBER NOT NULL
  ) ;
ALTER TABLE Attribute_business ADD CONSTRAINT Attribute_business__IDX PRIMARY KEY ( attribute_id, business_id ) ;

CREATE TABLE Review_vote
  (
    review_id NUMBER NOT NULL ,
    vote_id   NUMBER NOT NULL
  ) ;
ALTER TABLE Review_vote ADD CONSTRAINT Review_vote__IDX PRIMARY KEY ( review_id, vote_id ) ;

CREATE TABLE Yelper_vote
  (
    yelper_id NUMBER NOT NULL ,
    vote_id  NUMBER NOT NULL
  ) ;
ALTER TABLE Yelper_vote ADD CONSTRAINT Yelper_vote__IDX PRIMARY KEY ( yelper_id, vote_id ) ;

CREATE TABLE Elite_year_yelper
  (
    elite_year_id NUMBER NOT NULL ,
    yelper_id     NUMBER NOT NULL
  ) ;
ALTER TABLE Elite_year_yelper ADD CONSTRAINT Elite_year_yelper__IDX PRIMARY KEY ( elite_year_id, yelper_id ) ;

CREATE TABLE Business_category
  (
    business_id NUMBER NOT NULL ,
    category_id NUMBER NOT NULL
  ) ;
ALTER TABLE Business_category ADD CONSTRAINT Business_category__IDX PRIMARY KEY ( business_id, category_id ) ;

CREATE TABLE Yelper_friend
  (
    yelper_id  NUMBER NOT NULL ,
    friend_id NUMBER NOT NULL
  ) ;
ALTER TABLE Yelper_friend ADD CONSTRAINT Yelper_friend__IDX PRIMARY KEY ( yelper_id, friend_id ) ;

CREATE TABLE attribute
  (
    attribute_id    NUMBER NOT NULL ,
    attribute_name  VARCHAR2 (4000) ,
    attribute_value VARCHAR2 (4000)
  ) ;
ALTER TABLE attribute ADD CONSTRAINT attribute_PK PRIMARY KEY ( attribute_id ) ;

CREATE TABLE business
  (
    business_id     NUMBER NOT NULL ,
    business_id_str VARCHAR2 (30) ,
    business_name   VARCHAR2 (4000) ,
    address         VARCHAR2 (4000) ,
    city            VARCHAR2 (4000) ,
    state           VARCHAR2 (4000) ,
    latitude        NUMBER (18,15) ,
    longitude       NUMBER (18,15) ,
    stars           NUMBER (2,1) ,
    review_count    NUMBER ,
    business_open   VARCHAR2 (4000)
  ) ;
ALTER TABLE business ADD CONSTRAINT business_PK PRIMARY KEY ( business_id ) ;

CREATE TABLE category
  (
    category_id   NUMBER NOT NULL ,
    category_name VARCHAR2 (4000)
  ) ;
ALTER TABLE category ADD CONSTRAINT category_PK PRIMARY KEY ( category_id ) ;

CREATE TABLE checkin
  (
    checkin_id  NUMBER NOT NULL ,
    business_id NUMBER
  ) ;
ALTER TABLE checkin ADD CONSTRAINT checkin_PK PRIMARY KEY ( checkin_id ) ;

CREATE TABLE checkin_info
  (
    checkin_info_id NUMBER NOT NULL ,
    checkin_time    VARCHAR2 (4000) ,
    checkin_count   NUMBER ,
    checkin_id      NUMBER NOT NULL
  ) ;
ALTER TABLE checkin_info ADD CONSTRAINT checkin_info_PK PRIMARY KEY ( checkin_info_id ) ;

CREATE TABLE complement
  (
    complement_id    NUMBER NOT NULL ,
    complement_type  VARCHAR2 (4000) ,
    complement_count NUMBER ,
    yelper_id        NUMBER
  ) ;
ALTER TABLE complement ADD CONSTRAINT complement_PK PRIMARY KEY ( complement_id ) ;

CREATE TABLE elite_year
  (
    elite_year_id NUMBER NOT NULL ,
    elite_year VARCHAR2 (4000)
  ) ;
ALTER TABLE elite_year ADD CONSTRAINT elite_year_PK PRIMARY KEY ( elite_year_id ) ;

CREATE TABLE hours
  (
    hours_id    NUMBER NOT NULL ,
    hours_day   VARCHAR2 (4000) ,
    hours_open  VARCHAR2 (4000) ,
    hours_tim   VARCHAR2 (4000) ,
    business_id NUMBER
  ) ;
ALTER TABLE hours ADD CONSTRAINT hours_PK PRIMARY KEY ( hours_id ) ;

CREATE TABLE neighborhood
  (
    neighborhood_id   NUMBER NOT NULL ,
    neighborhoor_name VARCHAR2 (4000)
  ) ;
ALTER TABLE neighborhood ADD CONSTRAINT neighborhood_PK PRIMARY KEY ( neighborhood_id ) ;

CREATE TABLE review
  (
    review_id   NUMBER NOT NULL ,
    yelper_id   NUMBER ,
    stars       NUMBER (2,1) ,
    text        VARCHAR2 (4000) ,
    review_date DATE ,
    business_id NUMBER
  ) ;
ALTER TABLE review ADD CONSTRAINT review_PK PRIMARY KEY ( review_id ) ;

CREATE TABLE tip
  (
    tip_id      NUMBER NOT NULL ,
    text        VARCHAR2 (4000) ,
    yelper_id   NUMBER ,
    tip_date    DATE ,
    likes       NUMBER ,
    business_id NUMBER
  ) ;
ALTER TABLE tip ADD CONSTRAINT tip_PK PRIMARY KEY ( tip_id ) ;

CREATE TABLE yelper
  (
    yelper_id       NUMBER NOT NULL ,
    yelper_id_str   VARCHAR2 (30) ,
    yelper_name     VARCHAR2 (4000) ,
    review_count    NUMBER ,
    average_stars   NUMBER (18,17) ,
    yelping_since   DATE ,
    fans            NUMBER
  ) ;
ALTER TABLE yelper ADD CONSTRAINT yelper_PK PRIMARY KEY ( yelper_id ) ;

CREATE TABLE vote
  (
    vote_id    NUMBER NOT NULL ,
    vote_type  VARCHAR2 (4000) ,
    vote_count NUMBER
  ) ;
ALTER TABLE vote ADD CONSTRAINT vote_PK PRIMARY KEY ( vote_id ) ;

ALTER TABLE Business_neighorhoor ADD CONSTRAINT FK_ASS_1 FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE Elite_year_yelper ADD CONSTRAINT FK_ASS_10 FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE Business_category ADD CONSTRAINT FK_ASS_12 FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE Business_category ADD CONSTRAINT FK_ASS_13 FOREIGN KEY ( category_id ) REFERENCES category ( category_id ) ;

ALTER TABLE Yelper_friend ADD CONSTRAINT FK_ASS_19 FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE Business_neighorhoor ADD CONSTRAINT FK_ASS_2 FOREIGN KEY ( neighborhood_id ) REFERENCES neighborhood ( neighborhood_id ) ;

ALTER TABLE Yelper_friend ADD CONSTRAINT FK_ASS_20 FOREIGN KEY ( friend_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE Attribute_business ADD CONSTRAINT FK_ASS_3 FOREIGN KEY ( attribute_id ) REFERENCES attribute ( attribute_id ) ;

ALTER TABLE Attribute_business ADD CONSTRAINT FK_ASS_4 FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE Review_vote ADD CONSTRAINT FK_ASS_5 FOREIGN KEY ( review_id ) REFERENCES review ( review_id ) ;

ALTER TABLE Review_vote ADD CONSTRAINT FK_ASS_6 FOREIGN KEY ( vote_id ) REFERENCES vote ( vote_id ) ;

ALTER TABLE Yelper_vote ADD CONSTRAINT FK_ASS_7 FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE Yelper_vote ADD CONSTRAINT FK_ASS_8 FOREIGN KEY ( vote_id ) REFERENCES vote ( vote_id ) ;

ALTER TABLE Elite_year_yelper ADD CONSTRAINT FK_ASS_9 FOREIGN KEY ( elite_year_id ) REFERENCES elite_year ( elite_year_id ) ;

ALTER TABLE checkin ADD CONSTRAINT checkin_business_FK FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE checkin_info ADD CONSTRAINT checkin_info_checkin_FK FOREIGN KEY ( checkin_id ) REFERENCES checkin ( checkin_id ) ;

ALTER TABLE complement ADD CONSTRAINT complement_user_FK FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE hours ADD CONSTRAINT hours_business_FK FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE review ADD CONSTRAINT review_business_FK FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE review ADD CONSTRAINT review_user_FK FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;

ALTER TABLE tip ADD CONSTRAINT tip_business_FK FOREIGN KEY ( business_id ) REFERENCES business ( business_id ) ;

ALTER TABLE tip ADD CONSTRAINT tip_user_FK FOREIGN KEY ( yelper_id ) REFERENCES yelper ( yelper_id ) ;


-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            20
-- CREATE INDEX                             0
-- ALTER TABLE                             42
-- CREATE VIEW                              0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- TSDP POLICY                              0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
