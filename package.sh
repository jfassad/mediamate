#!/bin/bash

cd "`dirname \"$0\"`"
PROJECT_DIR="`pwd`"
ARCHIVE_NAME="app.tar.gz"
PACKAGE_DIR="target"

# Change to the project directory
cd "${PROJECT_DIR}"

# Create package directory if it doesn't exist
mkdir -p "${PACKAGE_DIR}"

pip freeze > requirements.txt

# Create the compressed archive, excluding .idea, venv, and package directories
cp .gitignore .tarignore
sed -i '/\/$/s/\/$//' .tarignore
tar -czvf "${PROJECT_DIR}/${PACKAGE_DIR}/${ARCHIVE_NAME}" --exclude='package.sh' --exclude='.tarignore' --exclude='.gitignore' --exclude='.git' --exclude='tmp' --exclude-from="${PROJECT_DIR}/.tarignore" --directory="${PROJECT_DIR}" .
rm .tarignore

