package main

import (
	"crypto/rsa"
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
	"net/url"

	jwt "github.com/dgrijalva/jwt-go"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

type Response struct {
	Status string
	Desc   string
	Token  string
}

type User struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Email    string `json:"email"`
	Id		 int	`json:"id"`
}

type Token struct {
	Token string `json:"token"`
}

var (
	verifyKey *rsa.PublicKey
	signKey   *rsa.PrivateKey
)

func Initialize(user string, password string, dbname string) *sql.DB {
	connectionString := fmt.Sprintf("%s:%s@/%s", user, password, dbname)
	var err error
	db, err := sql.Open("mysql", connectionString)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("conexion exitosa")

	return db
}

func Insert(username, password, email string) bool {
	var db *sql.DB
	db = Initialize("julianmacagno", "rivadavia850", "julian")

	if username == "" || password == "" || email == "" {
		return false
	}

	var insert = "insert into user values (NULL, '" + username + "','" + email + "','" + password + "');"
	fmt.Println(insert)
	_, err := db.Query(insert)
	if err != nil {
		return false
	}

	fmt.Println("insercion exitosa " + insert)

	defer db.Close()
	return true
}

func Update(oldusername, username, password, email string) (bool, string) {
	var db *sql.DB
	db = Initialize("julianmacagno", "rivadavia850", "julian")

	var update = "update user set name='" + username + "', password='" + password + "', email='" + email + "' where name='" + oldusername + "';"
	fmt.Println(update)
	_, err := db.Query(update)
	if err != nil {
		fmt.Println(err)
		return false, oldusername
	}

	fmt.Println("actualizacion exitosa " + update)

	defer db.Close()
	return true, username
}

func Select(mail, password string) (bool, string, int) {

	var db *sql.DB
	db = Initialize("julianmacagno", "rivadavia850", "julian")

	if mail == "" || password == "" {
		return false, "Error", -1
	}

	var query = "SELECT id, name FROM user WHERE email='" + mail + "' AND password='" + password + "';"
	fmt.Println(query)
	row, err := db.Query(query)
	if err != nil {
		panic(err.Error())
	}

	var name string
	var id int
	for row.Next() {
		err = row.Scan(&id, &name)
		if err != nil {
			panic(err.Error())
		}
		if name != "" {
			return true, name, id
		}
	}
	return false, "Error", -1
}

func loginUser(w http.ResponseWriter, r *http.Request) {

	if r.Body == nil {
		http.Error(w, "please send a request body", 400)
		return
	}

	var u User
	err := json.NewDecoder(r.Body).Decode(&u)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	var res bool
	var name string
	var id int
	res, name, id = Select(u.Email, u.Password)
	if res == true {
		u.Username = name
		u.Id = id
		tokenString := createToken(u)
		response := Response{"OK", "usuario logueado correctamente", tokenString}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)

	} else {

		response := Response{"ERROR", "logueado incorrecto", ""}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	}
}

func createToken(u User) string {
	token := jwt.NewWithClaims(jwt.SigningMethodRS256, jwt.MapClaims{
		"username": u.Username,
		"password": u.Password,
		"email": 	u.Email,
		"id" :		u.Id,
		"exp":      time.Now().Add(time.Minute * time.Duration(5)).Unix(),
		"iat":      time.Now().Unix(),
	})
	tokenString, err := token.SignedString(signKey)
	if err != nil {
		fmt.Println("Error while signing the token")
	}
	// fmt.Println(tokenString)
	return tokenString
}

func registerUser(w http.ResponseWriter, r *http.Request) {

	var u User
	if r.Body == nil {
		http.Error(w, "Please send a request body", 400)
		return
	}
	err := json.NewDecoder(r.Body).Decode(&u)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}

	var res = Insert(u.Username, u.Password, u.Email)
	if res == true {
		response := Response{"OK", "Usuario Registrado", ""}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	} else {
		response := Response{"ERROR", "No se pudo registrar el usuario", ""}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	}
}

func updateUser(w http.ResponseWriter, r *http.Request) {
	type UUser struct {
		OldUsername string `json:"oldusername"`
		Username    string `json:"username"`
		Password    string `json:"password"`
		Email       string `json:"email"`
		Id			int	   `json:"id"`
	}

	var u UUser
	if r.Body == nil {
		http.Error(w, "Please send a request body", 400)
		return
	}
	err := json.NewDecoder(r.Body).Decode(&u)
	if err != nil {
		http.Error(w, err.Error(), 400)
		return
	}
	var res, _ = Update(u.OldUsername, u.Username, u.Password, u.Email)
	if res == true {
		tokenString := createToken(User{u.Username, u.Password, u.Email, u.Id})
		response := Response{"OK", "Actualizado", tokenString}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	} else {
		response := Response{"ERROR", "No se pudo actualizar", ""}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	}
}

func getUser(w http.ResponseWriter, r *http.Request) {
	key, ok := r.URL.Query()["name"]
	if !ok || len(key[0]) < 1 {
		response := Response{"ERROR", "no parameter in URL", ""}
		result, err := json.Marshal(response)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	} else {
		var user User
		user = SelectByName(key[0])
		result, err := json.Marshal(user)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
		w.Header().Set("Content-Type", "application/json")
		w.Write(result)
	}

}

func SelectByName(username string) User {
	var db *sql.DB
	db = Initialize("julianmacagno", "rivadavia850", "julian")

	var query = "SELECT * FROM user WHERE name='" + username + "';"
	fmt.Println(query)
	row, err := db.Query(query)
	if err != nil {
		panic(err.Error())
	}

	var id int
	var name string
	var pass string
	var email string
	for row.Next() {
		err = row.Scan(&id, &name, &pass, &email)
		if err != nil {
			panic(err.Error())
		}
	}
	return User{name, pass, email, id}
}

func handleRequest() {
	myrouter := mux.NewRouter().StrictSlash(true)
	
	u, err := url.Parse("https://localhost:8082")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Listening on http://127.0.0.1:" + u.Port() + "/");

	myrouter.HandleFunc("/users/login", loginUser).Methods("POST")
	myrouter.HandleFunc("/users/register", registerUser).Methods("POST")
	myrouter.HandleFunc("/users/update", updateUser).Methods("PUT")
	myrouter.HandleFunc("/users/", getUser).Methods("GET")
	log.Fatal(http.ListenAndServe(":8082", myrouter))
}

func initKeys() {
	signBytes, _ := ioutil.ReadFile("keypair.priv")
	signKey, _ = jwt.ParseRSAPrivateKeyFromPEM(signBytes)
	verifyBytes, _ := ioutil.ReadFile("keypair.pub")
	verifyKey, _ = jwt.ParseRSAPublicKeyFromPEM(verifyBytes)
}

func main() {
	initKeys()
	handleRequest()
}
