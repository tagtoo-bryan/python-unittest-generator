import unittest
{% if path != "" %}from {{ path }} {% endif %}import {{ name }}

class Test{{ name }}(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    {% for key, value in tests.iteritems() %}
    def test_{{ key }}(self):
        {% for case in value %}

        {% if case["error"] %}

        self.assertRaises({{ case["result"] }}, {{ name }}.{{ key }},
            {%- for arg in case["args"] -%}
            {{ arg }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}

            {%- if kwargs -%},

            {%- for k, arg in case["kwargs"].iteritems() -%}
            {{ k }}={{ arg }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}

            {%- endif -%}
        )

        {% else %}
        result = {{ name }}.{{ key }}(
            {%- for arg in case["args"] -%}
            {{ arg }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}

            {%- if kwargs -%}, 

            {%- for k, arg in case["kwargs"].iteritems() -%}
            {{ k }}={{ arg }}{% if not loop.last %}, {% endif %}
            {%- endfor -%}

            {%- endif -%}
        )

        self.assertEqual(result, {{ case["result"] }})

        {% endif %}

        {% endfor %}
        return

    {% endfor %}



if __name__ == '__main__':
    unittest.main()
