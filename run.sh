#!/bin/bash
python3 model/train.py
nohup python3 honeypot/ssh_fake.py &
flask --app app/app.py run --host=0.0.0.0 --port=9900
