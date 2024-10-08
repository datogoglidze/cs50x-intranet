"""table create documents

Revision ID: dec5bf7e2384
Revises: 5655d1a6ea52
Create Date: 2024-10-08 15:59:24.742622

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dec5bf7e2384"
down_revision: Union[str, None] = "5655d1a6ea52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='documents' and xtype='U'
        )
        BEGIN
        CREATE TABLE [dbo].[documents] (
            [id]            [NVARCHAR](36) NOT NULL PRIMARY KEY,
            [user_id]       [NVARCHAR](36),
            [creation_date] [DATETIME2]    NOT NULL DEFAULT GETDATE(),
            [category]      [NVARCHAR](50),
            [directory]     [NVARCHAR](100),
            [status]        [NVARCHAR](10)
        )
        END
    """)


def downgrade() -> None:
    pass
