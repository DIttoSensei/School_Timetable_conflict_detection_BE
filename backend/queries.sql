-- create
CREATE TABLE COURSEITEM (
  Id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  lecturer_name TEXT NOT NULL,
  time_start TEXT NOT NULL,
  time_end TEXT NOT NULL
);

-- insert
INSERT INTO COURSEITEM VALUES (0001, 'Computer Architecture', '' , 'Mr Olubiyi', '8:30', '10:00');


-- fetch 
SELECT * FROM COURSEITEM;