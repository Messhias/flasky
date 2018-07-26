#!/bin/bash

clear

source venv/bin/activate

flask db upgrade

flask test

flask run
