# HOW TO RUN *converter.py*

## BEFORE:

``` 
	sudo add-apt-repository -yu ppa:deadsnakes/ppa
	sudo apt-get update && sudo apt-get -y install python3.4 python3.4-dev python3.4-venv python3-pip 
```

## MAKE AND RUN VIRTUAL ENVIRONMENT:

``` 
	python3.4 -m venv /path/to/new/virtual/environment/folder
	source /path/to/new/virtual/environment/folder/bin/activate
	pip install -r /path/to/file/requirements.txt
```

## RUN:

``` python converter.py /path/to/source/dir -o /path/to/optional/output/dir -sn 'optional_sheet_name_to_open'```

## DISABLE VIRTUAL ENVIRONMENT:

``` deactivate ```

## ...

## PROFIT!