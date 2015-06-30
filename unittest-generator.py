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
filelist = os.listdir("./schemas")
filelist = [name for name in filelist if ".yml" in name and ".swp" not in name]

for i in range(len(filelist)):
    filelist[i] = filelist[i].replace(".yml", "")


def patch_func(func, config, method_name, mock_name):
    def run(*args, **kwargs):
        error = None
        try:
            result = func(*args, **kwargs)
            result_type = 'success'
        except Exception as e:
            error = e
            result = e.__class__.__name__
            result_type = 'error'

        for case in config["methods"][method_name]["mocks"][mock_name]["cases"]:
            if case["args"] == args and case["kwargs"] == kwargs:
               return

        config["methods"][method_name]["mocks"][mock_name]["cases"].append(
            { "args": list(args), "kwargs": kwargs, "return_value": result, "return_type": result_type }
        )

        if error:
            raise(error)

        return result

    return run



def config_padding(config):
    for key, value in config["methods"].iteritems():
        value["mocks"] = {}
        for call in value["calls"]:
            call["args"] = [] if "args" not in call else call["args"]
            call["kwargs"] = [] if "kwargs" not in call else call["kwargs"]
        for case in value["cases"]:
            case["args"] = [] if "args" not in case else case["args"]
            case["kwargs"] = [] if "kwargs" not in case else case["kwargs"]

    return config


def find_mocks(config) :
    try:
        if config["package"] == "":
            _module = __import__(config["module"])
        else:
            _module = __import__(config["package"], fromlist = [config["module"]])
    except ImportError:
        # Todo: Display error message
        return

    mock_modules = [ config["module"] + '.' + mock_module for mock_module in config["mock"] ]
    for key, value in config["methods"].iteritems():
        _attr = _module
        for call in value["calls"]:
            try:
                _attr = getattr(_attr, call["name"])
                if call["type"] == "last_method":
                    _method = _attr
                elif call["type"] == "method":
                    call["args"] = [] if "args" not in call else call["args"]
                    call["kwargs"] = [] if "kwargs" not in call else call["kwargs"]
                    _attr = _attr(*call["args"], **call["kwargs"])
                elif call["type"] == "variable":
                    pass
                else:
                    pass
            except Exception as e:
                # Todo: Display error message
                pass

        for case in value["cases"]:
            with contextlib.nested(mock.patch(*mock_modules)) as mocks:
                try:
                    result = _method(*case["args"], **case["kwargs"])
                except Exception as e:
                    # print e.__class__.__name__
                    pass

            for index, m in enumerate(mock_modules):
                for mcall in mocks[index].method_calls:
                    real_call = re.search("^[^(]*", repr(mcall)).group().replace("call", m)
                    if real_call not in value["mocks"]:
                        value["mocks"][real_call] = {
                            "calls": real_call.replace(config["module"] + ".", "").split('.'),
                            "cases": []
                        }

    return config


def real_run(config):
    try:
        if config["package"] == "":
            _module = __import__(config["module"])
        else:
            _module = __import__(config["package"], fromlist = [config["module"]])
    except ImportError:
        # Todo: Display error message
        return

    mock_modules = [ config["module"] + '.' + mock_module for mock_module in config["mock"] ]
    for key, value in config["methods"].iteritems():
        _attr = _module
        for name, content in value["mocks"].iteritems():
            for call in content["calls"][:-1]:
                try:
                    _attr = getattr(_attr, call)
                except Exception as e:
                    # Todo: Display error message
                    pass

            try:
                setattr(_attr, content["calls"][-1], patch_func(getattr(_attr, content["calls"][-1]), config, key, name))
            except Exception as e:
                # Todo: Display error message
                pass

        _attr = _module
        for call in value["calls"]:
            try:
                _attr = getattr(_attr, call["name"])
                if call["type"] == "last_method":
                    _method = _attr
                elif call["type"] == "method":
                    call["args"] = [] if "args" not in call else call["args"]
                    call["kwargs"] = [] if "kwargs" not in call else call["kwargs"]
                    _attr = _attr(*call["args"], **call["kwargs"])
                elif call["type"] == "variable":
                    pass
                else:
                    pass
            except Exception as e:
                # Todo: Display error message
                pass

        for case in value["cases"]:
            try:
                case["result"] = _method(*case["args"], **case["kwargs"])
                case["result_type"] = "success"
            except Exception as e:
                case["result"] = e.__class__.__name__
                case["result_type"] = "error"

    return config

def repr_config(config):
    for key, value in config["methods"].iteritems():
        for case in value["cases"]:
            case["result"] = repr(case["result"])
            for index, arg in enumerate(case["args"]):
                case["args"][index] = repr(arg)
            for kw, arg in case["kwargs"].iteritems():
                case["kwargs"][kw] = repr(arg)

        for s, mock in value["mocks"].iteritems():
            for case in mock["cases"]:
                case["return_value"] = repr(case["return_value"])
                for index, arg in enumerate(case["args"]):
                    case["args"][index] = repr(arg)
                for kw, arg in case["kwargs"].iteritems():
                    case["kwargs"][kw] = repr(arg)

    return config





def gen_model():
    for testcase in filelist:
        with open('./schemas/%s.yml' % testcase) as ifile:
            config = yaml.load(ifile)
            config = config_padding(config)
            config = find_mocks(config)
            config = real_run(config)
            config = repr_config(config)
            content = template.render(**config)
            with open('./test_files/test_%s.py' % testcase, 'w') as ofile:
                ofile.write(content)

def run_test():
    for testcase in filelist:
        try:
            os.system("python ./test_files/test_%s.py" % testcase)
        except:
            pass

gen_model()
run_test()


"""
    I want the config be the form when using in the template, (repr before giving to template)

    get_object:
        calls:
            - { name: 'GraphAPI', args: [], kwargs: {access_token: 'post_id', version: '2.2'}, type: 'method' }
            - { name: 'get_object', type: 'last_method' }
        cases:
            - { args: [], kwargs: {id: 'post_id'}, result: object, result_type: 'error/success' }

        mocks:{
                  'facebook.requests.request': {
                      calls: ['requests', 'request']
                      cases:
                          - { args: ['GET', 'http://www.google.com.tw'], kwargs: {}, return_value: '<HTTP 200>', return_type: 'success' }
                          - { args: [], kwargs: {}, return_value: 'ParameterError?', return_type: 'error'}
                  },
              }

"""

