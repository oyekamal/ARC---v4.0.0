

```bash

1. sudo apt-get install mosquitto mosquitto-clients
2. sudo systemctl start mosquitto

3. python -m venv venv # one time only for creating the environment
4. source venv/bin/activate


5. pip install -r requirements.txt
6. 
  flask db init
  flask db migrate
  flask db upgrade

7. python run.py

```

<br />
when the master is running. open another terminal and run activate the environment using.


```bash
1. source venv/bin/activate
2. python flask_subscribe.py
```
<br />

> How to update db

```bash
flask db init
flask db migrate
flask db upgrade
```
