package main

import (
   "fmt"
   "net/http"
    "time"
)
var pong = make(chan int)

func ping(w http.ResponseWriter, req *http.Request,){
    fmt.Fprintf(w,"pong")
    pong <- 1
}

func main() {
    fmt.Println("you can ping at http://localhost:8090/ping")
    http.HandleFunc("/ping",ping)
    go func(){
    for range pong {
        fmt.Println("pong",time.Now())
        }
    }()
    http.ListenAndServe(":8090", nil)
}
