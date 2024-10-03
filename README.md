# Ping Pong GUI Project

# Git Workflow
In order for us to collaborate using GIT, we will use a simple workflow as
defined below. 

## One-Time Setup
Before working on the project, it must be cloned to your local device first:

### Instructions on Cloning the Project
After being added to the private repository, please follow the following
instructions to clone it locally. 

1. Navigate to where you would like to clone the project on your device.
2. Open a terminal in that directory
3. Run the command `git clone https://github.com/Jason1867/PingPongGUI.git`

## Subsequent Commits
A commit is the basic unit of change in GIT. It is a snapshot of the project
at a given point in time. Each time you make a change to the project, you
must create a new commit, and push it to the main branch. A basic workflow
is as follows:

1. Ensure you are on the main branch by running `git checkout main`
2. Pull the latest changes from the remote repository by running
    `git reset --hard origin/main`. This will remove any local changes you have
    made, and replace them with the latest changes from the remote repository. 
    Therefore, make sure that you do not have any changes that you want to keep
    before running this command.
3. Create a new branch for your changes by running
    `git checkout -b <branch-name>`. Replace `<branch-name>` with a name that
    includes your name and a short description of the changes you are making.
    For example, my name is Naji K. so I would call my branch
    `najik-implemented-login-page`.
4. Make your changes to the project.
5. Add your changes to the staging area by running `git add .`
6. Create a commit of your changes by running `git commit -m "<commit-message>"`
    Replace `<commit-message>` with a short description of the changes you made.
    For example, if I implemented the login page, I would run
    `git commit -m "Implemented login page"`.
7. While you were working on your changes, other people may have pushed changes
    to the remote repository. Therefore, you must pull the latest changes from
    the remote repository by running `git pull --rebase origin main`. This will
    merge the latest changes from the remote repository into your branch. If
    there are any merge conflicts, you will have to resolve them manually.
8. Push your changes to the remote repository by running
    `git push --set-upstream remote <branch>`. Replace `<branch>` with the name
    of the branch you created in step 3. For example, I would run
    `git push --set-upstream remote najik-implemented-login-page`. The 
    `--set-upstream` flag is only required the first time you push a branch to
    the remote repository. After that, you can simply run `git push origin`.
9. Go to the GitHub page for the repository, and create a pull request for your
    branch. This will allow other people to review your changes before they are
    merged into the main branch.
10. If there are any changes requested, make them, and push them to the remote
    repository. This will automatically update the pull request.
11. Once your pull request has been approved, you can merge it into the main
    branch. To do this, go to the GitHub page for the repository, and click
    "Merge pull request". Then, click "Confirm merge". This will merge your
    changes into the main branch.

Please be careful when running the commands above, as it is possible to lose
your work if you are not careful. Even worse, you could accidentally corrupt
someone else's work. If you are unsure about anything, please contact me and
I will be happy to help.


# Project Structure
- `pingPong.py`: contains all the source code. 
- `README.md`: this file.
