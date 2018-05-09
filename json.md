# JSON & Python

## JSON

[JSON (JavaScript Object Notation)](http://json.org/), specified by [RFC 7159]() (which obsoletes RFC 4627) and by ECMA-404, is a `lightweight data interchange` format inspired by [JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax (although it is not a strict subset of JavaScript).

### `JSON` is built on `two` structures:

* 1 A collection of `name/value` pairs. In various languages, this is realized as an `object`, `record`, `struct`, `dictionary`, `hash table`, `keyed list`, or `associative array`.


* An **ordered** `list` of values. In most languages, this is realized as an `array`, `vector`, `list`, or `sequence`.

###  In `JSON`, they take on these `forms`:

**1** An **object** is an `unordered` **set** of `name/value` pairs.

* An `object` begins with `{` (left brace) and ends with `}` (right brace).

* Each `name` is followed by `:` (colon) 

* The `name/value` pairs are `separated` by `, `(comma)

**2** An `array` is an `ordered` collection of **values**. 

* An array begins with `[` (left bracket) and ends with `]` (right bracket).

* Values are separated by `,` (comma).

**3** A `value` can be a `string` in double quotes, or a `number`, or `true` or `false` or `null`, or an `object` or an `array`. 

These structures can be `nested`.

**4** A **string** is a sequence of zero or more `Unicode` characters, wrapped in `double` quotes(`"`), using backslash escapes(`\`). 

A `character` is represented as a single character `string`. 

A string is very much like a `C` or `Java` string.

**5** A `number` is very much like a `C` or `Java` number, `except` that the `octal and hexadecimal` formats are not used.

## Example: the json file of Rankine81 object in step4-json: **rankine81.json** 

![rankine81](./step4/img/rankine81.jpg)


```json
{
    "name": "Rankine81",
    "nodes": [
        {
            "name": "Main Steam",
            "id": 0,
            "p": 8.0,
            "t": null,
            "x": 1,
            "fdot": 1
        },
        {
            "name": "Outlet Steam of HP",
            "id": 1,
            "p": 0.008,
            "t": null,
            "x": null,
            "fdot": null
        },
        {
            "name": "Condenser Water",
            "id": 2,
            "p": 0.008,
            "t": null,
            "x": 0,
            "fdot": null
        },
        {
            "name": "Main FeedWater",
            "id": 3,
            "p": 8.0,
            "t": null,
            "x": null,
            "fdot": null
        }
    ],
    "comps": [
        {
            "name": "Turbine",
            "type": "TURBINE-EX0",
            "eff": 100,
            "inNode": 0,
            "outNode": 1
        },
        {
            "name": "Condenser",
            "type": "CONDENSER",
            "inNode": 1,
            "outNode": 2
        },
        {
            "name": "Feedwater Pump",
            "type": "PUMP",
            "eff": 100,
            "inNode": 2,
            "outNode": 3
        },
        {
            "name": "Boiler",
            "type": "BOILER",
            "eff": null,
            "inNode": 3,
            "outNode": 0
        }
    ]
}
```


## Python3:19.2. json — JSON encoder and decoder

https://docs.python.org/3/library/json.html
