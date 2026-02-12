# Newsletter - CM Corp Project Documentation

LaTeX source files for the CM Corp Newsletter platform presentation.

## Directory Structure

```
handouts/
├── src/                    # LaTeX source files
│   └── main.tex           # Main document (7 sections)
├── test_handouts.py       # Test framework
├── main.pdf               # Generated PDF output
├── Makefile               # Build automation
└── README.md              # This file
```

## Project Details

| Field | Value |
|-------|-------|
| **Project Name** | Newsletter |
| **Customer** | CM Corp |
| **Team** | DePLOJ |
| **Team Members** | Mikaela, Fredrick, Arbiola, Martina, Nahrin |
| **Version** | 1.0 |

## Building the PDF

### Prerequisites
```bash
# Debian/Ubuntu
sudo apt-get install texlive-xetex fonts-noto fonts-fontawesome5

# Required packages (texlive-latex-extra):
# - fontspec, babel, tcolorbox, fontawesome5, tikz, booktabs, amssymb
```

### Build Commands

```bash
cd handouts

# Build PDF and run tests
make all

# Build PDF only
make pdf

# Run tests only
make test

# View PDF (Linux)
make view

# Clean build artifacts
make clean
```

## Testing Framework

The project includes a comprehensive test framework (`test_handouts.py`) that validates:

- **Content Validation:**
  - CM Corp mentioned
  - DePLOJ team name present
  - All team members listed
  - Version number and date present
  - Page numbering format ("1 / 5")

- **Forbidden Content:**
  - No "Guru" references
  - No "parent" references
  - No "Tiny Circuits" references

- **Structure Validation:**
  - Required sections present
  - Minimum section count (6)

- **Compilation:**
  - LaTeX compiles successfully
  - PDF generated

### Run Tests
```bash
python3 test_handouts.py
```

## Document Contents

| Section | Title |
|---------|-------|
| 1 | Project Overview |
| 2 | Technology Stack |
| 3 | Architecture Design |
| 4 | CI/CD Pipeline |
| 5 | Key Features |
| 6 | Setup Instructions |
| 7 | Summary |

## Styling Features

- **Colors:** Charcoal text (#2D3436), Neon Pink (#FF00FF), Neon Cyan (#00FFFF)
- **Fonts:** Source Sans Pro (soft, easy-to-read)
- **Custom Boxes:**
  - `\begin{insightbox}{...}` - Key insights (pink)
  - `\begin{stepbox}{...}` - Step-by-step (mint/cyan)
  - `\begin{importantbox}{...}` - Important notices (red/pink)
  - `\begin{techbox}{...}` - Technical details (yellow/orange)
  - `\begin{featurebox}{...}` - Features (neon cyan)

## Page Layout

- **Header Left:** DePLOJ (team name)
- **Header Right:** Newsletter - CM Corp
- **Footer Center:** Current page / Total pages (e.g., "1 / 6")
- **Footer Right:** Date | v1.0

## Editing

Open `src/main.tex` in any LaTeX editor (VS Code with LaTeX Workshop, TeXStudio, etc.) and modify as needed.

## Output

- **PDF Pages:** 6
- **File Size:** ~50KB
