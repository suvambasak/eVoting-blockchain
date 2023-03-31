# SC5-eVoting-G10

## install dependencies 
Install dependencies from `requirements.txt`
```bash
pip install -r requirements.txt
```

## Start application
1. Export app name
```bash
export FLASK_APP=dapp
```
2. Set debugging mode
```bash
export FLASK_DEBUG=1 
```
3. Start app </br>

For localhost
```bash
flask run
```
For LAN
```bash
flask run --host=0.0.0.0
```