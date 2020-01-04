#!/bin/bash

JAVA8_EXEC="${HOME}/opt/java8/bin/java"
RUNDECK_WAR_PATH="${HOME}/opt/rundeck/rundeck.war"

$JAVA8_EXEC -jar $RUNDECK_WAR_PATH
