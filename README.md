# Прогноз землятресений


В исследовании производится поиск возможной взаимосвязи гравитационного воздействия планет Солнечной системы на мощность и интенсивность землятресений на Земле.

![Карта сейсмической активности](/img/map_earthquakes.png "Карта сейсмической активности")
___

## 1. Источник данных
Сейчас данные загружаются в базу данных по API из https://earthquake.usgs.gov/earthquakes/search/

В предудущих версиях данные загружены из базы данных Федерального государственного бюджетного учреждения науки "Федеральный исследовательский центр Единая геофизическая служба Российской академии наук"

 http://eqru.gsras.ru/index.php?inc=main

 В файле содержатся сведения о более чем 160 000 зафиксированных землятресений на территории России начиная с 01.01.2003 г.
 
 ___
 ## 2. Загрузка и установка зависимостей (для Linux)
 Версия python - 3.10. Для работы с моделью необходимо:
 - скачать репозиторий и перейти в созданный каталог
 ```bash
 git clone https://github.com/RomanZorkin/temblor.git

 cd temblor
```
- установить необходимые зависимости python
```bash
 python -m venv venv

 source venv/bin/activate

 pip install poetry

 poetry init

 poetry install
 ```
 ___
 ## 3. Обучение модели
 Для обучения необходимо убедиться в наличии файла данных 'export.csv'. Далее достаточно выполнить код в jupyter notebook "train.ipynb". Обученная модель будет сохранена в файл "..._model.pkl", в заисимости от метода обучения (linear, lasso, ridge). Score модели не превышает 0,18.
 ![Точность предсказаний](/img/score.png "Точность предсказаний")
 ___
 ## 4. Получения прогноза землятресений

 Для получения прогноза необходимо открыть jupyter notebook "predict.ipynb". В ноутбуке будет использована ранее сохраненная модель "model.pkl". Далее необходимо задать желаемые праметры через переменные:
 ```python
 place = 'Barnaul, Russia'
date = "2022-01-01"  # начальная дата периода
period = 10  # длительность периода

magnitude_frame = predict_magnitude(place, date, period)
 ```
 - place - географическое название местности, для которой осуществляется прогноз в формате "Barnaul, Russia", "Moscow, Russia", "Kamchatka, Russia", "Caucasus, Russia" и т.д. Для поиска координат местности используется библиотека geopy. Формат названия местности также возможно посмотреть в документации. https://geopy.readthedocs.io/en/stable/index.html#
 - date - начальная дата периода в формате "2023-07-31", "2023/07/31"
 - period - количество дней прогноза (прогноз делается на каждый день). например на год - 365/366, на месяц - 30/31/28, на любой другой период.

 Результат будет получен в виде pandas Dataframe для удобства интрепретации.
 ```jupyter
        date	    magnitude
0	2022-01-01	2.009390
1	2022-01-02	2.014516
2	2022-01-03	2.036781
3	2022-01-04	2.041011
4	2022-01-05	2.044411
5	2022-01-06	2.046760
6	2022-01-07	2.048087
7	2022-01-08	2.048557
8	2022-01-09	2.044103
9	2022-01-10	2.032866
 ```

___
## 5. Параметры планет
В качестве праметров для обучения модели используются сведения о планетах, полученные с помощью библиотеки pyephem https://rhodesmill.org/pyephem/ на каждую дату.


## __ Запуск базы данных

Для старта проекта у вас должен быть установлен docker и docker-compose. И в корне проекта записан конфигурационный файл docker-compose.yml.

Источник - https://dev.to/titronium/clickhouse-server-in-1-minute-with-docker-4gf2

Запустите docker-compose, для старта контейнеров
```bash
docker-compose up -d
```
Дождитесь окончания скачивания и установки необходимых образов

### Конфигурация пользователя по умолчанию (суперпользователя)

Когда контейнер будет запущен, необходимо будет войти в его командную строку

```bash
docker-compose exec ch_server bash
```
Далее необходимо будет настроить пользователей, имеющих право доступа к базе данных. Установим текстовый редактор nano
```bash
apt-get update
apt-get install nano
```
Далее внесем изменения в конфигурационный файл, для предоставлению суперпользователю добавлять новых пользователей.
```bash
nano /etc/clickhouse-server/users.xml
```
Необходимо раскоментировать строки в настройках доступа суперполльзователя
```xml
..
<!-- User can create other users and grant rights to them. -->
<!-- <access_management>1</access_management> -->
..
```
В этом же файле можете установить пароль для этого пользователя

Источник - https://stackoverflow.com/questions/64166492/how-to-setup-an-admin-account-for-clickhouse

Для выхода из консоли контейнера введите
```bash
exit
```
И потребуется перезагрузка сервиса
```bash
docker-compose stop
docker-compose up -d
```
### Добавление новых пользователей
Запускаем клиента ClickHouse
```bash
docker-compose exec ch_server clickhouse-client
```
У вас появиться результат запуска клиента
```bash
ClickHouse client version 21.2.5.5 (official build).
Connecting to localhost:9000 as user default.
Connected to ClickHouse server version 21.2.5 revision 54447.

5175e561dffd :)
```
Это SQL консоль здесь стандартными командами добавляем пользователя
```bash
CREATE USER <имя пользователя> IDENTIFIED WITH sha256_password BY '<пароль пользователя>';
```
В дальнейшем, чтобы изменить набор привилегий и ролей пользователя, используйте запросы GRANT и REVOKE. Например, выдайте пользователю права на чтение всех объектов в определенной базе данных
```bash
GRANT SELECT ON <имя базы данных>.* TO <имя пользователя>;
```
Источник https://cloud.yandex.ru/docs/managed-clickhouse/operations/cluster-users


## Создание первой базы данных и таблицы
Источник https://clickhouse.com/docs/en/quick-start

Воспользуемся предыдущей командой для запуска консоли SQL
```bash
sudo docker-compose exec ch_server clickhouse-client
```
И далее вводим необходимые нам команды
```sql
SHOW databases

CREATE DATABASE IF NOT EXISTS quake
```

