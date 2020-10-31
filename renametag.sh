#!/usr/bin/env bash
# Author: Raúl Novelo https://github.com/rnovec
git tag v1.0.0-beta v1.0.0-alpha.3
git tag -d v1.0.0-alpha.3
git push origin --tags
git push origin :refs/tags/v1.0.0-alpha.3
git tag -l

