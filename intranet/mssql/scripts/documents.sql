CREATE TABLE documents
(
    [id]            [NVARCHAR](36) NOT NULL PRIMARY KEY,
    [user_id]       [NVARCHAR](36),
    [creation_date] [NVARCHAR](50),
    [category]      [NVARCHAR](50),
    [directory]     [NVARCHAR](100),
    [status]        [NVARCHAR](10)
)
