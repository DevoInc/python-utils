# Devo Faker
## Overview
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

## CLI
The command line allow us to call a template with a configuration in one
command, for example:
```
devo-faker -t template --config config.json -i
```
This command uses the template indicated with the configuration inside the
config.json file and makes the process interactive.

If you use ```devo-faker --help``` you can see all the available options.
Here is the help command result:
```
Usage: faker_cli.py [OPTIONS]

  Perform query by query string

Options:
  --config PATH                JSON File with the required configuration.
  -k, --key PATH               Key file for SSL.
  -c, --cert PATH              Cert file for SSL.
  -ch, --chain PATH            Chain file for SSL.
  --address TEXT               address to send.
  --port TEXT                  Port to send.
  --tag TEXT                   Tag from Devo.
  --file_name TEXT             File name to store events. If file name exist
                               will only store the events in a file. Can be
                               used with batch mode to set the file where
                               store the batch events
  --simulation                 Set as simulation. Shows the event in the
                               console, but do not send it
  -t, --template FILENAME      Template to send.  [required]
  -i, --interactive            Interactive mode.
  -raw, --raw_mode             Send raw mode.
  --prob INTEGER               Probability (0-100).
  --freq TEXT                  Frequency in seconds. Example:"1.0-5.0" =
                               random time between 1 sec. to 5secs.
  --batch_mode                 Enable blatch mode, a lot of events will be
                               generated as fast as possible and written to a
                               file. The events will be generated in thetime
                               range specified by the --date_range option
  --date_range <TEXT TEXT>...  batch mode: Date range where the logs will be
                               generated, default: the last 24 hours
  --date_format TEXT           (batch mode) Format of the generated dates.
                               default: "%Y-%m-%d %H:%M:%S.%f"
  --dont_remove_microseconds   (batch mode) By default the microseconds are
                               removed from the generated dates by doing
                               date[:-3] this flags prevents it
  --verbose                    Verbose mode shows the events created in the
                               console when sending dta into Devo.
  --help                       Show this message and exit.
```

The config.json file could be like this:
```
{
    "sender": {
        "key": "<path_to_key>.key",
        "cert": "<path_to_cert>.crt",
        "chain": "<path_to_chain>.crt",
        "tag": "test.keep.free",
        "address": "eu.elb.relay.logtrust.net",
        "port": 443
   }
}
```

## Batch mode tutorial

Sometimes we want to test a new application but we only have one
small file with some sample events. In this case we want to be able
to generate much more data from the original sample.

The batch mode allows to generate events between two arbitrary dates as fast 
as possible. The events will be dumped to the standard output and then you can
redirect it to a file or somewhere else

First we want to take the sample events and create a template from them. For
example, if we have these sample events:

```
<14>2018-03-22T23:56:09.237-07:00 ABCDEFGHI01 firewall.cisco_asa: 2018-03-22T23:56:09.237067-07:00 : %ASA-123456: Teardown dynamic UDP translation from inside:123.123.123.123/00001 to outside:111.111.111.111/11111 duration 0:02:32
<14>2018-03-22T23:56:09.076-07:00 ABCDEFGHI02 firewall.cisco_asa: 2018-03-22T23:56:09.076432-07:00 : %ASA-654321: Built inbound UDP connection 1234567890 for outside:123.123.123.123/00001 (111.111.111.111/00001)(LOCAL\Chocolatero, Paquito) to inside:1.1.1.1/11111 (0.0.0.0/11111) (Chocolatero, Paquito)
```

We have to identify the fields where we want to introduce some variation. In this
case we will generate different datetimes, hostnames, protocols, ips and ports. To
do that lt-faker integrates a library called faker that has many methods to generate
common data patterns such as street addresses, ips, etc..

The final template looks like this:

```
<14>{{next(date_generator)}} {{ fake.random_element(('ABCDEFGHI01', 'ABCDEFGHI02')) }} firewall.cisco.asa: 2018-03-22T23:56:09.237067-07:00 : %ASA-123456: Teardown dynamic {{ fake.random_element(('TCP', 'UDP', 'ICMP')) }} translation from inside:{{ fake.ipv4() }}/{{ fake.int(1, 65000) }} to outside:{{ fake.ipv4() }}/{{ fake.int(1, 65000) }} duration 0:02:32
<14>{{next(date_generator)}} {{ fake.random_element(('ABCDEFGHI01', 'ABCDEFGHI02')) }} firewall.cisco.asa: 2018-03-22T23:56:09.076432-07:00 : %ASA-654321: Built inbound {{ fake.random_element(('TCP', 'UDP', 'ICMP')) }} connection 1234567890 for outside:{{ fake.ipv4() }}/{{ fake.int(1, 65000) }} ({{ fake.ipv4() }}/{{ fake.int(1, 65000) }})(LOCAL\Chocolatero, Paquito) to inside:{{ fake.ipv4() }}/{{ fake.int(1, 65000) }} ({{ fake.ipv4() }}/{{ fake.int(1, 65000) }}) (Chocolatero, Paquito)
```

We have used these methods:
* datetime: We want sequential datetimes between the specified start_date and end_date, for this we
have to use the special command {{next(date_generator)}}
* hostnames: You can extract a list of hostnames from the original event sample or generate random ones, in
this case I extracted them from the original sample and converted them to this command:  
{{ fake.random_element(('ABCEFGHIJK', 'KJIHGFECBA')) }}
* protocols: The same as with hostnames: {{ fake.random_element(('TCP', 'UDP', 'ICMP')) }}
* ips: {{ fake.ipv4() }}
* ports: {{ fake.int(1, 65000) }}

Another very useful command to generate more realistic data is the following:
```
{{ fake.random_element({"%ASA-654321": 0.8, "%ASA-123456": 0.18, "%ASA-111111": 0.02}) }}
```
It allows to specify the probability of each element. 

The faker library has many data providers but they have to be instantiated explicitly in the devo-faker 
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

Right now lt-faker is configured to use two custom providers defined inside 
lt-faker **FileDataSourceProvider** and **NumbersProvider** and a third provider from the third
party faker library: **InternetProvider**. If you want to add more add them there, the providers 
of the faker library ar located in the faker.providers.* path and there are a lot of them!.


Now that the template is done you can generate the event file with the following command:

```
devo-faker -t /location/of/your_template 
    --batch_mode 
    --date_range "2018-02-01 00:00:00" "2018-02-05 00:10:00" 
    --freq 1-1000 
    --prob 50 > out.log
```

The generated logs will be located inside the **eventbatch.log** file.

You can use the **--freq** and **--prob** arguments to affect the way in which the events are generated.

**More template examples**

Reusing the eventdate in other parts of the log:
```
{%- set eventdate = next(date_generator) -%}
{{  eventdate }} {{ fake.ipv4() }} WEndpoint_Profile 1234567890 1 0 mac_address=10acbdefg01,ip_address={{ fake.ipv4() }},static_ip=t,hostname=DEVOHOSTNAME,username={{ 'USER%s' %fake.int(0, 9) }},login_status={{ fake.random_element({'ACCEPT': 0.4, 'REJECT': 0.1, 'TIMEOUT': 0.8}) }},error_code={{ fake.random_element((0, 106)) }}
```


## TODO
- Add more useful methods to the jinja collection
- Document news methods in Faker
- Provide use examples in script

