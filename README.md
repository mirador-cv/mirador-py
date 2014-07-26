# Mirador-Py [![Build Status](https://drone.io/github.com/mirador-cv/mirador-py/status.png)](https://drone.io/github.com/mirador-cv/mirador-py/latest)

A python client for the Mirador [Image Moderation API](http://mirador.im). To get started, you will need an API Key, available at [mirador.im](http://mirador.im). For questions about keys or support with this module please email support@mirador.im.

## Installation

The module is available [on pypi](https://pypi.python.org/pypi/Mirador), and can be installed with pip:

```shell
pip install mirador
```

## Getting started: command-line tool

There's a command-line tool included in, which should show up as `mirador-client` in your `PATH`. It takes in a file(s) of ids and urls and outputs html showing the result:

```shell
echo "baby-1  http://demo.mirador.im/test/baby.jpg" > test.urls
mirador-client -k your_api_key test.urls > test.html
open test.html
```

## Mirador python module

The python module has a simple interface in `mirador.MiradorClient`, documented here.

### `mirador.MiradorClient(api_key)`

The client supports classification of either images or files, where files can be filenames or file-objects.

### `MiradorClient#classify_files(files) => MiradorResultList<MiradorResult>`

Here, files can be a list of filenames or file objects, or a dict of `{ id: filename/filehandle }`, if you want to have a different `MiradorResult.id` on the results than the filename itself.

### `MiradorClient#classify_urls(urls) => MiradorResultList<MiradorResult>`

Same as with files, you can either pass a list and use the urls as ids, or pass a dict and specify your own ids.

### `MiradorClient#classify_raw(buffers) => MiradorResultList<MiradorResult>`

Here you need to pass a dict `{ id: buffer }`, so you can identify the results later.


## `mirador.MiradorResultList`

The result list allows for dict-access of the results and some better extended-dict functionality, also provides more backwards-compatibility to earlier versions of the API.

Basic methods:

### `MiradorResultList#__getitem__(request_id)`

You can get responses by the id you assigned when you called classify

### `MiradorResultList#__iter__`

Provides a list-like iterator on the actual `MiradorResult` objects

## `mirador.MiradorResult`

This has the following properties (it's pretty simple):

* `id` - (String) the id you passed in or the assumed value
* `value` - (float) the rating given by the API (0 = totally safe, 1.0 = totally unsafe)
* `safe` - (boolean) true = is safe, false = unsafe (NSFW/pornographic)
