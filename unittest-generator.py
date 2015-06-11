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
testlist = [name for name in testlist if ".yml" in name and ".swp" not in name]

for i in range(len(testlist)):
    testlist[i] = testlist[i].replace(".yml", "")


def catch_output(config):
    try:
        if config["path"] == "":
            _module = __import__(config["name"])
        else:
            _module = __import__(config["path"], fromlist = [config["name"]])
    except ImportError:
        # Display error message
        return

    for key, value in config["tests"].iteritems():
        try:
            _method = getattr(_module, key)
        except:
            pass

        for case in value["cases"]:
            try:
                args = case.get("args", [])
                kwargs = case.get("kwargs", {})
                result = _method(*args, **kwargs)
                case["result"] = result
            except Exception as e:
                case["result"] = e.__class__.__name__

    return config


def input_padding(config):
    # pad "kwargs" key and add '"' for string input
    
    for key, value in config["tests"].iteritems():
        for case in value["cases"]:
            case["args"] = [] if "args" not in case else case["args"]
            case["kwargs"] = {} if "kwargs" not in case else case["kwargs"]
            for count, arg in enumerate(case["args"]):
                if isinstance(arg, basestring):
                    case["args"][count] = '"' + arg + '"'

            for k, arg in case["kwargs"].iteritems():
                if type(arg) == "str":
                    case["kwargs"][k] = '"' + arg + '"'

    return config

def gen_model():
    for testcase in testlist:
        with open('./schemas/%s.yml' % testcase) as ifile:
            config = yaml.load(ifile)
            config = catch_output(config)
            config = input_padding(config)
            content = template.render(**config)
            with open('./test_files/test_%s.py' % config['name'], 'w') as ofile:
                ofile.write(content)

def run_test():
    for testcase in testlist:
        os.system("python ./test_files/test_%s.py" % testcase)

gen_model()
run_test()

