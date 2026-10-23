import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinema.db")


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS movies")
        cursor.execute(
            """
            CREATE TABLE movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration INTEGER,
                release_year INTEGER
            )
            """
        )
        connection.commit()
        print("Таблицю movies створено.")
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Помилка створення таблиці: {error}")


def insert_movies(connection):
    movies = [
        ("Початок", "Фантастика", 148, 2010),
        ("Хрещений батько", "Драма", 175, 1972),
        ("Темний лицар", "Бойовик", 152, 2008),
        ("Форрест Гамп", "Драма", 142, 1994),
        ("Матриця", "Фантастика", 136, 1999),
        ("Король Лев", "Мультфільм", 88, 1994),
    ]
    try:
        cursor = connection.cursor()
        cursor.executemany(
            "INSERT INTO movies (title, genre, duration, release_year) VALUES (?, ?, ?, ?)",
            movies,
        )
        connection.commit()
        print(f"Додано фільмів: {cursor.rowcount}")
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Помилка додавання даних: {error}")


def update_movie(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE movies SET duration = ? WHERE title = ?",
            (150, "Темний лицар"),
        )
        connection.commit()
        print(f"Оновлено записів: {cursor.rowcount}")
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Помилка оновлення даних: {error}")


def delete_movie(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM movies WHERE title = ?", ("Форрест Гамп",))
        connection.commit()
        print(f"Видалено записів: {cursor.rowcount}")
    except sqlite3.Error as error:
        connection.rollback()
        print(f"Помилка видалення даних: {error}")


def print_movies(rows):
    print(f"{'ID':<4}{'Назва':<22}{'Жанр':<14}{'Тривалість':<12}{'Рік':<6}")
    print("-" * 58)
    for row in rows:
        duration = f"{row[3]} хв"
        print(f"{row[0]:<4}{row[1]:<22}{row[2]:<14}{duration:<12}{row[4]:<6}")


def show_all(connection, title):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, genre, duration, release_year FROM movies")
        print(f"\n{title}")
        print_movies(cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Помилка вибірки даних: {error}")


def show_by_genre(connection, genre):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title, genre, duration, release_year FROM movies WHERE genre = ?",
            (genre,),
        )
        print(f"\nФільми жанру '{genre}':")
        print_movies(cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Помилка вибірки даних: {error}")


def show_sorted_by_duration(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, title, genre, duration, release_year FROM movies ORDER BY duration DESC"
        )
        print("\nФільми, відсортовані за тривалістю (від найдовшого):")
        print_movies(cursor.fetchall())
    except sqlite3.Error as error:
        print(f"Помилка вибірки даних: {error}")


def main():
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        print("З'єднання з базою даних cinema.db встановлено.")

        create_table(connection)
        insert_movies(connection)
        show_all(connection, "Усі фільми після додавання:")

        update_movie(connection)
        delete_movie(connection)
        show_all(connection, "Усі фільми після оновлення та видалення:")

        show_by_genre(connection, "Фантастика")
        show_sorted_by_duration(connection)
    except sqlite3.Error as error:
        print(f"Помилка бази даних: {error}")
    finally:
        if connection is not None:
            connection.close()
            print("\nЗ'єднання з базою даних закрито.")


if __name__ == "__main__":
    main()