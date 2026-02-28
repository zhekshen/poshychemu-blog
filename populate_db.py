import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poshychemu_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post

def populate():
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (password: admin123)")

    user = User.objects.get(username='admin')

    # Create dummy posts
    posts_data = [
        {
            'title': 'Секреты ловли щуки на живца',
            'content': 'Ловля щуки на живца — один из самых старых и эффективных способов рыбалки. В этой статье мы разберем основные снасти и выбор места.',
        },
        {
            'title': 'Лучшие места для рыбалки в Карелии',
            'content': 'Карелия славится своими озерами. Мы подготовили список из 5 самых рыбных мест, которые стоит посетить каждому рыболову.',
        },
        {
            'title': 'Как выбрать первый спиннинг?',
            'content': 'Для новичка выбор спиннинга может стать настоящим испытанием. Разбираемся в тестах, строе и материалах бланков.',
        }
    ]

    for p in posts_data:
        if not Post.objects.filter(title=p['title']).exists():
            Post.objects.create(title=p['title'], content=p['content'], author=user)
            print(f"Post '{p['title']}' created")

if __name__ == '__main__':
    populate()
