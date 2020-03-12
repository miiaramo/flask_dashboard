MODULE := dashboard

run:
	@python -m $(MODULE)

test:
	@pytest
