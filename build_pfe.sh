#!/usr/bin/env sh

# Enable strict error handling
set -e

# Get the version
PFE_VERSION="1.0.0"

# Variables for the source and build
SOURCE_DIRECTORY="pfe_src"
BUILD_DIRECTORY="pfe-${PFE_VERSION}-osx"
APP_DIRECTORY="${BUILD_DIRECTORY}/lib/app"
ARCHIVE_NAME="${BUILD_DIRECTORY}.tar.gz"

# Start in the directory where this script is located
BUILD_SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILD_SCRIPT_NAME="$(basename ${BASH_SOURCE[0]})"

cd "${BUILD_SCRIPT_PATH}"

# Ensure we have the source directory
if [ ! -d "${SOURCE_DIRECTORY}" ]; then
	echo "${SOURCE_DIRECTORY} directory not found. Be sure to place {$BUILD_SCRIPT_NAME} in the pfe base directory alongside ${SOURCE_DIRECTORY}"
	exit 1
fi

# Ensure we have the archive
if [ ! -f "${ARCHIVE_NAME}" ]; then
	echo "${ARCHIVE_NAME} not found. Be sure to place {$BUILD_SCRIPT_NAME} in the pfe base directory alongside ${ARCHIVE_NAME}"
	exit 1
fi

# Preserve the source
echo "Preserving the source..."
rm -rf "${SOURCE_DIRECTORY}"/*
cp -R "${APP_DIRECTORY}"/* "${SOURCE_DIRECTORY}"/

# Build new archive
echo "Building new archive..."
tar zcf "${ARCHIVE_NAME}" "${BUILD_DIRECTORY}"

# Finish up
echo "Build complete!"

exit 0