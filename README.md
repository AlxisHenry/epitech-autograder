# Epitech autograder notifications 🐡

This is a discord bot that sends a message to a channel when a new auto-grading is available on the intranet. 

> The bot knows when a new auto-grading is available by checking the grades page every 5 minutes using a python script.

## Table of contents
1. [How to use it ?](#how-to-use-it-)
2. [Technologies](#technologies)
3. [Authors](#authors)

## How to use it ?

First, you need to clone the repository.

```bash
$ git clone https://github.com/AlxisHenry/epitech-autograder.git
$ cd epitech-autograder
```

### Install javascript dependencies

```
$ npm install
```

### Configure the discord bot

```bash
cp config.sample.json config.json
```

Put your discord bot token in the `config.json` file.

```bash
$ cat config.json
{
	"token": "<your token here>"
}
```

### Configure the python script

```bash
cd bot
cp .env.example .env
cp autograder.sample.json autograder.json
```

#### Update the `.env` file with your own values

```bash
$ cat .env
BROWSER="edge"
DRIVER_PATH="./drivers/msedgedriver.exe"
PROFILE_PATH="C:\\Users\\user\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
WEBSITE_URL="https://www.google.com"
```

#### Optionally you can use a python virtual environment to run the bot

```bash
$ python3 -m venv venv
$ venv/Scripts/activate
```

#### Install the needed packages

```bash
$ pip install -r requirements.txt
```

### Everything is done :tada:

You can now run the bot.

```bash
$ cd ..
$ node index.js
```

## Technologies

![](https://img.shields.io/badge/javascript-%2320232a.svg?style=for-the-badge&logo=javascript&color=20232a)
![](https://img.shields.io/badge/python-%2320232a.svg?style=for-the-badge&logo=python&color=20232a)

## Authors

- [@AlxisHenry](https://github.com/AlxisHenry)
