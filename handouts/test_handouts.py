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
        self.test_content_present("Build version in footer", r"Build:|git rev-parse")

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

        # Data models diagram test
        self.test_content_present("Data models diagram has proper node structure", r"faUser.*admins")

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
