# demo-snapshotter
Demo project to manage AWS EC2 instances snapshots

## About

this project is a demo, and uses boto3 to manage AWS EC2 insatnces snapshots.

## Configuring

demo_shotter uses the configuration file created by the AWS CLI:

`aws configure --profile shotter`

## Running

`pipenv run python shottter/shotter.py <command> <subcommand> <--proyecto=PROYECTO>`

*command* is instances, volumes or snapshots
*subcommand* - dependson command
*proyecto* is optional

