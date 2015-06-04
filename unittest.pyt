import unittest
{% if path != "" %}from {{path}} {% endif %}import {{name}}

class Test{{ name }}(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    {% for key, value in tests.iteritems() %}
    def test_{{ key }}(self):
        {% for instance in value.test_instances %}
        self.assertEqual({{name}}.{{ key }}(
            {%- for input in instance["input"] -%}
            {{input}}{% if not loop.last %}, {% endif %}
            {%- endfor -%}
        ), {{ instance["output"] }})
        {% endfor %}
        return

    {% endfor %}



if __name__ == '__main__':
    unittest.main()
