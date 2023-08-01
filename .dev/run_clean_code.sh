#!/bin/bash

black --line-length=119 .
isort --profile=black .
