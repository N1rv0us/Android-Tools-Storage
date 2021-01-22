#!/usr/bin/env bash
gradle jar
# replace dx path with your own path
/Users/listennter/Library/Android/sdk/build-tools/27.0.3/dx  --dex --output Main.jar ./build/libs/java-1.0.jar