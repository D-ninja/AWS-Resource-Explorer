#!/bin/bash
echo " █████  █████  █████████      █████████  ███████████   ██████████    ███████████                                   "
echo "░░███  ░░███  ███░░░░░███    ███░░░░░███░░███░░░░░███ ░░███░░░░░█   ░█░░░███░░░█                                   "
echo " ░███   ░███ ░███    ░░░    ░███    ░░░  ░███    ░███  ░███  █ ░    ░   ░███  ░   ██████   ██████   █████████████  "
echo " ░███   ░███ ░░█████████    ░░█████████  ░██████████   ░██████          ░███     ███░░███ ░░░░░███ ░░███░░███░░███ "
echo " ░███   ░███  ░░░░░░░░███    ░░░░░░░░███ ░███░░░░░███  ░███░░█          ░███    ░███████   ███████  ░███ ░███ ░███ "
echo " ░███   ░███  ███    ░███    ███    ░███ ░███    ░███  ░███ ░   █       ░███    ░███░░░   ███░░███  ░███ ░███ ░███ "
echo " ░░████████  ░░█████████    ░░█████████  █████   █████ ██████████       █████   ░░██████ ░░████████ █████░███ █████"
echo "  ░░░░░░░░    ░░░░░░░░░      ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░░░░░░       ░░░░░     ░░░░░░   ░░░░░░░░ ░░░░░ ░░░ ░░░░░ "
echo "                                "

regions=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "eu-west-1" "eu-west-2")

# Check if pandas is installed
if ! python3 -c "import pandas" &> /dev/null; then
    pip install pandas &> /dev/null
fi
# Check if openpyxl is installed
if ! python3 -c "import openpyxl" &> /dev/null; then
    pip install openpyxl &> /dev/null
fi

echo "Finding Global Resources"
python3 global.py
for region in "${regions[@]}"
do
    echo "Executing in $region..." 
    export AWS_DEFAULT_REGION=$region
    python3 regional.py
    echo "Resources information has been appended to 'aws_resources.xlsx' successfully for $region"
done