#!/bin/bash

# Default values
REGION=""
COST=""
AGE=""
CSV_FILE="attractions.csv"
LOG_FILE="lottery.log"

# Function to show usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo "  -r, --region CITY      Filter by Region (e.g., 台北, 新北, 桃園...)"
    echo "  -c, --cost TYPE        Filter by Cost (e.g., 免費, 門票, 內部消費)"
    echo "  -a, --age GROUP        Filter by Age Group (e.g., 小孩, 都適合)"
    echo "  -h, --help             Show this help message"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--region) REGION="$2"; shift ;;
        -c|--cost) COST="$2"; shift ;;
        -a|--age) AGE="$2"; shift ;;
        -h|--help) usage ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

# Check if CSV exists
if [[ ! -f "$CSV_FILE" ]]; then
    echo "Error: $CSV_FILE not found!"
    exit 1
fi

# Filter logic
# Columns: Name, Type, City, Cost, Age, Map, Reference
# awk -F, '$3 ~ /Region/ && $4 ~ /Cost/ && $5 ~ /Age/'
# We use partial matching or exact matching? Let's use partial for flexibility but check specific columns.

FILTERED=$(tail -n +2 "$CSV_FILE" | awk -F, -v region="$REGION" -v cost="$COST" -v age="$AGE" '
    BEGIN { COUNT=0 }
    {
        if (($3 ~ region) && ($4 ~ cost) && ($5 ~ age)) {
            print $0
            COUNT++
        }
    }
')

if [[ -z "$FILTERED" ]]; then
    echo "No attractions found matching criteria."
    exit 0
fi

# Select one randomly
# We can use shuf if available, or sort -R
SELECTED=$(echo "$FILTERED" | shuf -n 1)

# Extract details
NAME=$(echo "$SELECTED" | cut -d, -f1)
TYPE=$(echo "$SELECTED" | cut -d, -f2)
CITY_VAL=$(echo "$SELECTED" | cut -d, -f3)
COST_VAL=$(echo "$SELECTED" | cut -d, -f4)
AGE_VAL=$(echo "$SELECTED" | cut -d, -f5)
MAP_LINK=$(echo "$SELECTED" | cut -d, -f6)

# Output result
echo "🎉 Congratulations! Your destination is:"
echo "========================================"
echo "📍 Name: $NAME"
echo "🏙️  City: $CITY_VAL"
echo "🏷️  Type: $TYPE"
echo "💰 Cost: $COST_VAL"
echo "👥 Age: $AGE_VAL"
echo "🗺️  Map: $MAP_LINK"
echo "========================================"

# Log result
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Timestamp,Name,City,Cost,Age" > "$LOG_FILE"
fi
echo "$TIMESTAMP,$NAME,$CITY_VAL,$COST_VAL,$AGE_VAL" >> "$LOG_FILE"
