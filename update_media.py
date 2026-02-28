import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poshychemu_project.settings')
django.setup()

from blog.models import Post

def update_posts():
    # Images in media/blog_images/
    # Imag1.jpg, Imag2.jpg, Imag3.jpg, Imag4.jpg
    # Video in media/blog_videos/
    # Рыба есть ! 😱 Ловить надо уметь! 🎣🐡 #fishing #рыбалка #рыбалканафидер #fish #рыба-1080x1920-avc1.mp4

    posts = Post.objects.all().order_by('id')
    
    # Mapping files to posts
    # We have 3 posts from populate_db.py
    # Post 1: Секреты ловли щуки на живца
    # Post 2: Лучшие места для рыбалки в Карелии
    # Post 3: Как выбрать первый спиннинг?

    if posts.count() >= 1:
        p1 = posts[0]
        p1.image = 'blog_images/Imag1.jpg'
        p1.video = 'blog_videos/Рыба есть ! 😱 Ловить надо уметь! 🎣🐡 #fishing #рыбалка #рыбалканафидер #fish #рыба-1080x1920-avc1.mp4'
        p1.save()
        print(f"Updated '{p1.title}' with image1 and video")

    if posts.count() >= 2:
        p2 = posts[1]
        p2.image = 'blog_images/Imag2.jpg'
        p2.save()
        print(f"Updated '{p2.title}' with image2")

    if posts.count() >= 3:
        p3 = posts[2]
        p3.image = 'blog_images/Imag3.jpg'
        p3.save()
        print(f"Updated '{p3.title}' with image3")

    # If there are more posts or we want to create a 4th one for the 4th image
    if posts.count() < 4:
        from django.contrib.auth.models import User
        admin = User.objects.get(username='admin')
        p4 = Post.objects.create(
            title='Зимняя рыбалка: что нужно знать?',
            content='Зимняя рыбалка — это особое удовольствие и риск. В этой статье мы расскажем о подготовке снаряжения и безопасности на льду.',
            author=admin,
            image='blog_images/Imag4.jpg'
        )
        print(f"Created new post '{p4.title}' with image4")

if __name__ == '__main__':
    update_posts()
