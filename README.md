# NiMi-trading-bot

[![Build Status](https://travis-ci.com/proSingularity/NiMi-trading-bot.svg?branch=master)](https://travis-ci.com/proSingularity/NiMi-trading-bot) [![codecov](https://codecov.io/gh/proSingularity/NiMi-trading-bot/branch/master/graph/badge.svg)](https://codecov.io/gh/proSingularity/NiMi-trading-bot)

## Dev setup

From project root run in order
```shell
pip3 install virtualenv
cd env/Scripts
activate`
// on win7 with Eclipse the current directory is now shown as "(env) E:\git-repositories\NiMi-trading-bot\env\Scripts>"
cd ../..
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
// Inside Eclipse set your python interpreter to the "python.exe" in your "env" directory
```

## Useful commands

Run type checker for all files in `src` (see [mypy doc](https://mypy.readthedocs.io/en/latest/command_line.html))
`mypy src`