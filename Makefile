UV ?= uv
UV_RUN = $(UV) run --active
PYTEST_ARGS = -v -x -p no:warnings --cov-report term-missing --cov=.

update:
	@$(UV) lock --upgrade && $(UV_RUN) pre-commit autoupdate

install:
	@$(UV) sync --active --group dev
	@$(UV_RUN) pre-commit install -f

lint:
	@$(UV_RUN) pre-commit run --all

.PHONY: tests
tests:
	@$(UV_RUN) pytest $(PYTEST_ARGS)

build:
	@$(UV) build

test:
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" = "" ]; then \
		echo "Usage: make test <path_to_test>. Example: make test megalus/tests.py::test_health_check"; \
		exit 1; \
	fi
	@echo "${BLUE}Running test: $(filter-out $@,$(MAKECMDGOALS))...${NC}"
	@$(UV_RUN) pytest $(PYTEST_ARGS) $(filter-out $@,$(MAKECMDGOALS))
	@echo "${GREEN}Test completed.${NC}"

# Prevent make from treating the argument as a target
%:
	@:
