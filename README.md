# ldscript_test

## install and run webserver
pip3 install -r requirements.txt

export FLASK_APP=simple_server.py

python -m flask run 

## install and run corese
git clone git@github.com:Wimmics/corese.git
cd corese/
mvn -Dmaven.test.skip=true package
java -jar corese-server/target/corese-server-4.1.1-jar-with-dependencies.jar -lf

note: -lf activates support for linked functions

## access GUI of robot arm
http://127.0.0.1:5000/robotarmthing

By right clicking into the website and selecting 'inspect element', then navigate in the dev panel to the 'Console' view, you should see the output from Corese. The request is sent from within the html file robotArmThing.html
