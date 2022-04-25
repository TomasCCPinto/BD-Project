
from tokenize import Token
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2 as psy

def connetion_db():
    db = psy.connect(user = 'aulaspl', password = 'aulaspl', host = '127.0.0.1', database = "project")
    db.autocommit = False
    
    return db

def tokenise():
    conn   = connetion_db()
    pointer = conn.cursor()
    query    = "SELECT password FROM customer WHERE id_user <= 30 "
    pointer.execute(query)
    rows = pointer.fetchall()
    pointer.close()

    pointer = conn.cursor()
    
    cont=1
    for x in rows:
        token = generate_password_hash(password=x[0])
        print(check_password_hash(token,x[0]))
        
        pointer.execute(f"UPDATE customer SET password='{token}' WHERE id_user={cont}")
        cont+=1
    conn.commit()
    pointer.close()
    conn.close()
    print("tokenised")

if __name__ == "__main__": 
    tokenise()
    
