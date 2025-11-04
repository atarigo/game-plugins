# Makefile for game-plugins
PY := uv run

# ANSI color codes
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

.PHONY: help dev format test

help: ## Show available commands
	@echo "$(GREEN)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(CYAN)%-12s$(RESET) %s\n", $$1, $$2}'

dev: format test ## Run development server
	@echo "$(YELLOW)Running development server...$(RESET)"
	$(PY) main.py

format: ## Format code and check for errors
	@echo "$(YELLOW)Running ruff format...$(RESET)"
	$(PY) ruff format .
	@echo "$(YELLOW)Running ruff check with auto-fix...$(RESET)"
	$(PY) ruff check --fix .
	@echo "$(GREEN)✓ Format completed!$(RESET)"

test: ## Run tests (usage: make test args="-v -rP")
	@echo "$(YELLOW)Running tests...$(RESET)"
	$(PY) pytest $(args)
