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




def patch_func(func, *config):
    def run_func(*args, **kwargs):
        # config["inputs"]
        # config["outputs"]
        func(*args, **kwargs)

    return run_func




def set_mock_return_value(config, mocks)



def test_mocks(config):
    try:
        if config["package"] == "":
            _module = __import__(config["module"])
        else:
            _module = __import__(config["package"], fromlist = [config["module"]])
    except ImportError:
        # Todo: Display error message
        return

    mock_modules = [ config["module"] + '.' + key for key, value in config["mock"].iteritems() ]
    for key, value in config["methods"].iteritems():
        # config = parse_call(value["call"])
        



        _attr = _module
        with contextlib.nested(*mock_modules) as mocks:
            for key, value in config["mock"].iteritems():
                
                

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
                    case["args"] = [] if "args" not in case else case["args"]
                    case["kwargs"] = [] if "kwargs" not in case else case["kwargs"]
                    result = _method(*case["args"], **case["kwargs"])
                except Exception as e:
                    # print e.__class__.__name__
                    pass

                for index, m in enumerate(mocks):
                    for mcall in m.mock_calls:
                        mcall_str = repr(mcall).replace("call", config["module"] + '.' + config["mock"]["modules"][index])
                        mock_attrs.append(mcall_str)

            config["methods"][key]["mocks"] = mock_attrs


    return config





def transform_mock(config):
    # remove dummy mocks & chain the mocks
    for key, value in config["methods"].iteritems():
        new_mocks = []
        for m in value["mocks"]:
            ms = m.replace(re.search("\([^)]+\)", m).group(), "") if re.search("\([^)]+\)", m) else m
            pre = False
            for new_mock in new_mocks:
                if ms.startswith(new_mock):
                    #pre = True
                    break

            if not pre:
                new_mocks.append(ms)

        config["methods"][key]["mocks"] = new_mocks

    import pdb;pdb.set_trace()

    return config


def gen_model():
    for testcase in filelist:
        with open('./schemas/%s.yml' % testcase) as ifile:
            config = yaml.load(ifile)
            config = add_mocks_key_into_config(config)
            config = catch_output(config)
            config = transform_mock(config)


            config = input_padding(config)
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

