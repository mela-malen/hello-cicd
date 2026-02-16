HANDOUTS_DIR = .
SRC_DIR = src
TEST_FILE = test_handouts.py
VERSION_FILE = version.tex
VERSION_TRACKER = .version_number

all: pdf test

pdf: $(SRC_DIR)/main.tex $(VERSION_FILE)
	xelatex -output-directory=$(HANDOUTS_DIR) $(SRC_DIR)/main.tex
	@echo "PDF generated: handouts/main.pdf"
	@if [ -f $(HANDOUTS_DIR)/main.pdf ]; then echo "SUCCESS: handouts/main.pdf is ready"; fi

$(VERSION_FILE): $(VERSION_TRACKER)
	@echo "Generating version info..."
	@GIT_COMMIT=$$(git rev-parse --short HEAD) && \
	VERSION_NUM=$$(cat $(VERSION_TRACKER)) && \
	printf "\\\\newcommand{\\\\gitcommit}{%s}\n" "$$GIT_COMMIT" > $(VERSION_FILE) && \
	printf "\\\\newcommand{\\\\versionnumber}{%s}\n" "$$VERSION_NUM" >> $(VERSION_FILE)

$(VERSION_TRACKER):
	@echo "Initializing version tracker..."
	@echo "1" > $(VERSION_TRACKER)

increment-version:
	@echo "Incrementing version number..."
	@awk 'BEGIN {getline v < "$(VERSION_TRACKER)"; print v+1 > "$(VERSION_TRACKER)"}'

version: $(VERSION_TRACKER) increment-version $(VERSION_FILE)
	@echo "Current version: $$(cat $(VERSION_TRACKER))"
	@echo "Git commit: $$(git rev-parse --short HEAD)"

test: $(TEST_FILE)
	@echo "Running LaTeX document tests..."
	python3 $(TEST_FILE)

clean:
	rm -f $(HANDOUTS_DIR)/*.pdf $(HANDOUTS_DIR)/*.log $(HANDOUTS_DIR)/*.aux $(HANDOUTS_DIR)/*.out $(HANDOUTS_DIR)/*.toc
	rm -f $(VERSION_FILE)

view: pdf
	@if command -v xdg-open > /dev/null; then xdg-open $(HANDOUTS_DIR)/main.pdf; \
	  elif command -v open > /dev/null; then open $(HANDOUTS_DIR)/main.pdf; \
	fi

.PHONY: all pdf test clean view version increment-version
