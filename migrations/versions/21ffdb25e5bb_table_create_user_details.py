"""table create user_details

Revision ID: 21ffdb25e5bb
Revises: 3155daf9a206
Create Date: 2024-10-08 15:57:38.939198

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "21ffdb25e5bb"
down_revision: Union[str, None] = "3155daf9a206"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects
            WHERE name='user_details' and xtype='U'
        )
        BEGIN
        CREATE TABLE [dbo].[user_details] (
            [id]           [NVARCHAR](36)  NOT NULL PRIMARY KEY,
            [first_name]   [NVARCHAR](100),
            [last_name]    [NVARCHAR](100),
            [birth_date]   [NVARCHAR](10),
            [department]   [NVARCHAR](100),
            [email]        [NVARCHAR](100),
            [phone_number] [NVARCHAR](100)
        )
        END
    """)


def downgrade() -> None:
    pass
