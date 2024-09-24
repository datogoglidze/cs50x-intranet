CREATE TABLE documents
(
    [position]      INT IDENTITY (1, 1) NOT NULL PRIMARY KEY,
    [id]            [NVARCHAR](36)      NOT NULL UNIQUE,
    [user_id]       [NVARCHAR](36),
    [creation_date] [NVARCHAR](50),
    [category]      [NVARCHAR](50),
    [directory]     [NVARCHAR](100),
    [status]        [NVARCHAR](10)
)
