> Скачать из репозитория проект: https://github.com/albajes/resizing

В основной папке, где находится файл docker-compose.yml должен лежать файл .env
В основной папке, где находится файл docker-compose.yml вводим команду:
> docker-compose up -d

На компьютере должен быть запущен docker

Один url адрес:
> /resize?width=50&height=50&filename=picture_name.jpeg

где
- #### width, height - нужные размеры изображения
- #### filename - имя файла(картинки)


Если в указанной в .env директории нет файла с именем filename, получаем исключение.
> Файл не найден. Код 400.

Если в указанной в .env директории есть файл с именем filename, ищем этот файл с указанными размерами, то есть:
> filename_width_height

width, height мы передали в запросе

Если в указанной в .env директории есть файл с именем filename_width_height, возвращаем его.

Если в указанной в .env директории нет файла с именем filename_width_height, то открываем файл с именем filename.
Меняем размер изображения на те размеры, что были переданы в запросе, сохраняем в директории с именем filename_width_height и возвращаем изображение.