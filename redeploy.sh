#!/bin/bash
docker stop wl-twitter-bot && docker rm wl-twitter-bot
docker build -t wl-twitter-bot . && docker run -d -p 7999:8000 --name wl-twitter-bot --network gem wl-twitter-bot