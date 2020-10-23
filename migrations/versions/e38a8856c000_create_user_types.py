"""create_user_types

Revision ID: e38a8856c000
Revises: c41126b443fe
Create Date: 2020-10-20 06:37:57.704141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e38a8856c000'
down_revision = 'c41126b443fe'
branch_labels = None
depends_on = None


def upgrade():
    op.get_bind().execute("""
    INSERT INTO user_type (id, alias, title, comment_limit) 
    VALUES (1, 'default', 'Обычный', 3),
     (2, 'premium', 'Premium', NULL)
    """)


def downgrade():
    conn = op.get_bind()

    conn.execute('DELETE FROM user')
    conn.execute('DELETE FROM user_type')

    conn.execute('DROP TABLE post_tag CASCADE')
    conn.execute('DROP TABLE comment CASCADE')
    conn.execute('DROP TABLE post CASCADE')
    conn.execute('DROP TABLE tag CASCADE')
    conn.execute('DROP TABLE user CASCADE')
    conn.execute('DROP TABLE user_type CASCADE')
