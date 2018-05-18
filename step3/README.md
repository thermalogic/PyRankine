# Rankine Cycle Representation

The first stage in the Rankine Cycle Simulator is to be able to generate a Rankine Cycle schematic.

A Rankine Cycle schematic should be able to describe the `nodes` and `components` present in a Rankine Cycle and also be able to describe how these components are `connected` to each other through `nodes`.

* 1 Rankine Cycle Representation as `.csv` filea

* 2 Rankine Cycle Representation as `JSON` file

* 3 Python: `json` — JSON encoder and decoder

## 1  Rankine Cycle Representation as a Comma Separated Value (.csv) file

A `Comma Separated Value (.csv)` file can be opened and edited in any `spreadsheet` software like any other spreadsheet.

In the .csv file, each `row` of the spreadsheet appears in a separate `line` and the `contents of the cells` in a row are separated by `commas`.

A `.csv` file is essentially a `text` file which can be edited  by any Text Editor


### The  Rankine Cycle is `drawn` in two `.csv` files 

* `nodes`:  

    The nodes would have `unique ID `(**NID**) for the nodes in the Rankine Cycle schematic

* `components`: `components` and how these components are `connected`  to each other through `nodes`.

   The components would have `unique symbols`(**TYPE**) for the components in the Rankine Cycle schematic

### Example: the CSV files of the Rankine Cycle 81 schematic

![rankine81](./img/rankine81.jpg)

CSV files of e Rankine Cycle 81 schematic 

* `nodes`: [rankine81-nds.csv](./step3-csv/rankine81-nds.csv)

* `components`: [rankine81-dev.csv](./step3-csv/rankine81-dev.csv)

![rankine81-nds](./img/rankine81-nds.png)

![rankine81-nds-sp](./img/rankine81-nds-sp.png)

![rankine81-dev](./img/rankine81-dev.png)

![rankine81-dev-sp](./img/rankine81-dev-sp.png)

## 2 Rankine Cycle Representation as a JSON file

[JSON (JavaScript Object Notation)](http://json.org/), specified by [RFC 7159]() (which obsoletes RFC 4627) and by ECMA-404, is a `lightweight data interchange` format inspired by [JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax (although it is not a strict subset of JavaScript).

### `JSON` is built on `two` structures:

* 1 A collection of `name/value` pairs. In various languages, this is realized as an `object`, `record`, `struct`, `dictionary`, `hash table`, `keyed list`, or `associative array`.


* 2 An **ordered** `list` of values. In most languages, this is realized as an `array`, `vector`, `list`, or `sequence`.

###  In `JSON`, they take on these `forms`

#### 1 An `object` is an `unordered` set of `name/value` pairs.

* An `object` begins with `{` (left brace) and ends with `}` (right brace).

* Each `name` is followed by `:` (colon) 

* The `name/value` pairs are `separated` by `, `(comma)

### 2 An `array` is an `ordered` collection of **values**

* An array begins with `[` (left bracket) and ends with `]` (right bracket).

* Values are separated by `,` (comma).

#### 3 A `value` can be a `string` in double quotes("), or a `number`, or `true` or `false` or `null`, or an `object` or an `array`

These structures can be **nested**.

#### 4 A **string** is a sequence of zero or more `Unicode` characters, wrapped in `double` quotes(`"`), using backslash escapes(`\`)

A `character` is represented as a single character `string`. 

A string is very much like a `C` or `Java` string.

#### 5 A `number` is very much like a `C` or `Java` number, `except` that the `octal and hexadecimal` formats are not used.

### The  Rankine Cycle is `drawn` in the json  files 

* `nodes`

  The nodes would have `unique ID `(**id**) for the nodes in the Rankine Cycle schematic

* `components`

   The components would have `unique symbols`(**type**) for the components in the Rankine Cycle schematic

###  Example: the json file of the Rankine Cycle 81 schematic 

![rankine81](./img/rankine81.jpg)


the json file of the Rankine Cycle 81 schematic: **rankine81.json**

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

## 3 Python3:19.2. json — JSON encoder and decoder

https://docs.python.org/3/library/json.html
