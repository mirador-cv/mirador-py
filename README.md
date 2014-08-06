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
## Classifying Files

The python client supports working with a number of data types:

* file objects (e.g, `x` where `x = open('myfile.png', 'r')`) [classify_files](#classify_files)
* filenames [classify_files](#classify_files)
* data uris (e.g., data:image/png;base64,eehlk3jr;q3lfhf;eaef==) [classify_data_uris](#classify_data_uris)
* file buffers (e.g., `x` where `x` = open('myfile.png', 'r').read()`) -- useful for form uploads [classify_buffers](#classify_buffers)

Every method has an associated single-request method, e.g., [classify_file](#classify_file) for classify_files. These have a similar interface but only support processing of one item at a time.

### <a name='classify_files'></a> mirador.MiradorClient#classify_files

All classification methods share an identical interface that allows for generally flexible input. The mirador API, and the `mirador.MiradorResultList` object returned by the API allow for the attribution of an arbitrary identifier to your requests, to make post-processing of results easier. However, in cases where you do not specify an ID, the client will choose one (in a way that generally makes sense). For more information on the format of results, please see the documentation on [mirador.MiradorResultList](#result-list).

The simplest way to classify files is by filename:

```python
import mirador

client = mirador.MiradorClient('your_api_key')
results = client.classify_files('nsfw.jpg', 'sfw.jpg')

# since no id was specified, the requests are given the filenames as ids:
print results['nsfw.jpg'].safe 
print results['sfw.jpg'].safe
```

Alternatively, you can specify an id by passing in a dictionary of id: item mappings, or by using kwargs (as in a `dict()` constructor):

```python
# these are equivalent
results = client.classify_files({'nsfw': 'nsfw.jpg', 'sfw': 'sfw.jpg'})
results = client.classify_files(nsfw='nsfw.jpg', sfw='sfw.jpg')
```

#### <a name='using-file-objects'></a> Using File Objects

You can also pass file or file-like objects (that have a `read()` method and `.name` property, e.g., a `BytesIO`) using either format:

```python
# the id will be item.name, so in this case, the filenames will be the ids
results = client.classify_files(open('nsfw.jpg', 'r'), open('sfw.jpg', 'r'))

# same request, specifying ids
results= client.classify_files(nsfw=open('nsfw.jpg', 'r'), sfw=open('sfw.jpg', 'r'))
```

To pass an already-read file (a buffer), use [classify_buffers](#classify_buffers)

#### <a name='classify_file'></a> mirador.MiradorClient#classify_file

As in the other classification methods, classify_files has a corresponding single-request method, classify_file. This can be used with the same interface as its multiple-request sibling:

```python
nsfw = client.classify_file('nsfw.jpg')
print nsfw.id # "nsfw.jpg"

nsfw = client.classify_file({'nsfw': 'nsfw.jpg'})
print nsfw.id # 'nsfw'

nsfw = client.classify_file(nsfw='nsfw.jpg')
print nsfw.id # 'nsfw'
```

### <a name='classify_buffers'></a> mirador.MiradorClient#classify_buffers

This has an identical usage/interface to [classify_files](#classify_files), except that instead of passing in filenames or file objects, you only provide already-read buffers.

When not explicitly specifying an ID, the client uses the index of the item in the parameters, since we can't derive a name from a file buffer:

```python
import mirador

client = mirador.MiradorClient('your_api_key')

responses = client.classify_buffers(open('nsfw.jpg', 'r').read(), open('sfw.jpg', 'r').read())
print responses[0].safe # False
print responses[1].safe # True
```

For this reason, when working with buffers, it's best to specify an id (if you can):

```python
import mirador

client = mirador.MiradorClient('your_api_key')

responses = client.classify_buffers(nsfw=open('nsfw.jpg', 'r').read(), sfw=open('sfw.jpg', 'r').read())

print responses['nsfw'].value # 0.99
print responses['sfw'].safe # True
```

#### <a name='classify_buffer'></a> mirador.MiradorClient#classify_buffer

This is a simple helper when only classifying one buffer, it returns a `mirador.MiradorResult` object directly, instead of a `mirador.MiradorResultList`. The interface is otherwise identical to classify_buffers:

```python
nsfw_result = client.classify_buffer(open('nsfw.jpg', 'r').read())
nsfw_result = client.classify_buffer(nsfw=open('nsfw.jpg', 'r').read())
```

### <a name='classify_data_uris'><a> mirador.MiradorClient#classify_data_uris

This method exists as a convenience for simplified client-server communication when using clients that work with data uris (e.g., in web applications). For example, given this javascript (using jQuery to be concise):

```javascript

$('#form-field').on('change', function (e) {
  var file = this.files[0],
      reader = new FileReader();

  reader.onload = function (e) {
    $.post('/proxy/mirador', { id: file.name, data: e.target.result }).done(function (res) {
      console.log(res);
    });
  };

  reader.readAsDataURL(file);
});
```

We could handle that request on the server with this code:

```python
import mirador
from flask import Flask, jsonify

app = Flask(__name__)
mc = mirador.MiradorClient('your_api_key')

@app.route('/proxy/mirador', methods=('POST',))
def proxy_image():

  id = request.form['id']
  data = request.form['data']

  return jsonify(
      **client.classify_data_uri(id=data).__dict__))


if __name__ == '__main__':
    app.run()

```

This example shows the singular, `classify_data_uri`, however, the multiple -- `classify_data_uris`, has an identical interface.


## <a name='classifying-urls'></a> Classifying Urls

There are a couple of requirements to be mindful of when classifying urls, they must meet the following criteria:

* be publically-accessibly
* have a correctly set mimetype (`image/*`)
* respond/be retrievable in less than `mirador.MiradorClient.TIMEOUT` seconds
* not require query paramters

Given that, the interface for classifying urls is identical to that when using [classify_files](#classify_files)

### <a name='classify_urls'></a> mirador.MiradorClient#classify_urls

Since urls are text and are generally short, our client uses the url as an id by default:

```python
import mirador

client = mirador.MiradorClient('your_api_key')

results = client.classify_urls('http://static.mirador.im/test/nsfw.jpg', 'http://static.mirador.im/test/sfw.jpg')
print results['http://static.mirador.im/test/nsfw.jpg']

```

However, as with classifying files, an id can be specified either through keyword arguments or a dictionary:

```python

# these are equivalent
results = client.classify_urls(nsfw='http://static.mirador.im/test/nsfw.jpg', sfw='http://static.mirador.im/test/sfw.jpg')
print results['nsfw']

results = client.classify_urls({'nsfw': 'http://static.mirador.im/test/nsfw.jpg', 'sfw': 'http://static.mirador.im/test/sfw.jpg'})
print results['nsfw']

```

#### <a name='classify_url'></a> mirador.MiradorClient#classify_url

As with the other methods/data types, you can also classify a single url using the convenience function `classify_url`. This will return a mirador.MiradorResult object:

```python
nsfw_result = client.classify_url('http://static.mirador.im/test/nsfw.jpg')

nsfw_result = client.classify_url(nsfw='http://static.mirador.im/test/nsfw.jpg')
print nsfw_result.id # "nsfw"
```

## <a name='result'></a> mirador.MiradorResult

The `MiradorResult` object reprents the classification result for a single image/url. It has the following properties:

* `id` `[string|int]` - a unique identifier for the result
* `safe` `[boolean]` - indicates if an image contains adult content.
* `value` `[float 0.0-1.0]` - the likelyhood that the image does contain adult content (for implementing a custom threshold)
* `name` `[string]` **DEPRECATED** - maps to `id`

This object contains a helper `to_json` method, along with `__str__` and `__repr__` overrides that provide easy visual access to information about the result.

## <a name='result-list'></a> mirador.MiradorResultList

The purpose of the result list (over a built-in `list`) is to allow for indexing by a Result's `id`, which can be achieved through regular bracket syntax. You can iterate the `MiradorResultList` object as a `dict`:

```python

results = client.classify_files('test1.jpg', 'test2.jpg')
results['test1.jpg'] # MiradorResult

for id, result in results:
    print "{}, {}".format(id, type(result)) # test1.jpg, MiradorResult

```

The `MiradorResultList` object also has a `__len__` override so you can easily check how many results you have received.

## Contributing / Issues

Please submit any issues as issues [here on github](http://github.com/mirador-cv/mirador-py/issues), feel free to submit a pull request, or for immediate support, contact us at support@mirador.im.
