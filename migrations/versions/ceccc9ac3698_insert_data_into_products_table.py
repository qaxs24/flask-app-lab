"""Insert data into products table

Revision ID: ceccc9ac3698
Revises: 1b866bd526a4
Create Date: 2025-12-08 17:45:42.891564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceccc9ac3698'
down_revision = '1b866bd526a4'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO categories (name) VALUES ('Electronics')")
    op.execute("""
        INSERT INTO products (name, price, active, category_id) 
        SELECT 'Smart Watch', 200.0, 1, id FROM categories WHERE name = 'Electronics'
    """)
    op.execute("""
        INSERT INTO products (name, price, active, category_id) 
        SELECT 'Headphones', 50.0, 1, id FROM categories WHERE name = 'Electronics'
    """)


def downgrade():
    op.execute("DELETE FROM products WHERE name IN ('Smart Watch', 'Headphones')")
    op.execute("DELETE FROM categories WHERE name = 'Electronics'")
