import jinja2
import yaml
import os

env = jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=jinja2.FileSystemLoader('.')
)
template = env.get_template('unittest.pyt')

def gen_model():
    for testcase in os.listdir('./tests'):
        import pdb;pdb.set_trace()
        with open('./tests/%s' % testcase) as ifile:
            config = yaml.load(ifile)
            content = template.render(**config)
            with open('./db/nodes/%s.py' % config['name'], 'w') as ofile:
                ofile.write(content)

gen_model()
assert os.system('apidoc -i db') == 0
# assert os.system('appcfg.py update .') == 0
