# База данных растений
# Категории: травы, овощи, фрукты, ягоды

PLANTS_DB = [
    {
        'id': 1,
        'name': 'Алоэ Вера',
        'description': 'Суккулент с лекарственными свойствами.',
        'care': 'Полив раз в 2-3 недели, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Aloe_vera_%28L%29_Burman.jpg/440px-Aloe_vera_%28L%29_Burman.jpg',
        'category': 'травы'
    },
    {
        'id': 2,
        'name': 'Монстера',
        'description': 'Тропическое растение с большими листьями.',
        'care': 'Полив 1-2 раза в неделю, рассеянный свет',
        'image_url': '1.jpg',
        'category': 'травы'
    },
    {
        'id': 3,
        'name': 'Фикус Бенджамина',
        'description': 'Популярное комнатное дерево.',
        'care': 'Полив 2-3 раза в неделю, яркий непрямой свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ficus_benjamina_02.jpg/440px-Ficus_benjamina_02.jpg',
        'category': 'травы'
    },
    {
        'id': 4,
        'name': 'Сансевиерия',
        'description': 'Неприхотливое растение "тещин язык".',
        'care': 'Полив раз в 2 недели, теневынослива',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Sansevieria_trifasciata_var._laurentii.jpg/440px-Sansevieria_trifasciata_var._laurentii.jpg',
        'category': 'травы'
    },
    {
        'id': 5,
        'name': 'Спатифиллум',
        'description': '"Женское счастье" с белыми цветами.',
        'care': 'Полив 2-3 раза в неделю, умеренный свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Spathiphyllum_wallisii_flower.jpg/440px-Spathiphyllum_wallisii_flower.jpg',
        'category': 'травы'
    },
    {
        'id': 6,
        'name': 'Базилик',
        'description': 'Ароматная кулинарная трава.',
        'care': 'Полив ежедневно, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Ocimum_basilicum_MHNT.jpg/440px-Ocimum_basilicum_MHNT.jpg',
        'category': 'травы'
    },
    {
        'id': 7,
        'name': 'Томат',
        'description': 'Популярный овощ для салатов и консервации.',
        'care': 'Полив 2-3 раза в неделю, много солнца',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Tomato_je.jpg/440px-Tomato_je.jpg',
        'category': 'овощи'
    },
    {
        'id': 8,
        'name': 'Огурец',
        'description': 'Сочный овощ для свежих салатов.',
        'care': 'Обильный полив, тепло и свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Cucumis_sativus_-_Köhler–s_Medizinal-Pflanzen_-_072.jpg/440px-Cucumis_sativus_-_Köhler–s_Medizinal-Pflanzen_-_072.jpg',
        'category': 'овощи'
    },
    {
        'id': 9,
        'name': 'Перец болгарский',
        'description': 'Сладкий перец, богатый витамином C.',
        'care': 'Полив умеренный, тепло',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Paprika_anthocyan.jpg/440px-Paprika_anthocyan.jpg',
        'category': 'овощи'
    },
    {
        'id': 10,
        'name': 'Яблоня',
        'description': 'Плодовое дерево с сочными фруктами.',
        'care': 'Полив раз в неделю, обрезка',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Apple_tree_with_fruit.jpg/440px-Apple_tree_with_fruit.jpg',
        'category': 'фрукты'
    },
    {
        'id': 11,
        'name': 'Лимон',
        'description': 'Цитрусовое дерево с кислыми плодами.',
        'care': 'Полив 2-3 раза в неделю, яркий свет',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Lemon_and_lime_fruit.jpg/440px-Lemon_and_lime_fruit.jpg',
        'category': 'фрукты'
    },
    {
        'id': 12,
        'name': 'Клубника',
        'description': 'Сладкая ягода с характерным ароматом.',
        'care': 'Полив регулярный, солнечное место',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Fragaria_x_ananassa_%27Florence%27.jpg/440px-Fragaria_x_ananassa_%27Florence%27.jpg',
        'category': 'ягоды'
    },
    {
        'id': 13,
        'name': 'Малина',
        'description': 'Кустарник с сладкими ягодами.',
        'care': 'Полив обильный, опора для кустов',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Raspberries_%28Rubus_idaeus%29.jpg/440px-Raspberries_%28Rubus_idaeus%29.jpg',
        'category': 'ягоды'
    },
    {
        'id': 14,
        'name': 'Черника',
        'description': 'Лесная ягода с антиоксидантами.',
        'care': 'Кислая почва, умеренный полив',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Vaccinium_corymbosum_%28Blueberry%29.jpg/440px-Vaccinium_corymbosum_%28Blueberry%29.jpg',
        'category': 'ягоды'
    }
]

CATEGORIES = ['травы', 'овощи', 'фрукты', 'ягоды']

def get_plant_by_id(plant_id: int):
    """Получить растение по ID"""
    return next((p for p in PLANTS_DB if p['id'] == plant_id), None)

def get_all_plants():
    """Получить список всех растений"""
    return PLANTS_DB

def get_plants_by_category(category: str):
    """Получить растения по категории"""
    return [p for p in PLANTS_DB if p.get('category') == category]

def get_categories():
    """Получить список всех категорий"""
    return CATEGORIES
