# Initialization
init:
	sudo -H pip3 install -r requirements.txt
	sudo -H pip3 install --editable .

	mkdir -p db/
	mkdir -p data/
	mkdir -p reports/

	touch db/commodities.json
	touch db/funds.json
	touch db/reits.json
	touch db/stocks.json

	touch db/currencies.json
	touch db/industries.json
