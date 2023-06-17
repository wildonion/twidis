#!/bin/bash
docker stop twidis && docker rm twidis
docker build -t twidis . && docker run -d -p 7999:8000 --name twidis --network gem twidis