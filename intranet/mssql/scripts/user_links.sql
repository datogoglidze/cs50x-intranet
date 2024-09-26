CREATE TABLE user_links
(
    [id]      [NVARCHAR](36) NOT NULL PRIMARY KEY,
    [user_id] [NVARCHAR](36),
    [name]    [NVARCHAR](50),
    [link]    [NVARCHAR](550)
)
