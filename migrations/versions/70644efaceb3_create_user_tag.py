"""create_user_tag

Revision ID: 70644efaceb3
Revises: e38a8856c000
Create Date: 2020-10-26 03:44:47.649209

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '70644efaceb3'
down_revision = 'e38a8856c000'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'user_tag' not in tables:
        op.create_table(
            'user_tag',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), index=True, nullable=False),
            sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), index=True, nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )


def downgrade():
    conn = op.get_bind()

    conn.execute('DELETE FROM user_tag')
    conn.execute('DROP TABLE user_tag')
