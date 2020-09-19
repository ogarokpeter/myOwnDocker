# myOwnDocker

## Description

Python 3 implementation of Docker for Linux. Doesn't support all Docker commands. Based on many ideas.

Program was implemented as a task in my university. The description of the task (in Russian) can be found in the fils task_statement.pdf.

The project was originally assembled for Gitlab, so Gitlab CI files are present.

## How to run

Just run 

```
$ python3 my_own_docker.py
```

with nessessary CLI arguments. The list of all arguments and a quick help can be reached by running

```
$ python3 my_own_docker.py --help
```
It is a good idea not to run this on your OS but to use Vagrant for virtualization. For your convenience, a Vagrantfile is provided.
