#!/bin/bash

# URL of the ESP32 metrics endpoint
URL="http://<esp32IP>/metrics"

# Check if a metric argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <metric>"
  echo "Available metrics: cpuLoad, heapFree, storageTotal, storageUsed"
  exit 3
fi

# Get the JSON metrics
json=$(curl -s "$URL")
if [ -z "$json" ]; then
  echo "UNKNOWN - Unable to fetch metrics |"
  exit 3
fi

# Extract JSON fields using jq
cpuLoad=$(echo "$json" | jq -r '.cpuLoad')
heapFree=$(echo "$json" | jq -r '.heapFree')
storageTotal=$(echo "$json" | jq -r '.storageTotal')
storageUsed=$(echo "$json" | jq -r '.storageUsed')

# Check which metric the user requested
case "$1" in
  cpuLoad)
    echo "OK - CPU Load: $cpuLoad | cpuLoad=$cpuLoad;;;;"
    exit 0
    ;;
  heapFree)
    echo "OK - Heap Free: $heapFree | heapFree=$heapFree;;;;"
    exit 0
    ;;
  storageTotal)
    echo "OK - Storage Total: $storageTotal | storageTotal=$storageTotal;;;;"
    exit 0
    ;;
  storageUsed)
    echo "OK - Storage Used: $storageUsed | storageUsed=$storageUsed;;;;"
    exit 0
    ;;
  *)
    echo "UNKNOWN - Unknown option: $1"
    echo "Available metrics: cpuLoad, heapFree, storageTotal, storageUsed"
    exit 3
    ;;
esac
