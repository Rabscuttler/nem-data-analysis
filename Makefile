.PHONY: clean data lint requirements create_conda_env, create_pipenv_env setup_jupyter_lab

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = nem-data-analysis
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

ifeq (,$(shell which pipenv))
HAS_PIPENV=False
else
HAS_PIPENV=True
endif
#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_python
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Make Dataset
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Set up python interpreter environment using conda and environment.yml
create_conda_env:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
	conda env create .
	@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
else
	@echo ">>> Conda not detected. Install conda, add to env variables and try again."
endif

## Set up python interpreter environment using Pipenv
create_pipenv_env: requirements
	@echo ">>> Installing snappy for parquet libraries"
	sudo apt install libsnappy-dev
	@echo ">>> Installing Pipenv using requirements.txt, then installing dependencies from Pipfile.lock"
	pipenv sync
	@echo ">>> New pipenv created. Run environment in shell fron this folder using:\npipenv shell"

## Set up jupyter-lab extensions
setup_jupyter_lab:
	# Avoid "JavaScript heap out of memory" errors during extension installation
	# (OS X/Linux)
	export NODE_OPTIONS=--max-old-space-size=4096

	# Jupyter widgets extension
	jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.1 --no-build
	# FigureWidget support
	jupyter labextension install plotlywidget@4.6.0 --no-build
	# and jupyterlab renderer support
	jupyter labextension install jupyterlab-plotly@4.6.0 --no-build
	# Matplotlib
	jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib --no-build
	# Build extensions (must be done to activate extensions since --no-build is used above)
	jupyter lab build
	unset NODE_OPTIONS


## Test python version
test_python:
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER) --version))
	@echo ">>> Correct version of Python installed, test passed."
else
	@echo ">>> Install Python 3"
endif

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
RAW_DIR = ./data/raw
PROC_DIR = ./data/processed
SRC_DIR = ./source_code/src/

FETCH_PAR = $(join $(SRC_DIR), data/fetch_and_clean_nem_participants.py)
FETCH_MAP = $(join $(SRC_DIR), data/fetch_causer_pays_mappings.py)

.PHONY: activate_env get_participants get_fcas_mappings

## Activate python env. Preferences Pipenv
activate_env:
ifeq (True,$(HAS_PIPENV))
	@pipenv shell
else
	@source activate $(PROJECT_NAME)
endif

## Fetch and clean NEM participants data
get_participants:
	$(PYTHON_INTERPRETER) $(FETCH_PAR) -raw_path $(RAW_DIR) -proc_path $(PROC_DIR)

## Fetch 4s Causer Pays data mapping
get_fcas_mappings:
	$(PYTHON_INTERPRETER) $(FETCH_MAP) -path $(RAW_DIR)
#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
