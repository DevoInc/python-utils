from devoutils.faker import SyslogFakeGenerator
from devo.sender import Sender

if __name__ == "__main__":
    with open("./simple_syslog_template.jinja2", 'r') as myfile:
        template = myfile.read()

    con = None
    # This example need a sender con
    # Example
    # con = Sender(config="./config.yaml")

    # If you remove simulation or set to false, data will be send
    f = SyslogFakeGenerator(engine=con,
                            template=template,
                            simulation=True,
                            probability=100,
                            frequency=(1, 1),
                            verbose=True)
    f.start()

