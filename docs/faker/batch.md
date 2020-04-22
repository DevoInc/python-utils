## Batch fake generator

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
