package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

var (
	buffer chan string
	file   string
)

const (
	api = "http://codeforces.com/api/user."
)

func sh(c string) {
	cmd := exec.Command("sh", "-c", c)
	cmd.Run()	
}

func Read(req, method string, fileName string) {
	url := api + method + "?"
	url += req
	sCmd := fmt.Sprintf("curl %s > %s", url, fileName)
	sh(sCmd)

}

func Reader() {
	for {
		user := <-buffer
		log.Println("curling ", user, "...")
		Read("handle=" + user, "rating", "user_rating/" + user + ".rating.json")
		Read("handle=" + user, "status", "user_submition/" + user + ".submition.json")
		Read("handles=" + user, "info", "user_info/" + user + ".info.json")
		//Read(user, "friends", "user_friends/" + user + ".friends.json")

		sCmd := fmt.Sprintf("echo '%s' >> readed.csv", user)
		sh(sCmd)
	}
}

func main() {
	fmt.Println("Press enter to stop...")
	sh("touch readed.csv")

	mc := os.Getenv("MACHINE_COUNT")
	MACHINE_COUNT, err := strconv.Atoi(mc)
	if err != nil {
		log.Fatalln("Plz enter correct MACHINE_COUNT.")
	}

	if len(os.Args) != 2 {
		log.Fatalln("Plz enter file name.")
	}
	file = os.Args[1]

	buffer = make(chan string, MACHINE_COUNT)

	for i := 0; i < MACHINE_COUNT; i += 1 {
		go Reader()
	}

	go func() {
			if dat, err := ioutil.ReadFile("readed.csv"); err == nil {
			rUsers := strings.Split(string(dat), "\n")
			if dat, err := ioutil.ReadFile(file); err == nil {
				users := strings.Split(string(dat), "\n")
				for _, u := range users {
					flag := false
					for _, u2 := range rUsers {
						if u2 == u {
							flag = true
							break
						}
					}
					if(flag) {
						continue
					}
					buffer <- u
				}
			} else {
				panic(err)
			}
		} else {
			panic(err)
		}
	}()

	fmt.Scanln()
}
