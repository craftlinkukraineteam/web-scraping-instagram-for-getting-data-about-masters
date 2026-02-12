# Instagram parser for getting data about masters

Цей парсер автоматизує пошук профілів в Instagram за ключовими словами (наприклад, "візажист Харків") і збирає базову інформацію про користувачів.

# Можливості парсера
- Автоматичний логінування в Instagram через Selenium WebDriver.
- Пошук профайлів за заданим ключовим словом.
- Автоматичний збір даних про:
   - nickname користувача;
   - ім'я;
   - біографію;
   - кількість підписників;
   - його навички та вміння;
- Збереження результатів у вигляді файлу Microsoft Excel (.xlsx) ("instagram_parser_for_getting_data_about_masters.xlsx")

# Технології, які використовуються
- Python 3;
- Selenium;
- WebDriver Manager;
- Pandas;
- Google Chrome;

# Як запустити
Встановіть залежності через консоль JetBrains PyCharm: 
```pip install selenium webdriver-manager pandas```

# Запустіть скрипт
Запустіть скрипт через консоль JetBrains PyCharm: 
```python.exe parser.py```
