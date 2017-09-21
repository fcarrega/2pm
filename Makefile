# Initialization
init:
	sudo -H pip3 install -r requirements.txt
	sudo -H pip3 install --editable .

	mkdir -p db/
	mkdir -p data/
	mkdir -p reports/

	touch db/reits.json
	touch db/commodities.json
	touch db/mutual_funds.json
	touch db/industries.json
	touch db/reits.json
	touch db/industries.json
	touch db/stocks.json
