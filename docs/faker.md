# Devo Faker
### Overview
Fake event generator

Generates fake events on realtime or on batch mode. Use the realtime
mode to generate realtime events to send or save them, or the
batch mode to generate a lot of events at once and save/send the events.

## Features
- Generate logs in batch mode and dump them to a file
- Uses jinja2 for templates with an event by line
- Uses faker for generate random data
- Probability 0-100 for process or not the next event
- Frequency as range in seconds for use random behaviour
- Mode interactive to decide when to launch the next iteration
- Mode simulation to send to a file

## Index - Fast reference

* [Jinja2 (Templates) documentation](https://jinja.palletsprojects.com/en/2.11.x/)
* [Generic variables](#Initializing base generator)
* [Devo-utils providers](#Devo-utils providers)
* [Custom providers](#Custom providers in script mode)
* [Third party providers](#Third party providers)
* [Important clarification in Jinja2](#Important clarification in Jinja2)

#### Usage

* [Batch fake generator](faker/batch.md)
* [File fake generator](faker/file.md)
* [Realtime fake generator](faker/realtime.md)
* [Simulation fake generator](faker/simulation.md)
* [Syslog fake generator](faker/syslog.md#syslog fake generator)
* [Syslog raw fake generator](faker/syslog.md#raw syslog fake generator)
* [Terminal/Shell CLI usage](faker/shellcli.md)


## Script usage

The specific use of each generator is in its respective file, in the above list. Here you have common uses

#### Initializing base generator

Devo-utils has several types of generators, and there are also several ways to initialize them, but 
all use BaseFakeGenerator as base class, soo you have common variables 
(Below is any flag that is in two or more fake generators)

Variable descriptions:

+ _engine_ **(_Sender_)**: Normal, a Sender object from devo-sdk, but you can use any object with a "send" function l
ike Sender class
+ _template_ **(_string_)**: Jinja2 template loaded as str
+ Simple probability and frequency: With this option you have one probability and frequency all time fixed.
    + _probability_ **(_integer_)**: Send probability: in the moment of send data, you can have probability from 0 to 100 
of send the event. 
This can make sending events somewhat more random, creating a more realistic graph, instead of sending 10 
events every second, with a probability of 70 (%) there will be variability. 
    + _frequency_ **(_tuple_)**: Tuple of integers with the minimum and maximum frequency, random, to send events:
        + **Example:** (1,2) means that events will be sent with a random frequency of between 1 and 2 seconds.
        + **Example:** (0.1, 1) decimals can be used
        + **The frequency is calculated in each send**, therefore if you put: (0,10) a random number (in seconds) 
        between 0 and 10 will be obtained, for example 6. It will wait 6 seconds and an event will be sent, and will 
        recalculate. For example, 10 in the next iteration = 10sg will be waited and the event will be sent (Always 
        taking into consideration the probability, of course), and it will be recalculated again and again each 
        iteration.
+ Complex probability and frequency:
    + With this option you can create rules to change the probability and frequency based on time periods, to create 
    false data more in line with a possible reality, for example: more data at peak times, at work hours, or on 
    weekends, etc.
    + _time_rules_ (_list_): list of objects, each objects its a rule. This value its not available as flag in CLI 
    mode, you need add values to the config file. Each object has 3 values -> 
    `{"rule": "", "probability": 1, "frequency": (1,10)}`
        + rule **(_string_)**: With CRON syntax you can create rules to change the probability and frequency of 
        shipments. These rules can be executed once (For example "0 8 * * *") or they can be rules that include ranges 
        (For example "* 8-18 * * *) you can even use a default like" * * * * * " .
        
          The priority, regarding rules that affect the same time range, will always be in order of appearance, that is, the 
first rule in the list is more priority than the following ones, if they share time periods. Therefore, in the example 
below, the second rule will only apply from 9:00 to 18:00, since the first rule also affects from 8:00 to 9:00.

          If it doesn't find a rule that applies for a moment, it will continue with the last one that was executed
        + probability **(_integer_)**: Same values as explained above
        + frequency **(_tuple_)**: Same values as explained above
        + **example:** time_rules=[{"rule": "0 0-9 * * *", "probability": 90, "frequency": (0.5, 2)}, 
        {"cron": "0 18 * * *", "probability": 30, "frequency": (5, 10)}]
        
+ interactive **(_bool_)**: interactive moode wait for your interaction to make the next event submission
+ simulation **(_bool_)**: If true, the events are not sent or written, they are only shown on the screen as if
 they had been done
+ verbose **(_bool_)**: verbose mode
+ date_generator **(_object_)**: date_generator for use next() in templates, default is `str(datetime.now())`.

##### some examples

Simple syslog faker generator, sending data using devo-sdk Sender:

Script:

    from devoutils.faker import SyslogFakeGenerator
    ....
    con = Sender(config=config)
    with open("test_template.jinja2", 'r') as myfile:
        template = myfile.read()

    sfg = SyslogFakeGenerator(engine=con, 
                              template=template, 
                              simulation=True,
                              probability=75,
                              frequency=(0.1, 5)
                              verbose=True)
    sfg.start()

Template:

    {#- Log -#}
    {%- set type = fake.random_element(["post", "get"]) %}
    {%- set nextdate = next(date_generator) -%}
    {{ nextdate }} receiving {{ type }} request


With the same template we can make more script examples:

    sfg = SyslogFakeGenerator(engine=con, 
                              template=template, 
                              time_rules=[
                                    {"rule": "0 8 * * *", "probability": 80,
                                     "frequency": (0.5, 2)},
                                    {"rule": "0 18 * * *", "probability": 50,
                                     "frequency": (4, 10)}
                                ])

## Devo-utils providers


The faker library has many data providers but they have to be instantiated explicitly in the devoutils.faker
TemplateParser class:

```
from .providers.file_data_source_provider import FileDataSourceProvider
from .providers.numbers_provider import NumbersProvider
from faker.providers.internet import Provider as InternetProvider

class TemplateParser:

    fake = None

    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(FileDataSourceProvider)
        self.fake.add_provider(NumbersProvider)
        # Ips networks emails etc..
        self.fake.add_provider(InternetProvider)
```

Right now lt-faker is configured to use two providers defined inside 
**FileDataSourceProvider** and **NumbersProvider** and a third provider from the third
party faker library: **InternetProvider**. If you want to add more add them there, the providers 
of the faker library ar located in the faker.providers.* path and there are a lot of them!.

You can use now in a template with `{{ fake.ipv4() }}`, `{{ fake.int(1, 65000) }}`

## Custom providers in script mode

In the fake generator, and in the templates you use, you can add any function / provider to generate data that you need, let's see a simple example

    from devoutils.faker import SyslogFakeGenerator
    from random import random # We import random function from python base
    ....
    con = Sender(config=config)
    with open("test_template.jinja2", 'r') as myfile:
        template = myfile.read()
        
    custom_providers = {"random" : random} # We need send all functions in a dictionary "name" -> function 

    sfg = SyslogFakeGenerator(engine=con, 
                              template=template, 
                              simulation=True,
                              probability=75,
                              frequency=(0.1, 5)
                              verbose=True,
                              providers=custom_providers)
    sfg.start()

And now we can use random function in template:

    {#- Log -#}
    {%- set type = fake.random_element(["post", "get"]) %}
    {%- set nextdate = next(date_generator) -%}
    {{ nextdate }} receiving {{ type }} request. Request duration: {{ random() }}


You can import full modules or one full class, and use it in Jinja like you use in python:

    from devoutils.faker import SyslogFakeGenerator
    import random # Now we import full random module
    ....
    con = Sender(config=config)
    with open("test_template.jinja2", 'r') as myfile:
        template = myfile.read()
        
    custom_providers = {"random" : random} 

    sfg = SyslogFakeGenerator(engine=con, 
                              template=template, 
                              simulation=True,
                              probability=75,
                              frequency=(0.1, 5)
                              verbose=True,
                              providers=custom_providers)
    sfg.start()

And now we can use all module in template:
    
    #- Log -#}
    {%- set type = fake.random_element(["post", "get"]) %}
    {%- set nextdate = next(date_generator) -%}
    {{ nextdate }} receiving {{ type }} request. Request duration: {{ random.random() }}. Request size {{ random.randint(0,100) }}

You can send the number of own providers that you want, you just have create/import the functions, put them 
in a dictionary and send them to "providers". 

    providers={"random": random, "wifi_ssd": random_ssd_provider, "names": random_names_provider}

## Third party providers
In the official Python Faker documentation you have a list of the providers included in the base package, 
and a list of providers created by other people:

* [Standar providers](https://faker.readthedocs.io/en/stable/providers.html)
* [Localized providers](https://faker.readthedocs.io/en/stable/locales.html#localized-providers)
* [Community providers](https://faker.readthedocs.io/en/stable/communityproviders.html)


## Important clarification in Jinja2

If you put a line with the block creator, after and before the %

    {%- set .... -%}

Faker will not treat that line as a line to send, only as a line with a variable, condition, etc. 

if a variable is created without the hyphens, for example:

    {% set myvar = 3 %}


As Faker not see the hyphens, the template use this line like one event, soo, one line to send. You need 
use ever the hyphens `-` to secure setters lines, or conditional lines, etc, are not send

