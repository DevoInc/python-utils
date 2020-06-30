# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2020-06-30
#### Added
 * Sorter now accept file encoding for write/read
 

## [3.0.0] - 2020-04-28
#### Added 
 * Faker
     * Faker time periods for probability and frequency
     * SimulationGenerator
     * New providers
     * New and splitted documentation of use
     * Examples for scripts and CLI shell
     * Generators/Faker now accept custom providers, custom functions 
     from base python or custom scripts for use in templates
     * CLI Shell has now all necessary flags for use all generators 
 
#### Changed
 * General
    * Modified base devo-sender from version 3.0.x to 3.3.0
    * Update dependencies to a new majors versions
    * Set dependencies to fixed versions (more maintenance, but much more security and reliability)
 * Sorter
    * file_sorted_join moved from devoutils.sorter to devoutils.fileio
    * Remove Python 2 compatibility
    * Sorter regex parser now accept group != 0
 * Faker
    * Faker cli add verbose mode to show the events in the console
    * Add file_name param to define a file to store events in batch mode or 
     for testing, store in a file but do not send it.
    * Generator template are moved for Template
    * Generator date_generator are moved for Template
    * Generators name changed, example: BatchSender for BatchFakerGenerator
    * Now you can make functions callable in each line of Faker Jinja2 Template
    * null_date_generator (Default date generator) isn't a generator now, its a normal function
    * Template.process() now not create new DateGenerator in each call
    * Numbers_providers has PEP8 variable names
    * `freq` var/flag in all code are now `frequency`
    * `prob` var/flag in all code are now `probability`
    * CLI Shell --config file now require all vars in "faker" object, and all vars for Sender in "sender" object


## [2.0.0] - 2019-07-02
#### Changed
 * Modified base devo-sender from version 2.x to >=3.0.1
 * Faker cli for adapt to new devo-sdk config files
 
#### Fixed
 * Problems with Sender raw sender in CLI removing tag
 * Problems with call key when can not exists

## [1.0.2] - 2019-04-24
#### Security
 * Updated requirements for high problems of security

## [1.0.1] - 2019-04-11
#### Fixed
 * Fixed problems with syslog_raw_sender in Faker when not "\n" at end of line sended
 
## [1.0.0] - 2019-02-22
#### Added
 * Requirements file
 * .pyup.yaml file for security dependencies bot

## [1.0.0] - 2019-01-16
#### Added
 * On the ninth month of the year, a Devo programmer finally decided to publish a part of the Utils and rest in peace.
