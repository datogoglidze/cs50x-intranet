"""table create news

Revision ID: 3d16fa7fab02
Revises: dec5bf7e2384
Create Date: 2024-10-08 16:00:08.242755

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d16fa7fab02"
down_revision: Union[str, None] = "dec5bf7e2384"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='news' and xtype='U'
        )
        BEGIN
        CREATE TABLE [dbo].[news] (
            [id]            [NVARCHAR](36)  NOT NULL PRIMARY KEY,
            [creation_date] [DATETIME2]     NOT NULL DEFAULT GETDATE(),
            [title]         [NVARCHAR](30)  NOT NULL,
            [content]       [NVARCHAR](MAX) NOT NULL
        )
        END
    """)


def downgrade() -> None:
    pass
