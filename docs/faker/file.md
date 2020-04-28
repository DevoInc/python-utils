## File fake generator

### Class

* [FileFakeGenerator](../../devoutils/faker/generators/file_fake_generator.py)

### Doc

file_name

This generator is mainly intended to create files with fake data.

You have one example in simple_file_template, we explain here:

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
