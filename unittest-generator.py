import jinja2
import yaml
import os

env = jinja2.Environment(
    trim_blocks=True,
    lstrip_blocks=True,
    loader=jinja2.FileSystemLoader('.')
)
template = env.get_template('unittest.pyt')
testlist = os.listdir("./schemas")
for i in range(len(testlist)):
    testlist[i] = testlist[i].replace(".yml", "")


def gen_model():
    for testcase in testlist:
        with open('./schemas/%s.yml' % testcase) as ifile:
            config = yaml.load(ifile)
            content = template.render(**config)
            with open('./test_files/test_%s.py' % config['name'], 'w') as ofile:
                ofile.write(content)

def run_test():
    for testcase in testlist:
        os.system("python ./test_files/test_%s.py" % testcase)

gen_model()
run_test()

