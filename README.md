## prefect streamline

prefect_streamline is an opinionated extension that provides helpers to deploy and test Prefect flows quickly and easily.

With its deployment and testing features, you can easily ensure the quality and reliability of your workflows before deploying them.

## Getting started

```bash
pip install prefect_streamline
```

## Usage

### Deploy flow using decorator

``prefect_streamline`` allows you to configure the deployment of flows with a decorator.
Vous pouvez définir plusieurs déploiements pour un même flow.

*myapp/flow.py*
```python
from prefect import flow
from prefect_streamline import deploybook

@deploybook.register(interval=90, name="hello2")
@deploybook.register(cron="*/3 * * * *")
@deploybook.register(name="manual")
@flow(name="main.myflow")
def myflow() -> int:
    return 43
```

the prefect-streamline cli browses all the subfolders of your application.

```bash
# deploy all the flows register into myapp/flow.py
prefect-streamline deploy myapp/flow.py

# search all flow records in all myapp modules.
prefect-streamline deploy --discover src/myapp
```

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/prefect_streamline.git
```

## Developper guideline

```
poetry shell
```

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
poetry install
```

### update the locked dependencies

```bash
poetry update
```

### Run the continuous integration process

Before commit or send a pull request, you have to execute the continuous integration process.

```bash
poetry run alfred ci
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2018-2022 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
