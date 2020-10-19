"""initial

Revision ID: c41126b443fe
Revises: 
Create Date: 2020-10-19 03:11:17.455550

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as su


# revision identifiers, used by Alembic.
revision = 'c41126b443fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account_type',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('alias', sa.String(32), nullable=False),
        sa.Column('title', sa.String(32), nullable=False),
        sa.Column('comment_limit', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('phone', sa.String(16), nullable=False),
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
        sa.Column('nickname', sa.String(64), nullable=True),
        sa.Column('avatar', sa.String(128), nullable=True),
        sa.Column('account_type_id', sa.Integer, sa.ForeignKey('account_type.id'), index=True, nullable=False),
        sa.Column('account_active_to', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_table(
        'tag',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(64), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(128), nullable=False),
        sa.Column('text', sa.String(512), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('account.id'), index=True, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_table(
        'comment',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('text', sa.String(512), nullable=False),
        sa.Column('author_id', sa.Integer, sa.ForeignKey('account.id'), index=True, nullable=False),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id'), index=True, nullable=False),
        sa.Column('parent_comment', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

    op.create_table(
        'post_tag',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('post_id', sa.Integer, sa.ForeignKey('post.id'), index=True, nullable=False),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id'), index=True, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('post_tag')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('tag')
    op.drop_table('account')
    op.drop_table('account_type')
