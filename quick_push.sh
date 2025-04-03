#!/bin/sh
# Quick push function to GitHub.
echo "Push comment: "
read PUSH_COMMENT
git add .
git commit -m "$PUSH_COMMENT"
git push
