#!/bin/bash

pyinstaller cli.py --name FromNothing --onefile --exclude-module=unittest
