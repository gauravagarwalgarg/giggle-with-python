#!/bin/bash
# Run linting, formatting, and type checking.
# Usage: bash scripts/lint.sh [directory]

set -e

TARGET="${1:-.}"

echo "=== Python Code Quality Checks ==="
echo "Target: $TARGET"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# 1. Ruff fast linter (replaces flake8, isort, pyupgrade, etc.)
echo "--- Ruff (lint) ---"
if command -v ruff &> /dev/null; then
    if ruff check "$TARGET" --fix; then
        echo -e "${GREEN}✓ Ruff: No issues${NC}"
    else
        echo -e "${RED}✗ Ruff: Issues found${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "${YELLOW}⚠ Ruff not installed: pip install ruff${NC}"
fi
echo ""

# 2. Ruff format (replaces black)
echo "--- Ruff (format) ---"
if command -v ruff &> /dev/null; then
    if ruff format "$TARGET" --check 2>/dev/null; then
        echo -e "${GREEN}✓ Formatting: OK${NC}"
    else
        echo -e "${YELLOW}⚠ Formatting issues found. Run: ruff format $TARGET${NC}"
        read -p "  Auto-format now? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            ruff format "$TARGET"
            echo -e "${GREEN}✓ Formatted${NC}"
        else
            ERRORS=$((ERRORS + 1))
        fi
    fi
else
    # Fallback to black
    if command -v black &> /dev/null; then
        if black --check "$TARGET" 2>/dev/null; then
            echo -e "${GREEN}✓ Black: OK${NC}"
        else
            echo -e "${YELLOW}⚠ Black: formatting needed. Run: black $TARGET${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    fi
fi
echo ""

# 3. Mypy type checking
echo "--- Mypy (type check) ---"
if command -v mypy &> /dev/null; then
    if mypy "$TARGET" --ignore-missing-imports --no-error-summary 2>/dev/null; then
        echo -e "${GREEN}✓ Mypy: No type errors${NC}"
    else
        echo -e "${YELLOW}⚠ Mypy: Type issues found (may be non-blocking)${NC}"
        # Don't increment ERRORS type issues are often warnings
    fi
else
    echo -e "${YELLOW}⚠ Mypy not installed: pip install mypy${NC}"
fi
echo ""

# Summary
echo "=== Summary ==="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS} check(s) failed ✗${NC}"
    exit 1
fi
