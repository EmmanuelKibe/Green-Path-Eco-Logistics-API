import os
import django

# 1. Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green_path.settings') 

# 2. Initialize Django apps (Crucial Fix!)
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if not password:
        print("❌ Error: DJANGO_SUPERUSER_PASSWORD not set in environment variables.")
        return

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Superuser '{username}' created successfully!")
    else:
        print(f"ℹ️ Superuser '{username}' already exists.")

if __name__ == "__main__":
    create_admin()