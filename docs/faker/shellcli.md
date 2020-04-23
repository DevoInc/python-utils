## CLI
The command line allow us to call a template with a configuration in one
command, for example:
```
devo-faker -t template --config config.json -i
```

Or all in config file
```
devo-faker --config config.json
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
  -p, --providers FILENAME     File with custom providers dict.
  -i, --interactive            Interactive mode.
  -raw, --raw_mode             Send raw mode.
  --probability INTEGER        Probability (0-100).
  --frequency TEXT             Frequency in seconds. Example: "1.0-5.0" =
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
   },
    "verbose": true,
    "probability": 80,
    "frequency": (2,4)
}
```

config.yaml its available too:
```
sender:
    key: "<path_to_key>.key",
    cert: "<path_to_cert>.crt",
    chain: "<path_to_chain>.crt",
    tag: "test.keep.free",
    address: "eu.elb.relay.logtrust.net",
    port: 443
simulation: true
probability: 50
frequency: (1,3)
providers: providers.py
```
