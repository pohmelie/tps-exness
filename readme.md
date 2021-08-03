# Test project solution for exness (calculator)

## Install

``` bash
python -m pip install -e ./[dev]
```

## Run

``` bash
python -m tps_exness --web-port 8080
```

or

``` bash
docker build . -t tps-exness
docker run --rm -it -p 8080:80 tps-exness
```

After that you can check web interface via http://localhost:8080 and check docs with http://localhost:8080/docs

## Test

``` bash
pytest
```
