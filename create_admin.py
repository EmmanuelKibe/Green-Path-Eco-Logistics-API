import os
import django

# Set the settings path - replace 'green_path' with your actual project folder name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green_path.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Created superuser: {username}")
    else:
        print(f"ℹ️ Superuser {username} already exists.")
else:
    print("⚠️ Skipping superuser creation: Credentials not found in Env.")