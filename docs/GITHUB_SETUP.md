# Publish Project Nightfall to GitHub

These commands create a remote only when a student chooses to do so. This project has not been initialised with a remote and does not push automatically.

## 1. Review the files

From the project directory:

```shell
git status
git diff --check
```

If Git is not already initialised and you want to publish this folder:

```shell
git init
git add .
git status
git commit -m "Build Project Nightfall investigation lab"
```

Suggested repository description: **A synthetic, offline-capable Streamlit workshop for evidence-led threat hunting and MITRE ATT&CK Enterprise v15.1 mapping.**

## 2. Create an empty GitHub repository

On GitHub, create a repository named `project-nightfall-attack-investigation`. Do not add a README, license, or .gitignore during repository creation because those files already exist here.

## 3. Add the remote and publish

Replace `YOUR-USERNAME` with your GitHub username. Use the HTTPS or SSH URL shown by GitHub:

```shell
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/project-nightfall-attack-investigation.git
git push -u origin main
```

GitHub authentication is handled by the user's normal Git credential manager or SSH setup. Never put tokens or credentials in `.env`, source code, or a command saved in a shared file.

## 4. Subsequent updates

```shell
git add .
git commit -m "Describe the investigation lab update"
git push
```

Review `git status` before every commit. The `.gitignore` excludes virtual environments, local environment files, caches, logs, and generated outputs. The published sample case and catalogue are synthetic or version-pinned public metadata.
