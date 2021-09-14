## Обучение моделей Gradient Boosting для решения задач Валидация и Группировки

### 1. Валидация задач на три группы: Good/Agood/Bad
    - good (хорошие)
    - bad (пложие) 
    - agood (скорее хорошие)


### 2. Определение группы задачи (17 групп)
    - Multiplication and division
    - Addition and subtraction
    - Fractions
    - Mixed operations
    - Measurements
    - Figures
    - Number
    - Modelling
    - Geometry
    - Time
    - Comparison
    - Estimation
    - Logic
    - Series and pattern
    - Graph
    - Probability
    - Money
    - Other

### Установка зависимостей и запуск проекта
    Для работы проекта необходимо установить следующие зависимости:
    pip install spacy
    pip install pandas
    pip install jupyter
    pip install anaconda
    pip install sklearn
    pip install matplotlib
    spacy download en_core_web_sm
    
## Быстрый старт обучения моделей

### Подготовка данных (необязательно)
1. Запускаем ноутбук **Create lemma statistics.ipynb** из главного раздела проекта. Данный скрипт собирает статистику всех лемм встречающихся в задачах датасета для дальнейшего обучения параметра, участвующего в обучении модели.
2. Запускаем ноутбук **Create Training DataSet.ipynb** из главного раздела проекта. Данный скрипт выполняет преобразование данных исходного датасета в данные, которые наилучшим образом подходят для обучения модели.

### Обучение модели Валидации задач по Good/Agood/Bad
- Запустие ноутбук **Training of validation model.ipynb** из главного раздела проекта и следуйте инструкциям.

### Обучение модели Группировки задач по 17 группам
- Запустите ноутбук **Training of grouping model.ipynb** из главного раздела проекта и следуйте инструкциям.
