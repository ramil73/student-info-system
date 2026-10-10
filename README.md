# Student Information System

A cloud-ready, console-based Student Information System written in Python.
Student records are stored in JSON, with modular code, external configuration,
logging, validation and error handling.

## Features
- **CRUD**: add, view, update and delete students
- **JSON storage** with atomic writes (no half-written files)
- **Search** by ID, name, course or email
- **CSV export**
- **Data validation** (email format, age range, required fields)
- **Error recovery**: a corrupted data file is backed up and the app restarts cleanly
- **Logging** to `logs/app.log`
- **Unit tests** (`unittest`)

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py            # Student dataclass
│   ├── services/student_service.py  # CRUD, search, export, persistence
│   ├── utils/                       # config, logger, validators, exceptions
│   └── main.py                      # Console menu
├── data/students.json               # Data store
├── config/config.json               # Settings
├── logs/                            # Log output
├── tests/                           # Unit tests
├── requirements.txt
└── .gitignore
```

## Getting Started
Requires Python 3.8+ (no external dependencies).

```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python -m src.main
```

## Configuration
Edit `config/config.json`:

| Key | Description | Default |
|-----|-------------|---------|
| `data_file` | JSON data store | `data/students.json` |
| `export_file` | CSV export path | `data/students_export.csv` |
| `log_file` | Log path | `logs/app.log` |
| `log_level` | DEBUG / INFO / WARNING / ERROR | `INFO` |

Set the `SIS_CONFIG` environment variable to use a different config file
(handy for containers and cloud deployments).

## Running Tests
```bash
python -m unittest discover tests -v
```

## Git Workflow
- `main` is always stable; work happens on `feature/*` branches
- Changes are merged through Pull Requests
- Commit messages follow `type: description` (feat, fix, docs, test, refactor)

## Author
<Your Name>
