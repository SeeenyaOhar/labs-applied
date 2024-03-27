"""initial

Revision ID: 0e246589bc36
Revises: 
Create Date: 2024-03-27 19:43:48.602157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e246589bc36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('firstName', sa.String(), nullable=True),
    sa.Column('lastName', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('role', sa.Enum('teacher', 'student', name='role'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('teacher',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('diplomas', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('employment', sa.ARRAY(sa.String()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_thumbnail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_user',
    sa.Column('class', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('class', 'user')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('class_', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_'], ['class.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('request',
    sa.Column('class', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class'], ['class.id'], ),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('class', 'user')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_table('message')
    op.drop_table('class_user')
    op.drop_table('class_thumbnail')
    op.drop_table('class')
    op.drop_table('teacher')
    op.drop_table('user')
    # ### end Alembic commands ###
