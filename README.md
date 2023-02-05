# 2023_MrSpeed

### macOS Setup Pre-requisites:
1. Download and install [Python 3.11](https://python.org/downloads/)
2. Install pipenv:
	1. `pip3 install pipenv`
	2. sudo alternative ## Not recommended unless pipenv fails to install without it
3. Clone the [2023_MrSpeed](https://github.com/Angelbots1339/2023_MrSpeed) repository
	1. GitHub CLI - `gh repo clone Angelbots1339/2023_MrSpeed` ## Recommended
	2. HTTPS - `https://github.com/Angelbots1339/2023_MrSpeed.git`
	3. SSH - `git@github.com:Angelbots1339/2023_MrSpeed.git`
4. `cd 2023_MrSpeed`
5. `pipenv install --ignore-pipfile`

### Rio First Time Setup
1. `cd rioSetup`
2. `./rioSetup.sh [Radio SSID]`
[![demo](https://asciinema.org/a/557437.svg)](https://asciinema.org/a/557437?autoplay=1)

### Branching Strategy (main is a protected branch)
1. `git checkout -b [YourName_BranchTitle]`
2. `git checkout [YourName_BranchTitle]`
3. Iterate through your code changes and validate functionality in the simulator before proceeding
4. `git add .`
5. `git commit -m "Your _detailed_ commit message"`
6. `git push origin [YourName_BranchTitle]`
7. Create a pull request
	```gh pr create` ## Requires installation of `gh` Github's command line utility```
	or
	From the github.com branch page, follow the instructions to submit your pull request into 'main'
8. Ask one of your peers to review your pull request and merge if they approve

### Post-Merge repository syncronization
1. `git checkout main`
2. `git fetch origin`
3. `git merge origin/main`
4. `git branch -d [YourName_BranchTitle]`

### Deploy your code to the rio
1. `cd deploy`
2. `python3 robot.py deploy`
[![demo](https://asciinema.org/a/557439.svg)](https://asciinema.org/a/557439?autoplay=1)
