#!/bin/bash

echo "Sending to heroku..."

git push heroku master

echo "Sending to amazon"

git push amazon master