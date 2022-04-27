# BotLearningEngWords
Бот для изучения английский слов

Функции: 
- изучение нового слова (/new), бот рандомно предлагает слово из списка анг слов
- добавление слов в ручную (/add)
- отображение словаря (/dictionary)
- прохождение теста (Выбор правильного перевода с анг на русский) (/test)
- перевод с английского на русский и наоборот (/translate)
- удаление слова из словаря (/delword)
- очистка словаря (/deldictionary)

Библиотеки 
1) TelegramBotAPI - для бота (pip install pyTelegramBotAPI)
2) google translate - для перевода (pip install googletrans)
3) pyenchant - для проверки правописания слов (pip install pyenchant)

БД SQLite
1) eng_words_dictionary - таблица английский слов (для команды /new)
2) user_dictionary - таблица для хранения изученных слов пользователями

