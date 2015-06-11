# python-unittest-generator
Auto generating unit testing file and description for python class

******

#### schema format

```
name: "name of module"
path: "path for module"
tests:
    "name of tested method":
        test_instances:
            - args: [arg1, arg2, ...]
            - kwargs: {kwarg1: value1, kwarg2, value2, ......}
            - checktype: "Equal"
    ...
```


******

#### How to use

python unittest-generator.py


