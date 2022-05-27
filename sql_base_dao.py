import sqlite3
import json


# класс для управления подключенной базой данных
class SQLBaseDAO:

    def __init__(self, path_database):
        self.path_database = path_database

    def connect(self):
        """
        Метод для подключения к базе данных
        возвращает cursor
        """
        with sqlite3.connect(self.path_database) as connection:
            cursor = connection.cursor()
            return cursor

    def search_title(self, title):
        """
        Метод ищет фильм по названию в базе данных, и возвращает словарь с информацией об этом фильме
        :return dict:
        """
        # выполняем подключение к базе данных
        cursor = self.connect()
        # создаем запрос к базе данных
        sql_query = f""" 
                    SELECT `title`, `country`, `release_year`, `listed_in`, `description`
                    FROM netflix 
                    WHERE `title` LIKE '{title}%' 
                    AND `type` = 'Movie'
                    ORDER BY `release_year` DESC 
                    LIMIT 1
                    """
        # выполняем запрос
        cursor.execute(sql_query)
        # получаем данные из запроса
        result = cursor.fetchall()
        # создаем и заполняем словарь полученными данными
        film_title = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4]
        }

        return film_title

    def search_by_range_year(self, from_release_year, to_release_year):
        """
        Поиск фильмов по диапазону лет выпуска
        :return список со словарями:
        """
        cursor = self.connect()
        sql_query = f"""
                    SELECT `title`, `release_year` FROM netflix
                    WHERE `release_year` BETWEEN {from_release_year} AND {to_release_year}
                    AND `type` = 'Movie'
                    ORDER BY `release_year` DESC
                    LIMIT 100
                    """
        cursor.execute(sql_query)

        title_results = []
        for item in cursor.fetchall():
            title_results.append(
                {
                    "title": item[0],
                    "release_year": item[1]
                }
            )

        return title_results

    def search_rating(self, *args):
        """
        Поиск контента по рейтингу
        :param args:
        :return список со словарями:
        """
        cursor = self.connect()
        # создаем список, в него будем складывать созданные словари
        result = []
        # выполняем цикл по args, если ввели несколько аргументов
        for rating in args:
            sql_query = f"""
                        SELECT `title`, `rating`, `description` FROM netflix
                        WHERE `rating` = '{rating}'
                        ORDER BY `title`    
                        """
            cursor.execute(sql_query)
            # наполняем словарь и добавляем в result[]
            for item in cursor.fetchall():
                result.append(
                    {
                        "title": item[0],
                        "rating": item[1],
                        "description": item[2]
                    }
                )

        return result

    def search_genre(self, genre):
        """
        Поиск фильмов по жанру
        :param genre:
        :return список со словарями:
        """
        cursor = self.connect()
        sql_query = f"""
                    SELECT `title`, `description`, `listed_in` FROM netflix
                    WHERE `listed_in` LIKE '%{genre}%'
                    ORDER BY `release_year` DESC
                    LIMIT 10
                    """
        cursor.execute(sql_query)
        result = []
        for item in cursor.fetchall():
            result.append(
                {
                    "title": item[0],
                    "description": item[1]
                }
            )

        return result

    def search_actor(self, actor_1, actor_2):
        """
        Поиск актеров которые играют с введенным дуэтом более двух раз
        """
        cursor = self.connect()
        sql_query = f"""
                    SELECT `cast` FROM netflix
                    WHERE `cast` LIKE '%{actor_1}%' 
                    AND `cast` LIKE '%{actor_2}%'
                    AND `cast` != ''
                    """

        cursor.execute(sql_query)
        # создаю пустой список для актеров
        list_actors = []
        # Перебираю список с кортежами
        for item in cursor.fetchall():
            # актеров разделяю через сплит и добавляю их в list_actors
            list_actors.extend(item[0].split(', '))

        result = set()
        # перебираю список с актерами
        for actor in list_actors:
            # проверяю число вхождений для каждого актера
            count = list_actors.count(actor)
            # исключаю актеров из поиска
            if actor in [actor_1, actor_2]:
                continue
            # если количество вхождений больше 2, то добавляю акторов в множество
            if count > 2:
                result.add(actor)

        return list(result)

    def search_movie(self, type_element, release_year, genre):
        """
        Поиск контента по его типу, году выпуска и жанру
        :return: возвращает json файл с названием и описанием
        """
        cursor = self.connect()
        sql_query = f"""
                    SELECT `title`, `description` FROM netflix
                    WHERE `type` = '{type_element}' 
                    AND `release_year` = '{release_year}'
                    AND `listed_in` LIKE '%{genre}%'
                    ORDER BY `release_year`
                    """
        cursor.execute(sql_query)

        list_movie = []
        for item in cursor.fetchall():
            list_movie.append(
                {
                    "title": item[0],
                    "description": item[1]
                }
            )

        return json.dumps(list_movie, indent=4, ensure_ascii=False)

# Проверка двух последних методов
# # test = SQLBaseDAO('netflix.db')
# # print(test.search_actor('Rose McIver', 'Ben Lamb'))
# # print(test.search_movie('Movie', 2010, 'action'))
