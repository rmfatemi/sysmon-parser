import csv
import pandas
import sys
import commands
import re
import os

# Getting the input CSV file as an argument as well as the number of lines in it
output = commands.getoutput('wc -l ' + str(sys.argv[-1]))
num_lines, input_file = output.split()

# Droping unnecessary rows and columns out of the raw input data
raw_data = pandas.read_csv(input_file, delimiter='\r\n', engine='python')
raw_data.to_csv('processed.csv', header=None, index=False)


def getRule(str1):
    substrings = str1.split()
    rule = substrings[substrings.index('(rule:') + 1]
    rule = rule.split(')', 1)[0]
    rule = re.findall('[A-Z][^A-Z]*', rule)
    rule = rule[0] + ' ' + rule[1]
    return rule


def getDate(str1):
    substrings = str1.split()
    date = substrings[1]
    return date


def getTime(str1):
    substrings = str1.split()
    time = substrings[2]
    return time


def getHash(str1):
    substrings = str1.split(',')
    MD5 = substrings[0]
    MD5 = MD5.replace('Hashes: MD5=', '')
    MD5 = MD5.replace('Hash: MD5=', '')
    return MD5


def getCommandLine(str1):
    command = str1.replace('CommandLine: ', '')
    return command


def getGUID(str1):
    guid = str1.replace('ProcessGuid: {', '')
    guid = guid.replace('}', '')
    return guid


def getParentGUID(str1):
    parentguid = str1.replace('ParentProcessGuid: {', '')
    parentguid = parentguid.replace('}', '')
    return parentguid


def getLogonGUID(str1):
    logonguid = str1.replace('LogonGuid: {', '')
    logonguid = logonguid.replace('}', '')
    return logonguid


with open('processed.csv') as csvin, open('final.csv', mode='w') as csvout:
    processed_data = csv.reader(csvin)
    final_data = csv.writer(csvout)

    os.remove('processed.csv')

    header = ['Date', 'Time', 'Rule', 'MD5 Hash', 'Process GUID', 'Parent Process GUID',
              'Logon ID']  # , 'Command Line']
    final_data.writerow(header)

    event = [None] * len(header)

    for row in processed_data:

        str1 = ''.join(row)
        str1 = str1.replace('"', '')

        if ('UtcTime' in str1):
            event[0] = getDate(str1)
            event[1] = getTime(str1)

        elif ('(rule:' in str1):
            event[2] = getRule(str1)

        elif ('MD5=' in str1):
            event[3] = getHash(str1)

        elif (str1.startswith('ProcessGuid: {')):
            event[4] = getGUID(str1)

        elif (str1.startswith('ParentProcessGuid: {')):
            event[5] = getParentGUID(str1)

        elif (str1.startswith('LogonGuid: {')):
            event[6] = getLogonGUID(str1)

        # elif (str1.startswith('CommandLine: ')):
        #     event[7] = getCommandLine(str1)

        if (str1.startswith('Information') and event[0]):
            final_data.writerow(event)
