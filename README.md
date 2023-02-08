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
Starting from the `main` branch...
1. `git checkout -b [YourName_BranchTitle]`
2. Iterate through your code changes and validate functionality in the simulator before proceeding
3. `git add .`
4. `git commit -m "Your _detailed_ commit message"`
5. `git push origin [YourName_BranchTitle]`
6. Create a pull request
	```gh pr create` ## Requires installation of `gh` Github's command line utility```
	or
	From the github.com branch page, follow the instructions to submit your pull request into 'main'
8. Ask one of your peers to review your pull request and merge after they approve

### Review Pull Requests
1. `gh pr list`
2. `gh pr checkout [pull request number]`
3. Review the code
4. Approve _or_ Request Changes:
	1. `gh pr review --approve`
	2. `gh pr review [pull request number] --request-changes -b "[your reason for requesting changes]"`

### Merge Pull Request
1. `gh pr merge [pull request number]`

### Post-Merge branch cleanup
1. `git checkout main`
2. `git pull`
4. `git branch -d [YourName_BranchTitle]`

### Deploy your code to the rio
1. `cd src`
2. `python3 robot.py deploy`
[![demo](https://asciinema.org/a/557439.svg)](https://asciinema.org/a/557439?autoplay=1)
