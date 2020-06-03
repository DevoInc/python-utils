from devoutils.faker import FileFakeGenerator

if __name__ == "__main__":
    with open("./simple_syslog_template.jinja2", 'r') as myfile:
        template = myfile.read()

    f = FileFakeGenerator(template=template,
                          probability=80,
                          frequency=(1, 3),
                          verbose=True,
                          file_name="faker_file_example.log")
    f.start()
