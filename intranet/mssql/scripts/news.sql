CREATE TABLE news
  (
     [position] INT IDENTITY(1, 1)  NOT NULL PRIMARY KEY,
     [id]       NVARCHAR(36)        NOT NULL UNIQUE,
     [title]    NVARCHAR(MAX),
     [content]  NVARCHAR(MAX),
  )
