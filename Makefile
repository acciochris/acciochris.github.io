SHELL := /bin/bash

.PHONY: html
html:
	source .venv/bin/activate && cd blog && $(MAKE) html

.PHONY: clean
clean:
	source .venv/bin/activate && cd blog && $(MAKE) clean

serve: html
	cd blog/_build/html && python3 -m http.server

.PHONY: dev
dev:
	source .venv/bin/activate && cd blog && $(MAKE) livehtml
