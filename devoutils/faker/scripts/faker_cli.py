# -*- coding: utf-8 -*-
"""Cli for launch faker options from shell"""
import datetime
import time
import sys
import os
import click
from dateutil import parser

# Commands
# ------------------------------------------------------------------------------
from devo.sender import Sender
from devo.common import Configuration
from devoutils.faker import BatchFakeGenerator, FileFakeGenerator, \
    SyslogFakeGenerator, SyslogRawFakeGenerator, SimulationFakeGenerator


@click.group()
def cli():
    """Empty group"""
    pass


@click.command()
@click.option('--config', type=click.Path(exists=True),
              help='JSON File with the required configuration.')
@click.option('--key', '-k', type=click.Path(exists=True),
              help='Key file for SSL.')
@click.option('--cert', '-c', type=click.Path(exists=True),
              help='Cert file for SSL.')
@click.option('--chain', '-ch', type=click.Path(exists=True),
              help='Chain file for SSL.')
@click.option('--address', help='address to send.')
@click.option('--port', help='Port to send.')
@click.option('--tag', help='Tag from Devo.')
@click.option('--simulation', is_flag=True,
              help='Set as simulation. Shows the event in the console, '
                   'but do not send it')
@click.option('--template', '-t', type=click.File('r'), required=True,
              help='Template to send.')
@click.option('--providers', '-p', type=click.File('r'), required=False,
              help='File with custom providers dict.')
@click.option('--interactive', '-i', is_flag=True,
              help='Interactive mode.')
@click.option('--raw_mode', '-raw', is_flag=True,
              help='Send raw mode.')
@click.option('--file_name', help='Use File Fake Generator.'
                                  'File name to store events. If file name '
              'exist will only store the events in a file. Can be used '
              'with batch mode to set the file where store the batch '
              'events')
@click.option('--probability', default=100, help='Probability (0-100).')
@click.option('--frequency', default="1-1", help='Frequency in seconds. '
                                                 'Example: '
                                                 '"1.0-5.0" = random time '
                                                 'between 1 sec. to 5secs.')
@click.option('--batch_mode', is_flag=True,
              help='Enable blatch mode, a lot of events will be generated as '
                   'fast as possible and written to a file. The events will be'
                   ' generated in thetime range specified by the --date_'
                   'range option')
@click.option('--date_range', type=(str, str),
              default=(str(datetime.datetime.now() -
                           datetime.timedelta(days=1)),
                       str(datetime.datetime.now())),
              help="batch mode: Date range where the logs will be generated, "
                   "default: the last 24 hours")
@click.option('--date_format', default="%Y-%m-%d %H:%M:%S.%f",
              help='(batch mode) Format of the generated dates. '
                   'default: "%Y-%m-%d %H:%M:%S.%f"')
@click.option('--dont_remove_microseconds', is_flag=True,
              help='(batch mode) By default the microseconds are removed '
                   'from the generated dates by doing date[:-3] '
                   'this flags prevents it')
@click.option('--verbose', is_flag=True,
              help='Verbose mode shows the events created in the console '
                   'when sending dta into Devo.')
def cli(**kwargs):
    """Perform query by query string"""
    engine, cfg = configure(kwargs)
    providers = None

    try:
        if "providers" in cfg.keys():
            provcfg = cfg.get("providers")
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                provcfg.get("module"),
                os.path.join(provcfg.get("path"),
                             provcfg.get("module") + ".py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            get_providers = getattr(module, provcfg.get("getter"))
            providers = get_providers()
            cfg.__delitem__("providers")
    except Exception as error:
        print_error("Error when loading Providers", show_help=False,
                    stop=False)
        print_error(error, show_help=False, stop=True)

    params = []
    click.echo("» Press Ctrl+C to stop the process «", file=sys.stderr)
    if cfg['interactive']:
        click.echo("» Interactive mode «")

    try:
        if cfg['simulation']:
            params.append('Simulation')
            thread = SimulationFakeGenerator(providers=providers, **cfg)
        elif cfg['batch_mode']:
            params.append('Batch mode')
            start_date = parser.parse(cfg['date_range'][0])
            end_date = parser.parse(cfg['date_range'][1])
            click.echo('Generating events between {} and {}'.format(start_date,
                                                                    end_date),
                       file=sys.stderr)
            thread = BatchFakeGenerator(start_date=start_date,
                                        end_date=end_date,
                                        providers=providers,
                                        **cfg)
        elif cfg['raw_mode']:
            scfg = cfg['sender']
            params.append('Host={0}:{1}'.format(scfg.get('address', None),
                                                scfg.get("port", None)))
            thread = SyslogRawFakeGenerator(engine=engine,
                                            providers=providers,
                                            **cfg)
        elif cfg.get('file_name', None):
            params.append('File Name {}'.format(cfg['file_name']))
            thread = FileFakeGenerator(providers=providers,
                                       **cfg)
        else:
            scfg = cfg['sender']
            params.append('Host={0}:{1}'.format(scfg.get('address', None),
                                                scfg.get("port", None)))
            params.append('Tag={0}'
                          .format(cfg.get('tag',
                                          scfg.get("tag", "my.app.faker.test")
                                          )
                                  )
                          )
            thread = SyslogFakeGenerator(engine=engine,
                                         **cfg)

        params.append('probability={0}'.format(cfg['probability']))
        params.append('frequency={0}'.format(cfg['frequency']))
        click.echo("» {0} «\n".format(', '.join(params)), file=sys.stderr)

        thread.daemon = True
        thread.start()

        while True:
            if not thread.is_alive():
                break
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        if engine is not None:
            engine.close()
        click.echo('\nReceived keyboard interrupt, quitting threads.\n')

# Utils
# ----------------------------------------------------------------------------


def configure(args):
    """For load configuration file/object"""

    if args.get('config'):
        config = Configuration(path=args.get('config'), section="faker")
        config.mix(dict(args))
    else:
        config = dict(args)

    if 'frequency' in config.keys() and isinstance(config.get("frequency"),
                                                   (str, bytes)):
        config['frequency'] = tuple([float(x)
                                     for x
                                     in config.get("frequency").split("-")])

    config['template'] = config['template'].read()

    # Initialize devo.sender with the config credentials but only
    # if we aren't in batch mode or simulation mode
    engine = None
    if not (config['batch_mode'] or config['simulation']
            or config.get('file_name', None)):
        try:
            if "sender" not in config.keys():
                config['sender'] = {'key': config.get('key', None),
                                    'chain': config.get('chain', None),
                                    'cert': config.get('cert', None),
                                    'address': config.get('address', None),
                                    'port': config.get('port', 443)}

            engine = Sender(config=config.get('sender'))
        except Exception as error:
            print_error(error, show_help=False)
            print_error("Error when loading devo sender configuration",
                        show_help=True)
    return engine, config


def print_error(error, show_help=False, stop=True):
    """Function for print errors"""
    click.echo(click.style(error, fg='red'), err=True)
    if show_help:
        click.echo("")
        click.echo(click.get_current_context().get_help())
    if stop:
        sys.exit(1)


if __name__ == '__main__':
    cli()
