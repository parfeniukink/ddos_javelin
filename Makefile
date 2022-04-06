BLACK_COMMAND = black ./
FLAKE8_COMMAND = flake8 ./
ISORT_COMMAND = isort ./

.PHONY: run
run:
	sudo python src/run.py 62.173.139.141 443

.PHONY: code_quality
code_quality:
	${BLACK_COMMAND} && ${ISORT_COMMAND} && ${FLAKE8_COMMAND}

