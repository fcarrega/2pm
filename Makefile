# Initialization
init:
	pip3 install -r requirements.txt


# Currencies
add_currency:
	python3 finance/currencies.py add $(CURRENCY)

remove_currency:
	python3 finance/currencies.py remove $(CURRENCY)

list_currencies:
	python3 finance/currencies.py list

get_rates:
	python3 finance/currencies.py get_rates


# Industries
add_industry:
	python3 finance/industries.py add $(SECTOR) $(INDUSTRY)

remove_industry:
	python3 finance/industries.py remove $(SECTOR) $(INDUSTRY)

list_industries:
	python3 finance/industries.py list
