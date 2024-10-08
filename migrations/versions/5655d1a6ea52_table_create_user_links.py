"""table create user_links

Revision ID: 5655d1a6ea52
Revises: 21ffdb25e5bb
Create Date: 2024-10-08 15:58:44.347986

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5655d1a6ea52"
down_revision: Union[str, None] = "21ffdb25e5bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='user_links' and xtype='U'
        )
        BEGIN
        CREATE TABLE [dbo].[user_links] (
            [id]      [NVARCHAR](36) NOT NULL PRIMARY KEY,
            [user_id] [NVARCHAR](36),
            [name]    [NVARCHAR](50),
            [link]    [NVARCHAR](550)
        )
        END
    """)


def downgrade() -> None:
    pass
