# python-flask-api-simple

Simple mock-up for python flask rest api


This mock-up includes these features

* RDB Connection with PooledDB
* Poetry package control
* devcontainer for team
* vscode debugger setting for team


※ Warning ※

* If there's some connection issue with mysql, wait for a minute. Maybe your mysql container is in loading status.


## how to run 
### 1) When you run this in local test environment

1. run vscode
2. install extension - devcontainer
3. F1 → Dev Containers: Rebuild and Reopen in Container
4. run vscode debugger (left menu - Run & Debug → Python Debugger: Flask)

### 2) As a docker container

Just copy and paste this command in your command line

```
bash ./build/build.sh
bash ./build/start_run.sh
```
