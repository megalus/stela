#!/bin/bash

# Inspect Unreleased Changelog
UNRELEASE_DATA=$(auto-changelog -u --stdout)
has_features=false
breaking_changes=false

if [[ $(echo ${UNRELEASE_DATA} | grep "#### New Features") == "" ]]
then
	has_features=true
fi
if [[ $(echo ${UNRELEASE_DATA} | grep "BREAKING") == "" ]]
then
	breaking_changes=true
fi

# Determine Version level
if [[ ${breaking_changes} == true ]]
then
	version_level="major"
elif [[ ${has_features} == true ]]
then
	version_level="minor"
else
	version_level="patch"
fi

# Determine Bump Rule
current_branch=$(git branch | grep -o -P "(?<=\* )\S+")
if [[ ${current_branch} == "master" ]]
then
	version_rule=${version_level}
else
	version_rule="pre${version_level}"
fi

PACKAGE_VERSION=$(poetry version | grep -o -P "(?<=stela )\S+")
echo "Current version: ${PACKAGE_VERSION}"
echo "Bump rule: ${version_rule}"

# Update Version
poetry version ${version_rule}

# Update Changelog
PACKAGE_NEW_VERSION=$(poetry version | grep -o -P "(?<=stela )\S+")
echo "New version: ${PACKAGE_NEW_VERSION}"
auto-changelog -v ${PACKAGE_NEW_VERSION}

# Commit alterations
echo "Commiting alterations..."
git add CHANGELOG.md
git add pyproject.toml
git commit -m "Auto-bump version ${PACKAGE_NEW_VERSION}"
git tag ${PACKAGE_NEW_VERSION}
git push

# Back Merge to develop if master
if [[ ${current_branch} == "master" ]]
then
	echo "Back merging alterations..."
	git reset --hard HEAD
	git checkout develop
	git merge origin/master
	git push
fi
