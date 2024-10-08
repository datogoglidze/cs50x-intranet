"""table create users

Revision ID: 3155daf9a206
Revises:
Create Date: 2024-10-08 15:55:31.931884

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3155daf9a206"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='users' and xtype='U'
        )
        BEGIN
        CREATE TABLE [dbo].[users] (
            [id]       [NVARCHAR](36)  NOT NULL PRIMARY KEY,
            [username] [NVARCHAR](100) NOT NULL,
            [password] [NVARCHAR](200) NOT NULL
        )
        END
    """)


def downgrade() -> None:
    pass
