# -*- coding: utf-8 -*-
"""Cli for launch faker options from shell"""
import datetime
import time
import sys
import click
from dateutil import parser

# Commands
# ------------------------------------------------------------------------------
from devo.sender import Sender
from devo.common import Configuration
from devoutils.faker import BatchSender, FileSender, SyslogSender, \
    SyslogRawSender


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
@click.option('--tag', help='Tag from Logtrust.')
@click.option('--simulation', is_flag=True, help='Set as simulation.')
@click.option('--template', '-t', type=click.File('r'), required=True,
              help='Template to send.')
@click.option('--interactive', '-i', is_flag=True,
              help='Interactive mode.')
@click.option('--raw_mode', '-raw', is_flag=True,
              help='Send raw mode.')
@click.option('--prob', default=100, help='Probability (0-100).')
@click.option('--freq', default="1-1", help='Frequency in seconds '
                                            '("1.0-5.0": 1 sec. to 5secs.).')
@click.option('--batch_mode', is_flag=True,
              help='Enable blatch mode, a lot of events will be generated as '
                   'fast as possible and written to a file. The events will be '
                   'generated in thetime range specified by the --date_'
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
def cli(**kwargs):
    """Perform query by query string"""
    engine, cfg = configure(kwargs)
    params = []

    click.echo("» Press Ctrl+C to stop the process «", file=sys.stderr)
    if cfg['interactive']:
        click.echo("» Interactive mode «")

    try:
        if cfg['simulation']:
            params.append('Simulation')

            thread = FileSender(cfg['template'],
                                interactive=cfg['interactive'],
                                prob=cfg['prob'], freq=cfg['freq'])
        elif cfg['batch_mode']:
            params.append('Batch mode')
            start_date = parser.parse(cfg['date_range'][0])
            end_date = parser.parse(cfg['date_range'][1])
            click.echo('Generating events between {} and {}'.format(start_date,
                                                                    end_date),
                       file=sys.stderr)
            thread = BatchSender(
                cfg['template'], start_date, end_date, prob=cfg['prob'],
                freq=cfg['freq'], date_format=cfg['date_format'],
                dont_remove_microseconds=cfg['dont_remove_microseconds'])
        elif cfg['raw_mode']:
            scfg = cfg['logtrust']
            params.append('Host={0}:{1}'.format(scfg['address'], scfg['port']))
            params.append('Tag={0}'.format(cfg['tag']))
            thread = SyslogRawSender(engine, cfg['template'],
                                     interactive=cfg['interactive'],
                                     prob=cfg['prob'], freq=cfg['freq'],
                                     tag=cfg['tag'])
        else:
            scfg = cfg['logtrust']
            params.append('Host={0}:{1}'.format(scfg['address'], scfg['port']))
            params.append('Tag={0}'.format(cfg['tag']))
            thread = SyslogSender(engine, cfg['template'],
                                  interactive=cfg['interactive'],
                                  prob=cfg['prob'], freq=cfg['freq'],
                                  tag=cfg['tag'])

        params.append('Prob={0}'.format(cfg['prob']))
        params.append('Freq={0}'.format(cfg['freq']))
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
# ------------------------------------------------------------------------------


def configure(args):
    """For load configuration file/object"""
    config = Configuration()
    if args.get('config'):
        config.load_config(args.get('config'))
    config.mix(dict(args))

    if 'freq' in config.cfg:
        parts = config.cfg['freq'].split('-')
        config.cfg['freq'] = (float(parts[0]), float(parts[1]))

    config.cfg['template'] = config.cfg['template'].read()

    # Initialize LtSender with the config credentials but only
    # if we aren't in batch mode or simulation mode
    engine = None
    if not (config.cfg['batch_mode'] or config.cfg['simulation']):
        try:
            if 'sender' in config.cfg:
                engine = Sender.from_config(config.get()['sender'])
            else:
                config.cfg['sender'] = {
                    'key' : config.cfg['key'],
                    'chain' : config.cfg['chain'],
                    'cert' : config.cfg['cert'],
                    'address' : config.cfg['address'],
                    'port' : config.cfg['port']
                }
                engine = Sender.from_config(config.cfg)
        except Exception as error:
            print_error(error, show_help=False)
            print_error("Error when loading devo sender configuration",
                        show_help=True)

    return engine, config.get()


def print_error(error, show_help=False, stop=True):
    """Function for print errors"""
    click.echo(click.style(error, fg='red'), err=True)
    if show_help:
        click.echo("")
        click.echo(click.get_current_context().get_help())
    if stop:
        sys.exit(1)

