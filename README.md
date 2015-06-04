# python-unittest-generator
Auto generating unit testing file and description for python class

******

#### schema format

```
name: [name of module]
path: [path for module]
tests: {
    [name of tested method]: {
		mock: {},
		test_instances: {
			{ input: , output: , type: }
		}
	},
	...
}
```


******

#### How to use

python unittest-generator.py


