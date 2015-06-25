import jinja2
import yaml
import os
import mock
import contextlib
import re

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
        if config["package"] == "":
            _module = __import__(config["module"])
        else:
            _module = __import__(config["package"], fromlist = [config["module"]])
    except ImportError:
        # Todo: Display error message
        return

    mock_modules = []
    for module_str in config["mock"]["modules"]:
        mock_modules.append(mock.patch(config["module"] + '.' + module_str))

    for key, value in config["methods"].iteritems():
        # config = parse_call(value["call"])

        _attr = _module

        with contextlib.nested(mock_modules) as mocks:
            for call in value["calls"]:
                try:
                    _attr = getattr(_attr, call["name"])
                    if value["type"] == "last_method":
                        _method = _attr
                    elif value["type"] == "method":
                        call["args"] = [] if "args" not in call else call["args"]
                        call["kwargs"] = [] if "kwargs" not in call else call["kwargs"]
                        _attr = _attr(*call["args"], **call["kwargs"])
                    elif value["type"] == "variable":
                        pass
                    else:
                        pass
                except:
                    # Todo: Display error message
                    pass

            for case in value["cases"]:
                try:
                    result = _method(*case["args"], **case["kwargs"])
                    if isinstance(result, mock.MagicMock):
                        # I want to find which  mock object should be set return_value to make the result has a return value, not a MagicMock object
                        name = re.search("name=\'[^']*\'", repr(result)).group().split('\'')[1]

                        result = config["module"] + '.' + name
                        case["type"] = "mock"
                    else:
                        case["type"] = "success"
                except Exception as e:
                    result = e.__class__.__name__
                    case["type"] = "error"

                case["result"] = repr(result)

                for index, m in enumerate(mocks):
                    case["mocks"] = []
                    for call in m.mock_calls:
                        param_str = repr(call).split("call")[1]
                        case["mocks"].append( {"module": mock_modules[index], "param_str": param_str} )


    return config


def input_padding(config):
    # pad "kwargs" key and add '"' for string input
    
    for key, value in config["methods"].iteritems():
        for case in value:
            case["args"] = [] if "args" not in case else case["args"]
            case["kwargs"] = {} if "kwargs" not in case else case["kwargs"]
            for count, arg in enumerate(case["args"]):
                if isinstance(arg, basestring):
                    case["args"][count] = repr(arg)

            for k, arg in case["kwargs"].iteritems():
                if type(arg) == "str":
                    case["kwargs"][k] = repr(arg)

    return config




def gen_model():
    for testcase in testlist:
        with open('./schemas/%s.yml' % testcase) as ifile:
            config = yaml.load(ifile)

            import pdb;pdb.set_trace()


            config = catch_output(config)
            config = input_padding(config)
            content = template.render(**config)
            with open('./test_files/test_%s.py' % testcase, 'w') as ofile:
                ofile.write(content)

def run_test():
    for testcase in testlist:
        try:
            os.system("python ./test_files/test_%s.py" % testcase)
        except:
            pass

gen_model()
run_test()

