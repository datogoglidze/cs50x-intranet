CREATE TABLE news
(
    [id]            [NVARCHAR](36)  NOT NULL PRIMARY KEY,
    [creation_date] [DATETIME2]     NOT NULL DEFAULT GETDATE(),
    [title]         [NVARCHAR](30)  NOT NULL,
    [content]       [NVARCHAR](MAX) NOT NULL
)
