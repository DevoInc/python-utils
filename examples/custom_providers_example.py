from devoutils.faker import SyslogFakeGenerator
import random
from devo.sender import Sender


def get_choices():
    return ["Failed", "Success", "Totally broken", "404", "500", "What?"]


if __name__ == "__main__":
    with open("./custom_providers_template.jinja2", 'r') as myfile:
        template = myfile.read()

    con = None
    # This example need a sender con
    # Example
    # con = Sender(config="./config.yaml")

    custom = {"random": random, "choices": get_choices}

    # If you remove simulation or set to false, data will be send
    f = SyslogFakeGenerator(engine=con,
                            template=template,
                            simulation=True,
                            probability=80,
                            frequency=(0.1, 3),
                            providers=custom,
                            verbose=True)
    f.start()
