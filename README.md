# PyBibim
PyBibim(파이비빔)은 파이썬으로 구현한 [Bibim(비빔)](http://bibim-lang.github.io/) 구현체입니다.

PyBibim은 Python2 및 RPython 환경에서 동작하며, 특히 pypy2-5.3.1 버전에서 가장 잘 동작합니다.
CPython 에서도 정상적으로 동작하는 것을 확인했지만, PyPy에 비해 **매우** 느리므로 권장하지 않습니다.

## Live Demo
[PyBibim Live Demo](http://bibim-lang.github.io/pybibim-demo/)를 통해 웹 브라우저에서 바로 PyBibim을 사용해 볼 수 있습니다.

## Quickstart

1. Clone and move

        git clone https://github.com/bibim-lang/pybibim.git
        cd pybibim

2. Install requirements

        pip install -r requirements.txt

3. run the code!

        python pybibim.py <filename>
