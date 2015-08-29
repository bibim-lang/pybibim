# PyBibim
PyBibim(파이비빔)은 파이썬으로 구현한 [Bibim(비빔)](http://bibim-lang.github.io/) 구현체입니다.

PyBibim은 Python3 환경에서 동작하며, 특히 pypy3-2.4.0 버전에서 가장 잘 동작합니다.
CPython 에서도 정상적으로 동작하는 것을 확인했지만, PyPy에 비해 **매우** 느리므로 권장하지 않습니다.

## Live Demo
[PyBibim Live Demo](http://bibim-lang.github.io/pybibim-demo/)를 통해 웹 브라우저에서 바로 PyBibim을 사용해 볼 수 있습니다.

(단, 해당 페이지는 Python2로 backport된 PyBibim을 사용합니다.)

## Quickstart

1. clone and move

        git clone https://github.com/bibim-lang/pybibim.git
        cd pybibim

2. install [rply](https://github.com/alex/rply)

        pip install rply

3. run the code!

        python pybibim.py <filename>
