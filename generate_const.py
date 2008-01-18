#! /usr/bin/env python
# Last Change: Thu Nov 02 01:00 PM 2006 J

# David Cournapeau 2006

# TODO:
#   args with the header file to extract info from

from header_parser import get_dict, put_dict_file

def generate_enum_dicts(header = '/usr/include/samplerate.h'):
    # Open the file and get the content, without trailing '\n'
    hdct    = [i.split('\n')[0] for i in open(header, 'r').readlines()]

    # Get converters enum codes
    nameregex   = '(SRC_[\S]*)'
    src_conv    = get_dict(hdct, nameregex)

    ## Get endianness 
    #nameregex   = '(SF_ENDIAN_[\S]*)'
    #sf_endian   = get_dict(hdct, nameregex)

    ## Get command constants
    #nameregex   = '(SFC_[\S]*)'
    #sf_command  = get_dict(hdct, nameregex)

    ## Get (public) errors
    #nameregex   = '(SF_ERR_[\S]*)'
    #sf_errors   = get_dict(hdct, nameregex)

    # Replace dict:
    repdict = {
        '%SRC_CONV%' : put_dict_file(src_conv, '_src_conv')
    }

    return repdict
