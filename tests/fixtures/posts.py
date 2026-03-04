import pytest
from mixer.backend.django import Mixer
@pytest.fixture
def post_with_published_location(
        mixer: Mixer, user, published_location, published_category):
    from django.core.files.uploadedfile import SimpleUploadedFile
    from PIL import Image
    import io
    
    # Создаем тестовое изображение в памяти
    img = Image.new('RGB', (100, 100), color=(73, 109, 137))
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    # Создаем SimpleUploadedFile вместо ImageFile
    image_file = SimpleUploadedFile(
        name='test_image.jpg',
        content=img_io.read(),
        content_type='image/jpeg'
    )
    
    # Создаем пост
    post = mixer.blend(
        'blog.Post',
        is_published=True,
        location=published_location,
        category=published_category,
        author=user,
        image=image_file
    )
    return post
