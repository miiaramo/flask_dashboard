# The binary to build (just the basename).
MODULE := flask_dashboard

run:
	@python -m $(MODULE)

test:
	@pytest
