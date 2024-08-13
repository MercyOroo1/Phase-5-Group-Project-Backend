"""empty message

<<<<<<<< HEAD:server/migrations/versions/0ca4649dc222_.py
Revision ID: 0ca4649dc222
Revises: 
Create Date: 2024-08-12 14:11:06.355542
========
Revision ID: f88286dbcb37
Revises: 
Create Date: 2024-08-13 22:27:14.395215
>>>>>>>> 6e2f8973a3ea80aa396f20338fafc4796d47c14e:server/migrations/versions/f88286dbcb37_.py

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
<<<<<<<< HEAD:server/migrations/versions/0ca4649dc222_.py
revision = '0ca4649dc222'
========
revision = 'f88286dbcb37'
>>>>>>>> 6e2f8973a3ea80aa396f20338fafc4796d47c14e:server/migrations/versions/f88286dbcb37_.py
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('license_number', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('experience', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('for_sale', sa.Integer(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=False),
    sa.Column('languages', sa.String(), nullable=False),
    sa.Column('agency_name', sa.String(), nullable=False),
    sa.Column('listed_properties', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('listing_fees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fee_amount', sa.Float(), nullable=False),
    sa.Column('fee_type', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('payment_frequency', sa.String(length=20), nullable=False),
    sa.Column('subscription_status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('square_footage', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('property_type', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('listing_status', sa.String(length=20), nullable=False),
    sa.Column('boosted', sa.Boolean(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], name='fk_property_agent'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('reset_token', sa.String(), nullable=True),
    sa.Column('token_expiry', sa.DateTime(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_user_role'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('agent_applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('license_number', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('experience', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.Column('for_sale', sa.Integer(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=False),
    sa.Column('sold', sa.Integer(), nullable=False),
    sa.Column('languages', sa.String(), nullable=False),
    sa.Column('agency_name', sa.String(), nullable=False),
    sa.Column('listed_properties', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
<<<<<<<< HEAD:server/migrations/versions/0ca4649dc222_.py
    op.create_table('boosted_properties',
========
    op.create_table('boosted_property',
>>>>>>>> 6e2f8973a3ea80aa396f20338fafc4796d47c14e:server/migrations/versions/f88286dbcb37_.py
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('boosted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], name='fk_contactmessage_agent'),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='fk_contactmessage_property'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_contactmessage_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('property_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('payment_status', sa.String(length=20), nullable=False),
    sa.Column('transaction_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('listing_fee_id', sa.Integer(), nullable=False),
<<<<<<<< HEAD:server/migrations/versions/0ca4649dc222_.py
    sa.ForeignKeyConstraint(['listing_fee_id'], ['listing_fees.id'], ),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
========
    sa.Column('agent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ),
    sa.ForeignKeyConstraint(['listing_fee_id'], ['listing_fees.id'], ),
>>>>>>>> 6e2f8973a3ea80aa396f20338fafc4796d47c14e:server/migrations/versions/f88286dbcb37_.py
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_id')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='fk_photo_property'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('photo_url', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('website', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('purchase_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('request_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_review_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saved_properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], name='fk_savedproperty_property'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_savedproperty_user'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('property_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=True),
    sa.Column('payment_status', sa.String(length=20), nullable=True),
    sa.Column('transaction_id', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['property_id'], ['properties.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_payment')
    op.drop_table('saved_properties')
    op.drop_table('reviews')
    op.drop_table('purchase_requests')
    op.drop_table('profiles')
    op.drop_table('photos')
    op.drop_table('payments')
    op.drop_table('features')
    op.drop_table('contact_messages')
<<<<<<<< HEAD:server/migrations/versions/0ca4649dc222_.py
    op.drop_table('boosted_properties')
========
    op.drop_table('boosted_property')
>>>>>>>> 6e2f8973a3ea80aa396f20338fafc4796d47c14e:server/migrations/versions/f88286dbcb37_.py
    op.drop_table('agent_applications')
    op.drop_table('users')
    op.drop_table('properties')
    op.drop_table('listing_fees')
    op.drop_table('roles')
    op.drop_table('agents')
    # ### end Alembic commands ###
