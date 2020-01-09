# README

Скрипт предназначен для создания и наполнения яндекс коллекций из категорий и товаров интернет-магазина.

Для управления работой скрипта есть несколько переменных:
1. **log_type** - Способ логина в Яндекс 1 - через форму, 2 - через куки(после логина через форму создаётся файл __cookies.pkl__ который можно использовать для последующей авторизации).
1. **need_create** - Для указания нужно ли создавать коллекцию или наполнять уже существующую 1 - нужно, 0 - не нужно.
1. **mode_add** = 2 - Управление режимом добавления фото в коллекцию 1 - добавление как url, 2 - добавление как картинки.