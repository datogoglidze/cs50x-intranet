CREATE TABLE user_details
  (
     [id]           [NVARCHAR](36)  NOT NULL PRIMARY KEY,
     [first_name]   [NVARCHAR](100),
     [last_name]    [NVARCHAR](100),
     [birth_date]   [INT],
     [department]   [NVARCHAR](100),
     [email]        [NVARCHAR](100),
     [phone_number] [NVARCHAR](100),
  )
