FROM golang:latest
RUN mkdir /api 
ADD . /api/ 
WORKDIR /api 
RUN go get -d -v github.com/dgrijalva/jwt-go
RUN go get -d -v github.com/go-sql-driver/mysql
RUN go get -d -v github.com/gorilla/mux
EXPOSE 8082
CMD ["go", "run", "api.go"]