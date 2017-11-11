#!/usr/bin/env bash

echo "Updating Remotes..."
#git remote
git pull origin # Pull origin to stay up to date

PHR="Release Alpha v"
NUM1=6 # Set new main version number here
NUM2=0 # And set version minor number here

TMP=$[NUM2-1]


echo ""
echo "Changing to"
echo $NUM1.$NUM2
echo "from"
echo $NUM1.$TMP
echo ""

VER=$NUM1.$NUM2
MSG=$PHR$VER

#sed -e "206s/$NUM1.$TMP/$NUM1.$NUM2/" templates/index.html # Update the new version num
#mv templates/index_tmp.html templates/index.html

echo $MSG
git commit --all --message "$MSG" # Commit all the changed code

git push origin # Update bitbucket
git push heroku # Update heroku
git push git # Update git

#git push AAmazon # Update amazon server (legacy)
#git push AHeroku # Update amazon / heroku sever  (legacy)