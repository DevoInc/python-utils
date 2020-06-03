## Syslog fake generator

### Class

* [SyslogFakeGenerator](../../devoutils/faker/generators/syslog_fake_generator.py)

### Doc

This generator is mainly intended to be used with [devo-sdk](https://github.com/DevoInc/python-sdk), 
using the Sender to send false data to Devo to simulate 
data entry, useful for pocs, tets, etc.

You have one example in simple_syslog_template, we explain here:

Script:

    from devoutils.faker import SyslogFakeGenerator
    from devo.sender import Sender
    
    if __name__ == "__main__":
        with open("./simple_syslog_template.jinja2", 'r') as myfile:
            template = myfile.read()

    con = Sender(config="./config.yaml")

    f = SyslogFakeGenerator(engine=con,
                            template=template,
                            probability=100,
                            frequency=(1, 1),
                            tag="my.app.request.info",
                            verbose=True)
    f.start()


With this code we create one Sender With this basic code we create a Sender with the devo-sdk to send data to 
Devo, and we create a SyslogFakeGenerator to create the false data.

You have to add the tag that you want to send in the creation of the SyslogFakeGenerator object, a
nd the generator will be in charge of using the con.send function (tag = self.tag, msg = fake_data_line) to send the data

Template:

    {%- set type = fake.random_element(["post", "get"]) -%}
    {{ next(date_generator) }} receiving {{ type }} request.
    {%- set a = 3 -%}
    
    
### CLI Usage

You can use this generator without any flags. Its the default execution of cli shell


    devo-faker --template "~/python-utils/examples/simple_syslog_template.jinja2" --config "config.yaml"
    
config.yaml:

    faker:
      probability: 80
      frequency: (2,5)
    sender:
      *devo-sdk configuration


You have more info, flags and options in [Terminal/Shell CLI usage](shellcli.md)



## Raw syslog fake generator
### Class

* [SyslogRawFakeGenerator](../../devoutils/faker/generators/syslog_raw_fake_generator.py)

### Doc

This generator is mainly intended to be used with [devo-sdk](https://github.com/DevoInc/python-sdk) too, 
but using the function [send_raw](https://github.com/DevoInc/python-sdk/blob/99844f1e849c470425565820dc62013e15613bde/devo/sender/data.py#L376)

It is the same in everything normal, except in, instead of using the devo-sdk to 
generate the syslog message headers, and you only 
create the data, in your template you will need to generate the entire line to send. 
This generator does not need the tag, since you add it in the headers

    <14>Jan  1 00:00:00 MacBook-Pro-de-X.local my.app.devo_sender.test: my data


### CLI Usage

You can use this generator with the option `--raw_mode`


    devo-faker --template "~/python-utils/examples/simple_syslog_template.jinja2" --config "config.yaml" --raw_mode
    
config.yaml:

    faker:
      probability: 80
      frequency: (2,5)
    sender:
      *devo-sdk configuration


You have more info, flags and options in [Terminal/Shell CLI usage](shellcli.md)
