CREATE TABLE news
(
    [id]            [NVARCHAR](36)  NOT NULL PRIMARY KEY,
    [creation_date] [NVARCHAR](50)  NOT NULL,
    [title]         [NVARCHAR](30) NOT NULL,
    [content]       [NVARCHAR](MAX) NOT NULL
)
