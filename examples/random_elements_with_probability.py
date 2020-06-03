from devoutils.faker import SyslogFakeGenerator
from collections import OrderedDict
import random
from devo.sender import Sender


def get_choices():
    """Get dict with options and probability of be selected"""
    return OrderedDict([("Failed", 0.5),
                        ("Success", 0.2),
                        ("Totally broken", 0.1),
                        ("404", 0.1),
                        ("500", 0.05),
                        ("What?", 0.05)])


if __name__ == "__main__":
    with open("./random_elements_with_probability.jinja2", 'r') as myfile:
        template = myfile.read()

    con = None
    # This example need a sender con
    # Example
    # con = Sender(config="./config.yaml")

    custom = {"choices": get_choices}

    # If you remove simulation or set to false, data will be send
    f = SyslogFakeGenerator(engine=con,
                            template=template,
                            simulation=True,
                            probability=100,
                            frequency=(1, 1),
                            providers=custom,
                            verbose=True)
    f.start()
