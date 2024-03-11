# GitHub Workflow

## Master Branch
- Purpose: Fully functional and tested functionalities are merged into this branch.
- Merge Policy: Only merge in fully tested and functional code from the development branch.
- Hotfix Branches: If there's an urgent fix needed in master, create a hotfix branch from master. Pull requests must be submitted and reviewed before merging hotfix branches into master.

## Development Branch
- Purpose: Merge your individual functionalities into this branch.
- Merge Policy: Merge your individual features and fixes into this branch before they are integrated into the master branch. Pull requests must be submitted and reviewed before merging into development.

## Hotfix Branches
- Purpose: Address urgent issues in the production codebase.
- Merge Policy: Pull requests must be submitted and reviewed before merging hotfix branches directly into the master branch once the issue is resolved.

## Feature Branches
- Purpose: Develop specific features in isolation from the main codebase.
- Merge Policy: Merge feature branches into the development branch once the feature is complete and tested. Pull requests must be submitted and reviewed before merging into development.

## Improvement Branches
- Purpose: Implement enhancements or optimizations to the existing codebase that can't be categorized under any other type of branch.
- Merge Policy: Merge improvement branches into the development branch once the enhancements are complete and tested. Pull requests must be submitted and reviewed before merging into development.

# Pull Requests

1. When your functionality/improvement/hotfix etc. is finished and you pushed it to your remote branch, you can put up a PR (pull request) to merge it into the branch you based it on.
2. Add every other team member as a reviewer.
3. Add the type of what your branch is in the title (e.g., hotfix, feature, improvement).
4. The PR needs to be approved by at least one person.
5. When it is approved, do Squash and Merge (this way any bugs that may occur can be easily reversed).
6. Delete the branch in the PR (There is a button on the bottom of the page of the PR after you've merged it)