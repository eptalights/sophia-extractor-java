# sophia-extractor-java
An [Eptalights](http://eptalights.com) Sophia Java tool for extracting Java (Jimple) instructions into JSON format.


## Installation

install the Python package `sophia-extractor-java` with:
```sh
pip install git+https://github.com/eptalights/sophia-extractor-java.git
```

Alternatively, you may clone the code from GitHub and build from source (git assumed to be available):

```sh
git clone https://github.com/eptalights/sophia-extractor-java.git
pip install path/to/sophia-extractor-java
```


## Usage

##### Extract Java (JIMPLE) code from a JAR file or a directory of compiled class files.

Use the `--binary-path` (or `-b`) option to specify the path to the JAR file or the directory containing compiled `.class` files.  

The extracted JSON data will be saved to the location specified by the `--extract-path` (or `-e`) option.  

If `--extract-path` is not provided, the output will be saved to the default directory: `./jimple_output`.

```sh
sophia_java_extractor --binary-path=/path/to/JARFILE.jar
```

or

```sh
sophia_java_extractor --binary-path=/path/to/classes_directory
```


## Setting up a Development Environment

The latest code under development is available on GitHub at https://github.com/eptalights/sophia-extractor-java.  
To obtain this version for experimental features or for development:

```bash
git clone https://github.com/eptalights/sophia-extractor-java.git
cd eptalights-python
pip install -e ".[dev]"
```

To run tests and styling checks:

```bash
pytest
flake8 src tests
black --check src tests
```


