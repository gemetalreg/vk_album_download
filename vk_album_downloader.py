from urllib.request import urlretrieve
import vk, os, time, math

# Авторизация

login = ''
password = ''
vk_id = ''

session = vk.AuthSession(app_id=vk_id, user_login=login, user_password=password) 

vkapi = vk.API(session, v ='5.122')


url = input('Ввведите url альбома vk ')

# Разбираем ссылку
album_id = url.split('/')[-1].split('_')[1]
owner_id = url.split('/')[-1].split('_')[0].replace('album', '')


photos_count = vkapi.photos.getAlbums(owner_id=owner_id, album_ids=album_id)['items'][0]['size']

counter = 0 # текущий счетчик
prog = 0 # процент загруженных
breaked = 0 # не загружено из-за ошибки
time_now = time.time() # время старта

#&nbsp;Создадим каталоги
if not os.path.exists('saved'):
    os.mkdir('saved')
photo_folder = 'saved/album{0}_{1}'.format(owner_id, album_id)
if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

def get_photo__with_opt_size(photo_obj, size="largest"):
    photo_size_i = 0
    height = 0

    photo_diff_sizes_obj = photo_obj['sizes']
    
    for i, photo_ex in enumerate(photo_diff_sizes_obj):
        cur_height = photo_ex['height']

        if cur_height > height:
            photo_size_i = i
            height = cur_height
    
    return photo_diff_sizes_obj[photo_size_i]

for j in range(math.ceil(photos_count / 1000)): # Подсчитаем&nbsp;сколько раз нужно получать список фото, так как число получится не целое - округляем в большую сторону
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=1000, offset=j*1000) #&nbsp;Получаем список фото
    for photo_obj in photos['items']: # объекты [0]['sizes']

        photo = get_photo__with_opt_size(photo_obj)
        counter += 1 # 'height'
        url = photo['url'] #&nbsp;Получаем адрес изображения

        prog = round(counter/photos_count * 100,2)
        print('Загружаю фото № {} из {}. Прогресс: {} %'.format(counter, photos_count, prog))
        
        try:
            urlretrieve(url, photo_folder + "/" + os.path.split(url)[1]) # Загружаем и сохраняем файл
        except Exception:
            print('Произошла ошибка, файл пропущен.')
            breaked += 1
            continue