import mock
import unittest
{% if package != "" %}from {{ package }} {% endif %}import {{ module }}

class Test{{ module }}(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    {% for key, value in methods.iteritems() %}
    def test_{{ key }}(self):
        {% for key, mock in value["mocks"].iteritems() %}
        def side_effect(*args, **kwargs):
            {% for case in mock["cases"] %}
            if args == {{ case["args"]}} and kwargs == {{ case["kwargs"] }}:
                return {{ case["return_value"] }}
            {% endfor%}

        {{ key }} = mock.Mock(side_effect=side_effect)
        {% endfor %}

        {% for case in value["cases"] %}
            {% if case["result_type"] == "success" %}
        result = {{ module }}.
                {%- for call in value["calls"] -%}
        {{ call["str"] }}{% if not loop.last %}.{% endif %}
                {%- endfor -%}
        (
                {%- if case["args"] -%}
                    {%- for arg in case["args"] -%}
        {{ arg }}{% if not loop.last %}, {% endif %}
                    {%- endfor -%}
                {%- endif -%}
                {%- if case["kwargs"] -%}
                    {%- for kw, arg in case["kwargs"].iteritems() -%}
        {{ kw }} = {{ arg }}{% if not loop.last %}, {% endif %}
                    {%- endfor -%}
                {%- endif -%}
        )
            {% elif case["result_type"] == "error" %}
        try:
            result = {{ module }}.
                {%- for call in value["calls"] -%}
            {{ call["str"] }}{% if not loop.last %}.{% endif %}
                {%- endfor -%}
            (
                {%- if case["args"] -%}
                    {%- for arg in case["args"] -%}
            {{ arg }}{% if not loop.last %}, {% endif %}
                    {%- endfor -%}
                {%- endif -%}
                {%- if case["kwargs"] -%}
                    {%- for kw, arg in case["kwargs"].iteritems() -%}
            {{ kw }} = {{ arg }}{% if not loop.last %}, {% endif %}
                    {%- endfor -%}
                {%- endif -%}
            )
        except Exception as e:
            self.assertEqual(e.__class__.__name__, {{ case["result"] }})
            {% endif %}
        {% endfor %}


        return

    {% endfor %}



if __name__ == '__main__':
    unittest.main()
