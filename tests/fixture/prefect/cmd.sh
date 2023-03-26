# check the version of prefect server and choose if it use prefect server or prefect orion
# prefect orion is used before version 2.8
if prefect | grep -q server; then
    prefect server start
else
    prefect orion start
fi
