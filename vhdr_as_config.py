
# coding: utf-8

# In[1]:


import configparser
from io import StringIO
import pandas as pd
import re


# In[2]:


with open('testdata/testdata0004.vhdr') as fin: cfgdat = fin.read()


# In[3]:


header, cfgdat = cfgdat.split('\n',1)


# In[4]:


header


# In[5]:


body, comment = cfgdat.split('[Comment]',1)


# In[6]:


config = configparser.ConfigParser()
config.optionxform = lambda option: option
config.read_string(body)


# In[7]:


def parse_channel(chstr):
    '''Parse channel info from VHDR file.'''

    name, reference, resolution, unit = chstr.split(',')

    return dict(name=name,
                reference=reference,
                resolution=float(resolution),
                unit=unit)
parse_channel(config["Channel Infos"]["Ch1"])


# In[8]:


vhdr = dict()
for section in config:
    vhdr[section] = dict(config[section])

vhdr['Common Infos']['NumberOfChannels'] = int(vhdr['Common Infos']['NumberOfChannels'])
vhdr['Common Infos']['SamplingInterval'] = int(vhdr['Common Infos']['SamplingInterval'])

for ch in vhdr['Channel Infos']:
    vhdr['Channel Infos'][ch] = parse_channel(vhdr['Channel Infos'][ch])

if "Coordinates" in vhdr:
    for ch in vhdr['Coordinates']:
        vhdr['Coordinates'][ch] = dict(zip(['r','phi','theta'], vhdr['Coordinates'][ch].split(',')))

vhdr


# In[9]:


split_comment = list(re.split("([=-]+)|\n\s*\n",comment,flags=re.MULTILINE))


# In[10]:


for s in split_comment:
    if s is not None and 'Phys. Chn.' in s:
        amplifier_info = s
        break
else:
    amplifier_info = None

pd.read_table(StringIO(amplifier_info),sep=r'\s{2,}',engine="python").head()


# In[11]:


for s in split_comment:
    if s is not None and 'Low Cutoff' in s and 'Phys. Chn.' not in s:
        filter_info = s
        break
else:
    filter_info = None

pd.read_table(StringIO(filter_info.strip()),sep=r'\s{2,}',engine="python").head()

