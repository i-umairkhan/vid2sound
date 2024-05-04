import jwt,datetime,os
from flask import Flask,request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# login route
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return "Missing username or password", 401
    
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM user WHERE email LIKE %s", [auth.username])

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid Credensials", 401
        else:
            return createJWT(auth.username,os.environ.get("JWT_SECRECT"),True)
    else:
        return "Invalid Credensials", 401

# validate route
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing Credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRECT"),algorithms=["HS256"]) 
    
    except:
        return "Not Authorized", 401
    
    return decoded, 200

# JWT creation function
def createJWT(username,secret,exp):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": exp
        }, 
        secret, 
        algorithm="HS256"
    )

# main function
if __name__ == "__main__":
    server.run(port=5000,host="0.0.0.0")