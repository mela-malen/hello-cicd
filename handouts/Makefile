HANDOUTS_DIR = .
SRC_DIR = src
TEST_FILE = test_handouts.py

all: pdf test

pdf: $(SRC_DIR)/main.tex
	xelatex -output-directory=$(HANDOUTS_DIR) $(SRC_DIR)/main.tex
	@echo "PDF generated: handouts/main.pdf"
	@if [ -f $(HANDOUTS_DIR)/main.pdf ]; then echo "SUCCESS: handouts/main.pdf is ready"; fi

test: $(TEST_FILE)
	@echo "Running LaTeX document tests..."
	python3 $(TEST_FILE)

clean:
	rm -f $(HANDOUTS_DIR)/*.pdf $(HANDOUTS_DIR)/*.log $(HANDOUTS_DIR)/*.aux $(HANDOUTS_DIR)/*.out $(HANDOUTS_DIR)/*.toc

view: pdf
	@if command -v xdg-open > /dev/null; then xdg-open $(HANDOUTS_DIR)/main.pdf; \
	  elif command -v open > /dev/null; then open $(HANDOUTS_DIR)/main.pdf; \
	fi

.PHONY: all pdf test clean view
