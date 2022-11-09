import pytest
from api import PetFriends
import os
from settings import valid_email, valid_password, invalid_email, invalid_password, infinit_password
pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status,result = pf.add_new_pet(auth_key, "Волк", "вых", '4', "images/1.jpeg")
    """Проверяем что можно добавить питомца с корректными данными"""
    assert status == 200

def test_add_new_pet_without_photo():
    """Проверяем возможность добавление питомца без фото """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_new_pet_without_photo(auth_key, "God", "dog", '4')
    # Проверяем что статус ответа равен 200
    assert status == 200



def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Скот", "кiт", '3', "images/1.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_photo_at_pet(pet_photo='images/1.jpeg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Тут Никого НЕТ!!!")

def test_successful_update_self_pet_info(name='Скот', animal_type='кiт', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Тут Никого НЕТ!!!") # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев

########### Теперь негативные тесты########################


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем на возможность введения непровильных данных(111) эл.почты """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    with pytest.raises(AssertionError):
        assert status == 403
        assert 'key' in result
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем на возможность введения пустого пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    with pytest.raises(AssertionError):
        assert status == 403
        assert 'key' in result

def test_get_api_key_for_invalid_infinit_password(email=valid_email, password=infinit_password):
    """ Проверяем на возможность введения бесконечно большого пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    with pytest.raises(AssertionError):
     assert status == 403
     assert 'key' in result

def test_add_new_pet_with_invalid_data():
    """Проверяем на возможность добавления питомца с отрицательным значением в возрасте"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status,result = pf.add_new_pet(auth_key, "Волк", "вых", '-4', "images/1.jpeg")
    if status == 200:
        raise Exception("Отрицательное занчение в возрасте!")
    else:
        assert status == 400
        assert 'key' in result

def test_add_new_pet_with_invalid_data1():
    """Проверяем на возможность добавления питомца со специальными символами вместо имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status,result = pf.add_new_pet(auth_key, "@!#$%^&*", "@!#$%^&*", '1', "images/1.jpeg")
    if status == 200:
        raise Exception("Можно вводить специальные символы вместо букв!")
    else:
        assert status == 400
        assert 'key' in result

def test_add_new_pet_with_invalid_data2():
    """Проверяем на возможность добавления питомца с пустыми данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_new_pet_without_photo(auth_key, "", "", '')

    if status == 200:
        raise Exception("Можно добавить питомца с пустыми данными!")
    else:
        assert status == 400
        assert 'key' in result
def test_add_new_pet_with_invalid_data3():
    """Проверка с негативным сценарием. Добавления питомца имя которого превышает 10 слов"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_new_pet_without_photo(auth_key, "АКТЁР, РЕЖИССЁР, МИСТЕР ВСЕЛЕННАЯ, ПОЛИГЛОТ, ЧЕМПИОН МИРА ПО БОУЛИНГУ , ПОБЕДИТЕЛЬ КОНКУРСА ГУБЫ всех времён и народов, СЦЕНАРИСТ, ПАРОХОД, СТРАЖ ГАЛАКТИКИ, КОМЕДИАНТ, "
                                                            "УЛЬТРАМАРИН, ЛУЧШИЙ ДРУГ АРНОЛЬДА ШВАРЦНЕГГЕРА, СОЗДАТЕЛЬ ХЭВИ-МЕТАЛЛА, ХУДОЖНИК, ОПЕРАТОР, ХОКАГЕ, ПРЕЗИДЕНТ ЮГОСЛАВИИ, ВЛАДЕЛЕЦ ЛИЧНОГО ТИРАНОЗВРА, КНЯЗЬ НОВГОРОДСКИЙ, КОРОЛЬ ШАМАНОВ, ЭКСТРАСЕНС, АВТОР БИБЛИИ, ГРОЗА СЕМИ МОРЕЙ, ЛИТЕРАТОР,ГАЛАКТУС, "
                                                            "ПОБЕДИТЕЛЬ БИТВЫ РОБОТОВ 2002, УРУКХАЙ, ПОВОДЫРЬ, ИКС-МЭН, ИМПЕРАТОР ЧЕЛОВЕЧЕСТВА, ГАЛЬСКИЙ ДРУИД, МЕТАТЕЛЬ ЯДРА И ИКРЫ, ДОВАКИН, ХРАНИТЕЛЬ ЗОЛОТОГО ГЛОБУСА, ПИРАМИДОГОЛОВЫЙ, "
                                                            "ВИТАМИН С, ХОЗЯИН МУРОМСКИХ ЛЕСОВ, ПОВЕЛИТЕЛЬ ВРЕМЕНИ, ВДОХНОВИТЕЛЬ НЕКРОНОМИКОНА, СТРЕЛОК, ЧЕМПИОН ПО СКАЧКАМ 1918 года, АГЕНТ 007, АРККАНЦЛЕР НЕЗРИМОГО УНИВЕРСИТЕТА, КОСМИЧЕСКИЙ КОВБОЙ, МАТЬ ДРАКОНОВ, КАРАТИСТ, СТРОИТЕЛЬ ПИРАМИД, БЭТМЕН, ИЗОБРЕТАТЕЛЬ ЛОЖКИ, АВАТАР, ЗАДАЮЩИЙ ТОН ВСЕЙ КОМНАТЕ, ЧУПАКАБРА, СТАЛКЕР, ФАРАОН, ОХОТНИК НА МАМОНТОВ, ЗНАКО ЗОДИАКА, СПАСИТЕЛЬ ЧЕЛОВЕЧЕСТВА 21 ДЕКАБРЯ 2012 ГОДА, ВЕТЕРАН КУЛИКОВСКОЙ БИТВЫ, НИЦШЕАНСКИЙ СВЕРХЧЕЛОВЕК, СЕКС-СИМВОЛ, СЕКС-ЗНАК, СЕКС-НАМЁК, АССАСИН, НАШ ПАРЕНЬ В ГОЛЛИВУДЕ, БОГ ЛЮБВИ У ДРЕВНИХ ШУМЕРОВ, ПОБЕДИТЕЛЬ ВОЛГОГРАДСКОГО ЧЕМПИОНАТА ПО ШАХМАТАМ СРЕДИ ЮНИОРОВ 2012, ГЛАДИАТОР, "
                                                            "ОХОТНИК НА ВАМПИРОВ и КОРОНОВАННЫЙ МУКОМОЛ ВСЕЯ РУСИ", "Алекс Н.", '')
    if status == 200:
        raise Exception("Возможно добавить питомца имя которого превышает 10 слов")
    else:
        assert status == 400
        assert 'key' in result

def test_add_new_pet_with_invalid_data4():
    """Проверка с негативным сценарием. Добавления питомца с породой которая превышает 10 слов"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_new_pet_without_photo(auth_key, "Волк-тигр", "ньюфаундленд миттельшнауцер ньюфаундленд миттельшнауцер ньюфаундленд миттельшнауцер ньюфаундленд миттельшнауцерньюфаундленд миттельшнауцерньюфаундленд миттельшнауцер", '4')
    if status == 200:
        raise Exception("Возможно добавить питомца название породы которого превышает 10 слов")
    else:
        assert status == 400
        assert 'key' in result
