CREATE TABLE documents
(
    [id]            [NVARCHAR](36) NOT NULL PRIMARY KEY,
    [user_id]       [NVARCHAR](36),
    [creation_date] [DATETIME2]    NOT NULL DEFAULT GETDATE(),
    [category]      [NVARCHAR](50),
    [directory]     [NVARCHAR](100),
    [status]        [NVARCHAR](10)
)
