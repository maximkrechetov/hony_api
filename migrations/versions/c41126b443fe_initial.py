"""initial

Revision ID: c41126b443fe
Revises: 
Create Date: 2020-10-19 03:11:17.455550

"""
from alembic import op
from sqlalchemy.engine.reflection import Inspector
import sqlalchemy as sa
import sqlalchemy_utils as su


# revision identifiers, used by Alembic.
revision = 'c41126b443fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()

    if 'user_type' not in tables:
        op.create_table(
            'user_type',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('alias', sa.String(32), nullable=False),
            sa.Column('title', sa.String(32), nullable=False),
            sa.Column('comment_limit', sa.Integer, nullable=True),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )

    if 'user' not in tables:
        op.create_table(
            'user',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('phone', sa.String(16), nullable=False, unique=True),
            sa.Column(
                'password',
                su.PasswordType(
                    schemes=[
                        'pbkdf2_sha512',
                        'md5_crypt'
                    ],
                    deprecated=['md5_crypt']
                ),
                nullable=False
            ),
            sa.Column('nickname', sa.String(64), nullable=False, unique=True),
            sa.Column('first_name', sa.String(32), nullable=False),
            sa.Column('last_name', sa.String(32), nullable=False),
            sa.Column('avatar', sa.String(128), nullable=True),
            sa.Column('user_type_id', sa.Integer, sa.ForeignKey('user_type.id'), index=True, nullable=False),
            sa.Column('account_active_to', sa.DateTime, nullable=True),
            sa.Column('birth_date', sa.DateTime, nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )

    if 'tag' not in tables:
        op.create_table(
            'tag',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('title', sa.String(64), nullable=False),
            sa.Column('is_active', sa.Boolean, default=True),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )

    if 'post' not in tables:
        op.create_table(
            'post',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('title', sa.String(128), nullable=False),
            sa.Column('text', sa.Text, nullable=False),
            sa.Column('preview_text', sa.String(300), nullable=False),
            sa.Column('cover', sa.String(64), nullable=True),
            sa.Column('author_id', sa.Integer, sa.ForeignKey('user.id'), index=True, nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )

    if 'comment' not in tables:
        op.create_table(
            'comment',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('text', sa.String(512), nullable=False),
            sa.Column('author_id', sa.Integer, sa.ForeignKey('user.id'), index=True, nullable=False),
            sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id'), index=True, nullable=False),
            sa.Column('parent_comment', sa.Integer, nullable=True),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )

    if 'post_tag' not in tables:
        op.create_table(
            'post_tag',
            sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id'), index=True, nullable=False),
            sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), index=True, nullable=False),
            sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
            sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
        )


def downgrade():
    pass
