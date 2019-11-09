# awscredansible
Use AWS resources from outside of AWS with Ansible

## Files
AWScre.py      - module, can be run as script
test_awscre.py - unit tests

## What is the problem?
Ansible on AWS can use server roles to very conveniently run playbooks with access to AWS resources
Or if it’s from a “home” account, AWS creds in files work just fine.
But ansible running remotely on non AWS (ie on prem, GCP, Oracle Cloud etc) then getting the credentials loaded can be a problem

## How it works
### Step one, ensure local creds in file
Some credentials should already exist on your local host in the ~/.aws/credentials file.  All you have to do is convert those credentials into a format that ansible can load.

Ansible AWS module is based on [boto3][1] and so will honour environment variables AWS_SECRET_KEY_ID and AWS_ACCESS_KEY_ID.  Ansible can load variable files into environment variables: this  is path I’ve taken

The file format in ~/.aws/credentials is like this

    [default]
    aws_access_key_id = AKIAXEX5OPTQQLXUAVL5
    aws_secret_access_key = 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

    [admin-account]
    aws_secret_access_key = mzTh1Sj9Btjxucbq//X6Ece1z6U6XE3Cysb+Ntdm
    aws_access_key_id = ASIAXEX3PUBILNYIJHAY
    aws_session_token = sXiACeiyqiPpd5z2wAHvEtmTR7/GGf88yVCJ/epz3StU2cU0y1SJUKo6+gch
    2YSsldTlsZzDEBSDubzGKtYur6rmzYZfq+v+KwrUbGobETwn1gvaNd4vg+kEaCg6eNhICisCMRHjrLfK
    YdaikcP9SbUSqQPHwew/F5rtzyWwU5pEle+8uHfYycwY1sSHWOn4bnBA9IpiiJDonTKdnPjWdwuep2E9
    pf7A3fxaPOCb+jss9CoI9YfzPLQ9CQSztqfdhqN4PxYvpXnLSms3Z6SB7cS


The format needed for ansible is

    ---
    env_vars:
    AWS_SECRET_ACCESS_KEY: mzTh1Sj9Btjxucbq//X6Ece1z6U6XE3Cysb+Ntdm
    AWS_ACCESS_KEY_ID: ASIAXEX3PUBILNYIJHAY
    AWS_SESSION_TOKEN: sXiACeiyqiPpd5z2wAHvEtmTR7/GGf88yVCJ/epz3StU2cU0y1SJUKo6+gc
    h2YSsldTlsZzDEBSDubzGKtYur6rmzYZfq+v+KwrUbGobETwn1gvaNd4vg+kEaCg6eNhICisCMRHjrLf
    KYdaikcP9SbUSqQPHwew/F5rtzyWwU5pEle+8uHfYycwY1sSHWOn4bnBA9IpiiJDonTKdnPjWdwuep2E
    9pf7A3fxaPOCb+jss9CoI9YfzPLQ9CQSztqfdhqN4PxYvpXnLSms3Z6SB7cS



AWScre.py will do this conversion

### Step 2, run the AWScre
To use the program call it  with 3 parameters
The credentials file path, usually $HOME/.aws/credentials
An output path to be used later by ansible, for example awsvars.yml
The account that is being used, for example ‘admin-account’

The output path should be in the ansible directory so that it is available on the remote host

### Step 3, use in Ansible playbooks
Next, add a ``vars_file`` directive to load the file you just made.  Add this to the playbook that needs to use AWS from GCP, like this

    ---

    - hosts: all
    gather_facts: yes
    become: yes
    become_user: root
    vars_files:
        - ../awsvars.yml
    environment: "{{ env_vars }}"

The python script I’ve written to setup the AWS credentials also makes a tweak to the sudo settings on the remote to ensure that the variables are exported during the “become_user”.  So the output file that is used by ansible actually looks like this

    ---
    env_vars:
    ANSIBLE_BECOME_FLAGS: '-H -S -n -E'
    AWS_SECRET_ACCESS_KEY: mzTh1Sj9Btjxucbq//X6Ece1z6U6XE3Cysb+Ntdm
    AWS_ACCESS_KEY_ID: ASIAXEX3PUBILNYIJHAY
    AWS_SESSION_TOKEN: sXiACeiyqiPpd5z2wAHvEtmTR7/GGf88yVCJ/epz3StU2cU0y1SJUKo6+gc
    h2YSsldTlsZzDEBSDubzGKtYur6rmzYZfq+v+KwrUbGobETwn1gvaNd4vg+kEaCg6eNhICisCMRHjrLf
    KYdaikcP9SbUSqQPHwew/F5rtzyWwU5pEle+8uHfYycwY1sSHWOn4bnBA9IpiiJDonTKdnPjWdwuep2E
    9pf7A3fxaPOCb+jss9CoI9YfzPLQ9CQSztqfdhqN4PxYvpXnLSms3Z6SB7cS


How well does it work?  Transferring software artifacts held in s3 from AWS to GCP was as fast as you’d expect, a few seconds for hundreds of MB

[1]: https://aws.amazon.com/sdk-for-python/
