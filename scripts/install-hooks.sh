#!/usr/bin/env sh

GIT_DIR=$(git rev-parse --git-dir)

echo "Installing hooks..."
# this command creates symlink to our pre-push.sh script
ln -sf ../../scripts/pre-push.sh $GIT_DIR/hooks/pre-push
echo "Done!"