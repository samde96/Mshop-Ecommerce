"""
Data migration script from MongoDB to PostgreSQL
Run: python migrate_from_mongodb.py
"""

import os
import sys
import django
from datetime import datetime
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mshop.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import UserProfile, Product, Order, OrderItem, Address, Payment, Blog

# MongoDB imports
import pymongo
from pymongo import MongoClient

def get_mongodb_connection():
    """Connect to MongoDB"""
    try:
        mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017')
        client = MongoClient(mongo_uri)
        db = client.get_database()
        return client, db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None


def migrate_users(mongo_db):
    """Migrate users from MongoDB to Django"""
    print("Migrating users...")
    users_collection = mongo_db['users']
    
    migrated_count = 0
    error_count = 0
    
    for mongo_user in users_collection.find():
        try:
            clerk_id = mongo_user.get('clerkId')
            if not clerk_id:
                print(f"Skipping user without clerkId")
                continue
            
            # Check if user already exists
            if User.objects.filter(username=clerk_id[:30]).exists():
                print(f"User {clerk_id} already exists, skipping...")
                continue
            
            email = mongo_user.get('email', f"{clerk_id}@mshop.local")
            name = mongo_user.get('name', 'User').split(' ')
            first_name = name[0] if len(name) > 0 else ''
            last_name = ' '.join(name[1:]) if len(name) > 1 else ''
            
            # Create Django user
            user = User.objects.create_user(
                username=clerk_id[:30],
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='temp_password_change_required'  # User should reset password
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                clerkId=clerk_id,
                avatar_url=mongo_user.get('imageUrl', ''),
                phone_number='',
                role='user'
            )
            
            migrated_count += 1
            print(f"✓ Migrated user: {email}")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error migrating user: {str(e)}")
    
    print(f"Users migration complete: {migrated_count} migrated, {error_count} errors\n")
    return migrated_count


def migrate_products(mongo_db):
    """Migrate products from MongoDB to Django"""
    print("Migrating products...")
    products_collection = mongo_db['products']
    
    migrated_count = 0
    error_count = 0
    
    for mongo_product in products_collection.find():
        try:
            user_id = mongo_product.get('userId')
            
            # Find the corresponding user
            user_profile = UserProfile.objects.filter(clerkId=user_id).first()
            if not user_profile:
                print(f"Skipping product, user {user_id} not found")
                continue
            
            user = user_profile.user
            
            # Map stock status
            stock_status = mongo_product.get('stockStatus', 'In_stock')
            stock = 10 if stock_status == 'In_stock' else (5 if stock_status == 'Limited_stock' else 0)
            
            images = mongo_product.get('image', [])
            image_url = images[0] if isinstance(images, list) and len(images) > 0 else ''
            
            # Create product
            product = Product.objects.create(
                name=mongo_product.get('name', 'Unnamed Product'),
                description=mongo_product.get('description', ''),
                price=Decimal(str(mongo_product.get('price', 0))),
                category=mongo_product.get('category', 'other').lower(),
                image_url=image_url,
                stock=stock,
                seller=user,
                is_active=True
            )
            
            migrated_count += 1
            print(f"✓ Migrated product: {product.name}")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error migrating product: {str(e)}")
    
    print(f"Products migration complete: {migrated_count} migrated, {error_count} errors\n")
    return migrated_count


def migrate_addresses(mongo_db):
    """Migrate addresses from MongoDB to Django"""
    print("Migrating addresses...")
    addresses_collection = mongo_db['addresses']
    
    migrated_count = 0
    error_count = 0
    
    for mongo_address in addresses_collection.find():
        try:
            user_id = mongo_address.get('userId')
            
            # Find the corresponding user
            user_profile = UserProfile.objects.filter(clerkId=user_id).first()
            if not user_profile:
                continue
            
            user = user_profile.user
            
            # Create address
            address = Address.objects.create(
                user=user,
                name=mongo_address.get('name', 'Default Address'),
                phone=mongo_address.get('phone', ''),
                street=mongo_address.get('street', ''),
                city=mongo_address.get('city', ''),
                state=mongo_address.get('state', ''),
                postal_code=mongo_address.get('postalCode', ''),
                country=mongo_address.get('country', 'Kenya'),
                is_default=mongo_address.get('isDefault', False)
            )
            
            migrated_count += 1
            print(f"✓ Migrated address: {address.name}")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error migrating address: {str(e)}")
    
    print(f"Addresses migration complete: {migrated_count} migrated, {error_count} errors\n")
    return migrated_count


def migrate_orders(mongo_db):
    """Migrate orders from MongoDB to Django"""
    print("Migrating orders...")
    orders_collection = mongo_db['orders']
    
    migrated_count = 0
    error_count = 0
    
    for mongo_order in orders_collection.find():
        try:
            user_id = mongo_order.get('userId')
            
            # Find the corresponding user
            user_profile = UserProfile.objects.filter(clerkId=user_id).first()
            if not user_profile:
                continue
            
            user = user_profile.user
            
            # Find shipping address
            address_id = mongo_order.get('address')
            shipping_address = None
            if address_id:
                shipping_address = Address.objects.filter(id=address_id).first()
            
            if not shipping_address:
                shipping_address = user.addresses.first()
            
            # Map order status
            mongo_status = mongo_order.get('status', 'Order Placed').lower()
            if 'placed' in mongo_status:
                order_status = 'pending'
            elif 'processing' in mongo_status:
                order_status = 'processing'
            elif 'shipped' in mongo_status:
                order_status = 'shipped'
            elif 'delivered' in mongo_status:
                order_status = 'delivered'
            elif 'cancelled' in mongo_status:
                order_status = 'cancelled'
            else:
                order_status = 'pending'
            
            payment_status = 'completed' if mongo_order.get('isPaid') else 'pending'
            
            # Create order
            order = Order.objects.create(
                order_id=mongo_order.get('_id', f"ORD-{migrated_count}"),
                user=user,
                total_amount=Decimal(str(mongo_order.get('amount', 0))),
                order_status=order_status,
                payment_status=payment_status,
                payment_method=mongo_order.get('paymentType', 'mpesa').lower(),
                shipping_address=shipping_address,
                mpesa_receipt_number=mongo_order.get('mpesaReceiptNumber', ''),
                created_at=mongo_order.get('date', datetime.now())
            )
            
            # Migrate order items
            items = mongo_order.get('items', [])
            for item in items:
                product_id = item.get('product')
                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.get('quantity', 1),
                        unit_price=product.price,
                        total_price=product.price * item.get('quantity', 1)
                    )
                except Product.DoesNotExist:
                    print(f"  ⚠ Product {product_id} not found for order item")
            
            migrated_count += 1
            print(f"✓ Migrated order: {order.order_id}")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error migrating order: {str(e)}")
    
    print(f"Orders migration complete: {migrated_count} migrated, {error_count} errors\n")
    return migrated_count


def migrate_blog_posts(mongo_db):
    """Migrate blog posts from MongoDB to Django"""
    print("Migrating blog posts...")
    blog_collection = mongo_db['blogs']
    
    migrated_count = 0
    error_count = 0
    
    for mongo_blog in blog_collection.find():
        try:
            author_id = mongo_blog.get('userId')
            
            # Find the corresponding user
            user_profile = UserProfile.objects.filter(clerkId=author_id).first()
            if not user_profile:
                # Use first admin user as fallback
                author = User.objects.filter(is_staff=True).first() or User.objects.first()
                if not author:
                    continue
            else:
                author = user_profile.user
            
            # Create blog post
            blog = Blog.objects.create(
                title=mongo_blog.get('title', 'Untitled'),
                slug=mongo_blog.get('slug', mongo_blog.get('_id', 'post')),
                content=mongo_blog.get('content', ''),
                excerpt=mongo_blog.get('excerpt', '')[:500],
                author=author,
                image_url=mongo_blog.get('image', ''),
                category=mongo_blog.get('category', 'other').lower(),
                is_published=mongo_blog.get('isPublished', False),
                views=mongo_blog.get('views', 0),
                created_at=mongo_blog.get('createdAt', datetime.now()),
                published_at=mongo_blog.get('publishedAt')
            )
            
            migrated_count += 1
            print(f"✓ Migrated blog: {blog.title}")
            
        except Exception as e:
            error_count += 1
            print(f"✗ Error migrating blog: {str(e)}")
    
    print(f"Blog migration complete: {migrated_count} migrated, {error_count} errors\n")
    return migrated_count


def main():
    print("=" * 60)
    print("Starting MongoDB to PostgreSQL Migration")
    print("=" * 60 + "\n")
    
    client, mongo_db = get_mongodb_connection()
    if not mongo_db:
        print("Failed to connect to MongoDB")
        sys.exit(1)
    
    try:
        total_migrated = 0
        
        total_migrated += migrate_users(mongo_db)
        total_migrated += migrate_products(mongo_db)
        total_migrated += migrate_addresses(mongo_db)
        total_migrated += migrate_orders(mongo_db)
        total_migrated += migrate_blog_posts(mongo_db)
        
        print("=" * 60)
        print(f"Migration Complete! Total items migrated: {total_migrated}")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Verify data in Django admin: http://localhost:8000/admin/")
        print("2. Update Next.js frontend to use Django API")
        print("3. Test all functionality")
        
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        sys.exit(1)
    finally:
        if client:
            client.close()


if __name__ == '__main__':
    main()
