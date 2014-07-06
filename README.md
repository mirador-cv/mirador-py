# Mirador-Py
A python client for the Mirador [Image Moderation API](http://mirador.im). To get started, you will need an API Key, available at [mirador.im/join](http://mirador.im/join). For questions about keys or support with this module please email support@mirador.im.

## Installation

The module is available [on pypi](https://pypi.python.org/pypi/Mirador), and can be installed with pip:

```shell
pip install mirador
```

## Getting started: command-line tool

For command-line use, the package installs a script called `mirador-client` that will be added to your path. For usage please enter `mirador-client -h`, basic usage is:

```shell
$ mirador-client -k YOUR_API_KEY images/*.{jpg,png}`
```

In this example, we are classifying all of the images in the `images` directory on your computer. URLs can be specified on the command line, although be careful to escape them in quotes (so that characters aren't interpreted by your shell)


## Mirador python module

The python module has a simple interface in `mirador.MiradorClient`, documented here.


### `mirador.MiradorClient(api_key)`

The client supports classification of either images or files, where files can be filenames or file-objects.

#### `MiradorClient.classify_files(*files) -> [MiradorResult]`

Example code:

```python
from mirador import MiradorClient

mc = MiradorClient('your_key_here')
fh = open('pic3.jpg', 'rb')

for res in mc.classify_files('pic1.jpg', 'pic2.jpg', fh):
    print "{name}, {safe}, {value}".format(**res.__dict__)
```

Here you can see that the `MiradorResult` object has 3 fields:

* `MiradorResult.name` - the url or filename used in the request
* `MiradorResult.safe` - (boolean) indicated if image is 'flagged' by API
* `MiradorResult.value` - (float) value 0.0 - 1.0 indicated confidence of decision

#### `MiradorResult.classify_urls(*urls) -> [MiradorResult]`

This has an indentical inteface to `classify_files`, except it expects http/https urls.

```python
from mirador import MiradorClient

mc = MiradorClient('your_key_here')

for res in mc.classify_files('http://example.com/pic2.jpg', 'http://example.com/pic3.jpg'):
    print "{name}, {safe}, {value}".format(**res.__dict__)
```


## Extensions & Integrations

We are in the process of providing extensions and integrations into common frameworks. This package contains an experimental django integration. It is highly advised against use right now, although the code is located in [ext/django.py](mirador/ext/django.py), if you want to take a look.
