#!/usr/bin/env python3
"""
Test Framework for LaTeX Handout Documents

Validates the Newsletter project documentation for CM Corp.
"""

import os
import re
import subprocess
import sys
from pathlib import Path


class LaTeXTestFramework:
    """Testing framework for LaTeX documentation validation."""

    def __init__(self, tex_file: str, output_dir: str = "."):
        self.tex_file = Path(tex_file)
        self.output_dir = Path(output_dir)
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []

    def run_all_tests(self):
        """Run all validation tests."""
        print("=" * 60)
        print("LaTeX Document Test Framework")
        print("=" * 60)
        print()

        # File existence tests
        self.test_file_exists("LaTeX source exists", self.tex_file)
        self.test_file_exists("Output directory exists", self.output_dir)

        # Content validation tests
        self.test_content_present("CM Corp mentioned", r"CM Corp")
        self.test_content_present("DePLOJ team name present", r"DePLOJ")
        self.test_content_present("Project name Newsletter", r"NEWSLETTER")
        self.test_content_present("Team members section", r"Arbiona.*Claude.*Fredrick.*Martina.*Mikaela.*Nahrin")

        # Page numbering test
        self.test_content_present("Page numbering format", r"\\thepage.*total\{page\}|/.*total")

        # Version and date
        self.test_content_present("Version number", r"v1\.0|Version.*1\.0")
        self.test_content_present("Generation date", r"\\today|Generated:")

        # Build info
        self.test_content_present("Build version in footer", r"Build:")

        # No forbidden content
        self.test_content_absent("No 'Guru' references", r"\\faUserAstronaut|Guru")
        self.test_content_absent("No 'parent' references", r"Parent|parent's")
        self.test_content_absent("No 'Tiny Circuits'", r"Tiny Circuits")
        self.test_content_absent("No 'pasted latex documents'", r"pasted latex")

        # Architecture tests
        self.test_content_present("Data models section", r"Data Models")
        self.test_content_present("CI/CD pipeline section", r"CI/CD")
        self.test_content_present("Technology stack section", r"Technology Stack")

        # Journey tests
        self.test_content_present("Visitor journey section", r"Visitor Journey")
        self.test_content_present("Administrator journey section", r"Administrator Journey")
        self.test_content_present("Conversion funnel section", r"Conversion Funnel")
        self.test_content_present("Newsletter selection section", r"Newsletter Selection")

        # Section count test
        self.test_min_sections(7)

        # Document structure tests
        self.test_content_present("Project Overview section", r"\\section\{Project Overview\}")
        self.test_content_present("Technology Stack section", r"\\section\{Technology Stack\}")
        self.test_content_present("Architecture Design section", r"\\section\{Architecture Design\}")
        self.test_content_present("CI/CD Pipeline section", r"\\section\{CI/CD Pipeline\}")
        self.test_content_present("Key Features section", r"\\section\{Key Features\}")
        self.test_content_present("Setup Instructions section", r"\\section\{Setup Instructions\}")
        self.test_content_present("Summary section", r"\\section\{Summary\}")
        self.test_content_present("Table of contents present", r"\\tableofcontents")

        # Data models diagram test
        self.test_content_present("Data models diagram has proper node structure", r"faUser.*admins")

        # Newsletter Selection Journey diagram tests
        self.test_content_present("Newsletter Selection has landscape", r"\\begin\{landscape\}")
        self.test_content_present("Newsletter Selection has TikZ diagram", r"\\begin\{tikzpicture")
        self.test_content_present("Newsletter Selection has visitor node", r"Subscribe Page")
        self.test_content_present("Newsletter Selection has validate node", r"Validate")
        self.test_content_present("Newsletter Selection has submit node", r"Submit")
        self.test_content_present("Newsletter Selection has welcome node", r"Welcome")
        self.test_content_present("Newsletter Selection has newsletter cards", r"Kost|Nutrition|Workouts|AI Training")

        # TikZ structure tests
        self.test_tikz_node_count("Newsletter diagram", r"\\subsection\{Newsletter Selection", 15)

        # LaTeX compilation test
        self.test_latex_compilation()

        # Print summary
        self.print_summary()

        return self.tests_failed == 0

    def test_file_exists(self, name: str, path: Path):
        """Test if a file exists."""
        if path.exists():
            self.passed(name)
        else:
            self.failed(name, f"File not found: {path}")

    def test_content_present(self, name: str, pattern: str):
        """Test if a pattern is present in the document."""
        try:
            with open(self.tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                self.passed(name)
            else:
                self.failed(name, f"Pattern not found: {pattern}")
        except Exception as e:
            self.failed(name, str(e))

    def test_content_absent(self, name: str, pattern: str):
        """Test that a pattern is NOT present in the document."""
        try:
            with open(self.tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if not re.search(pattern, content, re.IGNORECASE):
                self.passed(name)
            else:
                self.failed(name, f"Forbidden content found: {pattern}")
        except Exception as e:
            self.failed(name, str(e))

    def test_min_sections(self, min_count: int):
        """Test minimum number of sections."""
        try:
            with open(self.tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            sections = len(re.findall(r'\\section\{', content))
            if sections >= min_count:
                self.passed(f"At least {min_count} sections ({sections} found)")
            else:
                self.failed(f"Minimum {min_count} sections", f"Only {sections} sections found")
        except Exception as e:
            self.failed("Section count", str(e))

    def test_latex_compilation(self):
        """Test if LaTeX document compiles successfully."""
        try:
            os.chdir(self.output_dir)
            result = subprocess.run(
                ['xelatex', '-interaction=nonstopmode', '-output-directory=.', str(self.tex_file)],
                capture_output=True,
                text=True,
                timeout=120
            )

            # Check for output PDF
            pdf_path = self.output_dir / "main.pdf"
            if pdf_path.exists():
                self.passed("LaTeX compilation (PDF generated)")
            else:
                self.failed("LaTeX compilation", "PDF not generated")
                if result.returncode != 0:
                    # Extract last few lines of error
                    lines = result.stderr.strip().split('\n')[-10:]
                    self.errors.append("LaTeX errors:\n" + '\n'.join(lines))
        except subprocess.TimeoutExpired:
            self.failed("LaTeX compilation", "Timeout during compilation")
        except FileNotFoundError:
            self.failed("LaTeX compilation", "xelatex not found")
        except Exception as e:
            self.failed("LaTeX compilation", str(e))

        # Test PDF page count
        self.test_pdf_page_count()

    def test_pdf_page_count(self):
        """Test that PDF has expected number of pages."""
        try:
            pdf_path = self.output_dir / "main.pdf"
            if not pdf_path.exists():
                self.failed("PDF page count", "PDF not found")
                return

            # Try to use pdftk or pdfinfo if available
            try:
                result = subprocess.run(
                    ['pdfinfo', str(pdf_path)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.startswith('Pages:'):
                            pages = int(line.split(':')[1].strip())
                            if pages >= 5:
                                self.passed(f"PDF has {pages} pages (expected 5+)")
                            else:
                                self.failed("PDF page count", f"Only {pages} pages found, expected 5+")
                            return
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

            # Fallback: check file size suggests multi-page
            if pdf_path.stat().st_size > 100000:  # > 100KB suggests multi-page
                self.passed("PDF file size suggests multi-page document")
            else:
                self.failed("PDF page count", "Could not verify page count")

        except Exception as e:
            self.failed("PDF page count", str(e))

    def test_tikz_node_count(self, name: str, section_pattern: str, min_nodes: int):
        """Test that a TikZ diagram section has minimum nodes."""
        try:
            with open(self.tex_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the section
            section_match = re.search(section_pattern, content, re.IGNORECASE)
            if not section_match:
                self.failed(name, f"Section not found: {section_pattern}")
                return

            # Extract content from section (simplified - get next 2000 chars)
            start = section_match.end()
            section_content = content[start:start + 3000]

            # Count nodes in TikZ
            nodes = len(re.findall(r'\\node', section_content))

            if nodes >= min_nodes:
                self.passed(f"{name} has {nodes} nodes (expected {min_nodes}+)")
            else:
                self.failed(name, f"Only {nodes} nodes found, expected {min_nodes}+")

        except Exception as e:
            self.failed(name, str(e))

    def passed(self, name: str):
        """Record a passed test."""
        self.tests_passed += 1
        print(f"  \033[92m✓\033[0m {name}")

    def failed(self, name: str, reason: str):
        """Record a failed test."""
        self.tests_failed += 1
        print(f"  \033[91m✗\033[0m {name}")
        print(f"      Reason: {reason}")
        self.errors.append(f"{name}: {reason}")

    def print_summary(self):
        """Print test summary."""
        print()
        print("=" * 60)
        print("Test Summary")
        print("=" * 60)
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {total}")
        print(f"Passed: \033[92m{self.tests_passed}\033[0m")
        print(f"Failed: \033[91m{self.tests_failed}\033[0m")
        print()

        if self.errors:
            print("Errors:")
            for error in self.errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")
            print()

        if self.tests_failed == 0:
            print("\033[92mAll tests passed!\033[0m")
        else:
            print(f"\033[91m{self.tests_failed} test(s) failed.\033[0m")

        print()


def main():
    """Main entry point."""
    # Find the tex file
    tex_file = Path(__file__).parent / "src" / "main.tex"
    output_dir = Path(__file__).parent

    if not tex_file.exists():
        # Try alternative locations
        tex_file = Path("handouts/src/main.tex")
        output_dir = Path("handouts")

    if not tex_file.exists():
        print("Error: Could not find main.tex")
        sys.exit(1)

    # Run tests
    framework = LaTeXTestFramework(tex_file, output_dir)
    success = framework.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
