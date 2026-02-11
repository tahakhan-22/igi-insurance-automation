# VS Code Setup Guide for IGI Insurance Automation

This guide helps you set up Visual Studio Code for optimal development experience with the IGI Insurance Automation project.

## 🎨 Recommended VS Code Extensions

Install these extensions for the best development experience:

### Essential
- **Docker** (`ms-azuretools.vscode-docker`) - Manage containers from VS Code
- **Python** (`ms-python.python`) - Python language support
- **Pylance** (`ms-python.vscode-pylance`) - Fast Python language server
- **ESLint** (`dbaeumer.vscode-eslint`) - JavaScript/TypeScript linting
- **Prettier** (`esbenp.prettier-vscode`) - Code formatting

### Helpful
- **GitLens** (`eamodio.gitlens`) - Enhanced Git integration
- **Thunder Client** (`rangav.vscode-thunder-client`) - REST API testing
- **YAML** (`redhat.vscode-yaml`) - YAML language support
- **DotENV** (`mikestead.dotenv`) - .env file syntax highlighting
- **Path Intellisense** (`christian-kohler.path-intellisense`) - File path autocomplete

## ⚙️ VS Code Workspace Settings

Create a `.vscode/settings.json` file in the project root with these settings:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.tabSize": 4
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true
  },
  "files.watcherExclude": {
    "**/.git/objects/**": true,
    "**/node_modules/**": true,
    "**/__pycache__/**": true
  }
}
```

## 🐛 Debug Configuration

Create `.vscode/launch.json` for debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": true,
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

## 📁 Recommended Folder Structure

Open VS Code at the project root:

```bash
cd igi-insurance-automation
code .
```

Your workspace should look like:
```
igi-insurance-automation/
├── .vscode/
│   ├── settings.json
│   └── launch.json
├── backend/
│   └── app/
├── frontend/
│   └── src/
├── .env
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start from VS Code

### 1. Open Integrated Terminal
Press `` Ctrl+` `` (backtick) or `View > Terminal`

### 2. Start Docker Services
In the terminal, run:
```bash
docker compose up --build
```

### 3. Use Docker Extension
- Click the Docker icon in the left sidebar
- View running containers
- Right-click containers to:
  - View logs
  - Attach shell
  - Stop/Start/Restart
  - Open in browser

## 🔍 Using the Terminal

### Split Terminal for Multiple Services
- Backend logs: `docker compose logs -f backend`
- Frontend logs: `docker compose logs -f frontend`
- Database logs: `docker compose logs -f db`

### Run Multiple Terminals
- New terminal: `` Ctrl+Shift+` ``
- Split terminal: `Ctrl+\`

## 🐳 Docker Integration

### View Container Logs
1. Open Docker extension
2. Expand "Containers"
3. Right-click on a container
4. Select "View Logs"

### Attach to Container
1. Right-click on a running container
2. Select "Attach Shell"
3. Run commands inside the container

### Quick Container Actions
- **Start:** Right-click → Start
- **Stop:** Right-click → Stop
- **Restart:** Right-click → Restart
- **Remove:** Right-click → Remove

## 🧪 Testing API Endpoints

### Using Thunder Client Extension
1. Install Thunder Client extension
2. Create a new request
3. Set URL: `http://localhost:8000/api/clients/`
4. Test endpoints directly in VS Code

### Using Rest Client Extension
Create a `test.http` file:
```http
### Health Check
GET http://localhost:8000/health

### List Clients
GET http://localhost:8000/api/clients/

### Create Client
POST http://localhost:8000/api/clients/
Content-Type: application/json

{
  "name": "Test Client",
  "address_type": "Home",
  "address": "123 Test St",
  "country": "Pakistan",
  "city": "Karachi"
}
```

## 🎯 Keyboard Shortcuts

### Essential Shortcuts
- **Command Palette:** `Ctrl+Shift+P` (or `F1`)
- **Quick Open:** `Ctrl+P`
- **Terminal:** `` Ctrl+` ``
- **Git:** `Ctrl+Shift+G`
- **Search:** `Ctrl+Shift+F`
- **Debug:** `F5`
- **Format Document:** `Shift+Alt+F`

### Docker Extension Shortcuts
- **View Docker:** `Ctrl+Shift+D`

## 📝 Code Snippets

Create custom snippets for common patterns:

### Python Snippets
File > Preferences > User Snippets > Python

```json
{
  "FastAPI Router": {
    "prefix": "router",
    "body": [
      "from fastapi import APIRouter, Depends, HTTPException",
      "from sqlalchemy.orm import Session",
      "from app.database import get_db",
      "",
      "router = APIRouter(prefix=\"/api/${1:resource}\", tags=[\"${1:resource}\"])",
      "",
      "@router.get(\"/\")",
      "def list_${1:resource}(db: Session = Depends(get_db)):",
      "    return []"
    ]
  }
}
```

## 🔧 Troubleshooting

### Python Interpreter Not Found
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from `backend/venv/bin/python`

### Import Errors
1. Ensure Python extension is installed
2. Check that PYTHONPATH is set correctly
3. Reload VS Code window: `Ctrl+Shift+P` → "Reload Window"

### Docker Extension Not Working
1. Ensure Docker Desktop is running
2. Restart VS Code
3. Check Docker extension settings

## 💡 Pro Tips

### 1. Use Tasks
Create `.vscode/tasks.json` for common commands:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Docker Services",
      "type": "shell",
      "command": "docker compose up --build",
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

### 2. Git Integration
- View changes: `Ctrl+Shift+G`
- Stage files: Click `+` next to file
- Commit: Type message and `Ctrl+Enter`
- Push: Click `...` → Push

### 3. Multi-Cursor Editing
- Add cursor: `Alt+Click`
- Add next occurrence: `Ctrl+D`
- Select all occurrences: `Ctrl+Shift+L`

### 4. Quick File Navigation
- Go to file: `Ctrl+P`
- Go to symbol: `Ctrl+Shift+O`
- Go to definition: `F12`
- Peek definition: `Alt+F12`

## 📚 Additional Resources

- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Docker Tutorial](https://code.visualstudio.com/docs/containers/overview)
- [VS Code Keyboard Shortcuts](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)

## 🆘 Getting Help

If something doesn't work:
1. Reload VS Code window: `Ctrl+Shift+P` → "Reload Window"
2. Check extension logs: Output panel → Select extension
3. Restart VS Code
4. Restart Docker Desktop

---

**Happy Coding! 🚀**

For general setup instructions, see [GETTING_STARTED.md](GETTING_STARTED.md)
