import database
import psycopg2


def main():
    query = "SELECT * FROM customer;"


    try:
        with database.get_data_base() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                
                for row in cursor:
                    print(row)
                
                return

    except:
        print("FAILER")


if __name__ == "__main__":
    main()



