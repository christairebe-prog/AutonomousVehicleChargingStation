# Autonomous Vehicle Charging Station - Git Setup

## Initial Git Setup

Follow these steps to initialize Git version control for this project:

### 1. Initialize Git Repository
```powershell
cd C:\AutonomousVehicleChargingStation
git init
```

### 2. Configure Git (if not already done)
```powershell
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 3. Add All Files to Git
```powershell
git add .
```

### 4. Create Initial Commit
```powershell
git commit -m "Initial commit: Autonomous Vehicle Charging Station Management System

- Implemented Observer Pattern for real-time notifications
- Created models: Vehicle, ChargingSlot, ChargingStation
- Implemented services: QueueManager, BillingService, NotificationService, ReservationService
- Added comprehensive unit tests with pytest
- Created UML diagrams (Use Case, Class, Activity, Sequence)
- Dockerized application for easy deployment
- Followed PEP 8 coding standards"
```

### 5. Create GitHub Repository

#### Option A: Using GitHub CLI (if installed)
```powershell
gh repo create AutonomousVehicleChargingStation --public --source=. --remote=origin
git push -u origin main
```

#### Option B: Using GitHub Web Interface
1. Go to https://github.com/new
2. Create a new repository named "AutonomousVehicleChargingStation"
3. Do NOT initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL
5. Add remote and push:

```powershell
git remote add origin https://github.com/yourusername/AutonomousVehicleChargingStation.git
git branch -M main
git push -u origin main
```

### 6. Create Development Branch
```powershell
git checkout -b develop
git push -u origin develop
```

## Git Workflow

### Feature Branch Workflow

1. **Create a feature branch:**
```powershell
git checkout develop
git pull origin develop
git checkout -b feature/new-feature-name
```

2. **Make changes and commit:**
```powershell
git add .
git commit -m "feat: description of feature"
```

3. **Push feature branch:**
```powershell
git push -u origin feature/new-feature-name
```

4. **Create Pull Request on GitHub**

5. **Merge to develop, then to main**

## Conventional Commits

Use these commit message prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting)
- `chore:` - Maintenance tasks

### Examples:
```
feat: add reservation cancellation feature
fix: correct priority queue ordering
docs: update README with Docker instructions
test: add tests for billing service
refactor: improve queue manager performance
```

## Useful Git Commands

### Check status
```powershell
git status
```

### View commit history
```powershell
git log --oneline --graph --decorate --all
```

### Create and switch to branch
```powershell
git checkout -b branch-name
```

### Switch branches
```powershell
git checkout branch-name
```

### Pull latest changes
```powershell
git pull origin main
```

### View differences
```powershell
git diff
```

### View remote repositories
```powershell
git remote -v
```

## Branch Protection Rules (Recommended)

On GitHub, set up branch protection for `main`:
1. Go to repository Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging

## .gitignore

The project includes a `.gitignore` file that excludes:
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Test coverage reports
- OS-specific files

## Tags for Releases

Create tags for version releases:
```powershell
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Collaboration Tips

1. **Always pull before starting work:**
```powershell
git pull origin main
```

2. **Commit frequently with meaningful messages**

3. **Keep commits focused** - one logical change per commit

4. **Review changes before committing:**
```powershell
git diff
```

5. **Use branches** - never commit directly to main

## Troubleshooting

### Undo last commit (keep changes)
```powershell
git reset --soft HEAD~1
```

### Discard changes in working directory
```powershell
git checkout -- filename
```

### View remote URL
```powershell
git remote get-url origin
```

### Change remote URL
```powershell
git remote set-url origin https://github.com/yourusername/AutonomousVehicleChargingStation.git
```

---

**Note:** Make sure you have Git installed on your system. Download from: https://git-scm.com/downloads
