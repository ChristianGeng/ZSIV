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


# 
ALTER TABLE MyModel_mymodel ADD UNIQUE (url);

SHOW TABLES LIKE 'Z%';
SHOW TABLES;



select * from ZSIV_journals;
select * from ZSIV_mitarbeiter; 
select * from ZSIV_majournal;

SELECT majo.*, j.*
from  ZSIV_majournal majo
RIGHT JOIN  ZSIV_journals j  on majo.Journal_id=j.id;


SELECT majo.*, j.*
from  ZSIV_majournal majo
LEFT JOIN  ZSIV_journals j  on majo.Journal_id=j.id;

-- double join to do the thingy ...
SELECT majo.*, j.*, ma.*
from  ZSIV_majournal majo
LEFT JOIN  ZSIV_journals j  on majo.Journal_id=j.id
LEFT JOIN  ZSIV_mitarbeiter ma on majo.MA_id=ma.id
order by j.Name;

SHOW INDEX FROM ZSIV_summaries;

desc ZSIV_majournal;
desc  ZSIV_journals;  
desc ZSIV_mitarbeiter; 
desc ZSIV_summaries; 
desc ZSIV_choice;


select * from ZSIV_journals;
select * from ZSIV_mitarbeiter;
select * from ZSIV_majournal;
select * from ZSIV_majournal WHERE Journal_id=4;
select * from ZSIV_mitarbeiter;


-- subscriptions for Bernd Brachial
select * from ZSIV_majournal WHERE MA_id=2;





select * from ZSIV_majournal;
select * from  ZSIV_question;
select * from  ZSIV_choice;



