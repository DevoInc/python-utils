# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2019-10-17
#### Changed
 * Modified base devo-sender from version 3.0.x to 3.3.0
 * Faker cli add verbose mode to show the events in the console
 * Add file_name param to define a file to store events in batch mode or 
 for testing, store in a file but do not send it.

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
