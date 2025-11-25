#!/bin/bash

APP_NAME="VoxCode"
APP_DIR="$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

# Clean previous build
rm -rf "$APP_DIR"

# Create directories
mkdir -p "$MACOS_DIR"
mkdir -p "$RESOURCES_DIR"

# Compile Swift files
echo "Compiling Swift files..."
swiftc ui/swift/VoxCodeApp.swift \
       ui/swift/ContentView.swift \
       ui/swift/Bridge.swift \
       -o build/VoxCode.app/Contents/MacOS/VoxCode \
       -target x86_64-apple-macosx13.0 \
       -framework SwiftUI \
       -framework Foundation \
       -framework Combine \
       -framework AppKit

# Copy Info.plist
echo "Copying Info.plist..."
cp ui/swift/Info.plist build/VoxCode.app/Contents/Info.plist

# Ad-hoc signing (required for local execution on ARM Macs, good practice on Intel)
echo "Signing app..."
codesign --force --deep --sign - build/VoxCode.app

echo "Build complete: build/VoxCode.app"
