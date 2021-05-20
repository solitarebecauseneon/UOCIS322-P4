#!/bin/bash

for t in nTests/*.py
do
    nosetests $t
done
