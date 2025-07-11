#!/bin/bash

IMAGE_NAME="expdespy-tests"

echo "Building Docker image..."
if ! docker build -t $IMAGE_NAME .; then
  echo "Docker build failed!"
  exit 1
fi

echo "Running tests with coverage inside Docker container..."
if ! docker run --rm $IMAGE_NAME; then
  echo "Tests failed or coverage less than 90%."
  exit 1
fi

echo "All tests passed with coverage >= 90%."