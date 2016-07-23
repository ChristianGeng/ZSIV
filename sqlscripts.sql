-- Datenbankstruktur

mysql -u root -p
--- pass SQLADMIN
CREATE DATABASE ZSIV;

GRANT ALL ON ZSIV.* TO christian@'%' IDENTIFIED BY 'christian';
GRANT ALL ON ZSIV.* TO christian@'%' IDENTIFIED BY 'christian';
flush privileges; 

use ZSIV;
show tables;
--- nicht notwendig
-- CREATE USER christian@localhost IDENTIFIED BY 'christian';
sudo service mysql restart

--- DROP DATABASE ZSIV;






-- Abfragen

SHOW TABLES LIKE 'Z%';
SHOW TABLES;

-- Joins for Subscriptions
SELECT majo.*, j.*, ma.*
from  ZSIV_majournal majo
LEFT JOIN  ZSIV_journals j  on majo.Journal_id=j.id
LEFT JOIN  ZSIV_mitarbeiter ma on majo.MA_id=ma.id
order by ma.Nachname;

-- Versuch die komplette Liste von zu versendeten Artikeln zu generieren
select su.Journal_id,j.Name,su.Jahrgang,Heftnummer, ma.email, j.Name,j.id , su.SENT from ZSIV_summaries su 
INNER JOIN ZSIV_journals j on su.Journal_id=j.id
RIGHT JOIN ZSIV_majournal majo on j.id=majo.Journal_id
RIGHT JOIN ZSIV_mitarbeiter ma on majo.MA_id=ma.id;


SHOW INDEX FROM ZSIV_summaries;

desc ZSIV_majournal;
desc  ZSIV_journals;  
desc ZSIV_mitarbeiter; 
desc ZSIV_summaries; 

select * from ZSIV_journals;
select * from ZSIV_mitarbeiter;
select * from ZSIV_majournal;
select * from ZSIV_majournal WHERE Journal_id=4;
select SENT, Journal_id, Jahrgang, Heftnummer from ZSIV_summaries;


-- subscriptions for Bernd Brachial
select * from ZSIV_majournal WHERE MA_id=2;




