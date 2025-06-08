"""
Interface with [shabda](https://github.com/ilesinge/shabda) for audio samples
and text speech.

### `samples(definition: str)`

Fetch random samples from [freesound](https://freesound.org/)

Any word can be a pack definition. If you want more than one sample,
separate words by a comma: `"blue,red"`

You can define how many variations of a sample to assemble by adding a colon
and a number.
e.g. blue,red:3,yellow:2 will produce one 'blue' sample, three 'red' samples
and two 'yellow' sample.

Examples:

>>> samples('bass:4,hihat:4,rimshot:2')

will print in the terminal when finished downloading

>>> s1 >> loop('bass', dur=PDur(3,8), sample=2)
>>> s2 >> loop('hihat', dur=10, sus=2)
>>> s3 >> loop('rimshot', dur=PDur(7,9)*8, sample=2)

### `speech(words: str, language: str = 'en-GB', gender: str = 'f')`

Generate Text-to-Speech samples.

If you want more than one sample, separate words by a comma: `"hello,bye"`
If you want a sentence, separate it with `_`: `"eita_carai,oi"`

By default the language is `en-GB` but you can change this.

The gender of the voice unfortunately can be `f` and `m`.

If you only want to change the gender, use the following syntax

>>> speech('baby', gender='m')

Examples:

>>> speech('what')
>>> speech('voa,ai','pt-BR')
>>> speech('eita_carai,continua','pt-BR','m')

will print in the terminal when finished downloading

>>> v1 >> loop('eita_carai', dur=4, pan=[-5,0,1,0])
>>> v2 >> loop('voa', dur=PDur(3,8), pan=[0,1,0,-5])
>>> v3 >> loop('ai', dur=4, pan=[1,0,-5,0])
>>> v4 >> loop('continua', dur=var([PDur(3,8), 6], [7,1]), pan=[0,1,0,-5])
>>> v5 >> loop('what', dur=8, sus=2, pan=[0,1,0,-5])
"""

import json
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, urlretrieve
from threading import Thread

from .Settings import FOXDOT_LOOP

SHABDA_URL = os.getenv('SHABDA_URL', 'https://shabda.ndre.gr/')
SAMPLE_URL = SHABDA_URL + '{}.json?{}'
LOOP_PATH = Path(FOXDOT_LOOP)


def retrieve(url, path):
    try:
        urlretrieve(url, path)
    except HTTPError as error:
        print(f'Error when downloading the sample: \n\t{error=}\n\t{url=}')
    else:
        print(f'sample downloaded: {path}')

def download(base_url, sample, sounds):
    sample_dir = LOOP_PATH / sample
    if sample_dir.exists():
        shutil.rmtree(sample_dir)

    os.makedirs(sample_dir, exist_ok=True)
    with ThreadPoolExecutor() as pool:
        for sound in sounds:
            sound_path = sample_dir / Path(sound).name
            pool.submit(retrieve, f'{base_url}{sound}', sound_path)


def get_sample_list(definition, params):
    samples_map = SAMPLE_URL.format(definition, urlencode(params))
    with urlopen(samples_map) as response:
        return json.load(response)


def generate(definition, params=None):
    params = params or {}
    params['strudel'] = 1
    data = get_sample_list(definition, params)
    down = partial(download, data.pop('_base', SHABDA_URL))

    with ThreadPoolExecutor() as pool:
        for sample, list_sounds in data.items():
            pool.submit(down, sample, list_sounds)


def samples(definition):
    """
    Fetch random samples from freesound.org based on given words.

    Parameters
    ----------
    definition : str
        The sound pack definition:
          comma separated words with optional sample number.
          e.g. blue:2,red:4

    Examples
    --------
    >>> samples('bass:4,hihat:4,rimshot:2')

    """
    print('Starting the samples download')

    Thread(target=generate, args=(definition,), daemon=True).start()


def speech(words, language='en-GB', gender='f'):
    """
    Generate Text-to-Speech samples.

    Parameters
    ----------
    words : str
        Words to speech.
    language : str, default='en-GB'
        Language to use.
    gender : str, default='f'
        Voice gender..

    Examples
    --------
    >>> speech('vai,voa','pt-BR')

    """
    print('Starting the samples download')

    definition = f'speech/{words}'
    params = {'gender': gender, 'language': language}
    Thread(target=generate, args=(definition, params), daemon=True).start()
