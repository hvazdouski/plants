# База данных растений

PLANTS_DB = [
    {
        'id': 1,
        'name': 'Алоэ Вера',
        'description': 'Суккулент с лекарственными свойствами.',
        'care': 'Полив раз в 2-3 недели, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Aloe_vera_%28L%29_Burman.jpg/440px-Aloe_vera_%28L%29_Burman.jpg'
    },
    {
        'id': 2,
        'name': 'Монстера',
        'description': 'Тропическое растение с большими листьями.',
        'care': 'Полив 1-2 раза в неделю, рассеянный свет',
        'image_url': '1.jpg'
    },
    {
        'id': 3,
        'name': 'Фикус Бенджамина',
        'description': 'Популярное комнатное дерево.',
        'care': 'Полив 2-3 раза в неделю, яркий непрямой свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ficus_benjamina_02.jpg/440px-Ficus_benjamina_02.jpg'
    },
    {
        'id': 4,
        'name': 'Сансевиерия',
        'description': 'Неприхотливое растение "тещин язык".',
        'care': 'Полив раз в 2 недели, теневынослива',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Sansevieria_trifasciata_var._laurentii.jpg/440px-Sansevieria_trifasciata_var._laurentii.jpg'
    },
    {
        'id': 5,
        'name': 'Спатифиллум',
        'description': '"Женское счастье" с белыми цветами.',
        'care': 'Полив 2-3 раза в неделю, умеренный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Spathiphyllum_wallisii_flower.jpg/440px-Spathiphyllum_wallisii_flower.jpg'
    }
]

def get_plant_by_id(plant_id: int):
    """Получить растение по ID"""
    return next((p for p in PLANTS_DB if p['id'] == plant_id), None)

def get_all_plants():
    """Получить список всех растений"""
    return PLANTS_DB
