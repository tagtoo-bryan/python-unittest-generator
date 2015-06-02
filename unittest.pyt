import unittest
import {{ name }}

{% for testcase in tesetcases %}
class Test{{ testcase.name }}{unittest.TestCase}:
    def setUp(self):
        return

    def tearDown(self):
        return

    {% for test in tests %}
    def test_{{ test.name }}(self):
        return
    {% endfor %}

{% endfor %}


if __name__ == '__main__':
    unittest.main()
