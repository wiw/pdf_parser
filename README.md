# HOW TO RUN *converter.py*

## LINUX

### BEFORE:

``` 
	sudo add-apt-repository -yu ppa:deadsnakes/ppa
	sudo apt-get update && sudo apt-get -y install python3.4 python3.4-dev python3.4-venv python3-pip git
```

### MAKE AND RUN VIRTUAL ENVIRONMENT:

``` 
	python3.4 -m venv /path/to/new/virtual/environment/folder
	source /path/to/new/virtual/environment/folder/bin/activate
```

### PREPARE TO RUN:

```
	cd ~ && git clone https://github.com/wiw/pdf_parser.git
	cd pdf_parser
	pip install -r requirements.txt
```

#### optional:
If you need pull new version of script, use this command
```
	cd ~/parser_pdf
	git pull origin master 
```

Show help
```
	python converter.py --help
```

### RUN:

```
    python converter.py /path/to/source/dir -o /path/to/optional/output/dir -sn 'optional_sheet_name_to_open'
```

### DISABLE VIRTUAL ENVIRONMENT:

``` deactivate ```

### ...

### PROFIT!

--- 

## WINDOWS 7 and higher

### BEFORE:

Download latest version of python package from [here](https://www.python.org/downloads/windows/) ([python-3.7.2-x86-64](https://www.python.org/ftp/python/3.7.2/python-3.7.2-amd64.exe)/[python-3.7.2-x86](https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe))

**Next** install Git from [git-scm.com](https://git-scm.com/download/win) and 

**Next** in windows command line interface

``` 
	pip install virtualenv
```

### MAKE AND RUN VIRTUAL ENVIRONMENT:

``` 
	cd your_project
	virtualenv env
	\path\to\env\Scripts\activate.bat
```

### PREPARE TO RUN:

```
	cd your_project
	git clone https://github.com/wiw/pdf_parser.git
	cd pdf_parser
	pip install -r requirements.txt
```

#### optional:
If you need pull new version of script, use this command
```
	cd your_project/parser_pdf
	git pull origin master 
```

Show help
```
	python converter.py --help
```

### RUN:

```
    python converter.py /path/to/source/dir -o /path/to/optional/output/dir -sn 'optional_sheet_name_to_open'
```

### DISABLE VIRTUAL ENVIRONMENT:

``` deactivate ```

### ...

### AWESOME!