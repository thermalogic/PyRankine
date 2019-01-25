# Step3: Basic Object-Orientation Abstraction and Textual Representation of  Rankine Cycle

Object-oriented Programming

JSON file of Rankine Cycle Flowsheet

**Running:**
```bash
python rankine.py
```

## Example Rankine Cycles

Michael J. Moran, Howard N. Shapiro, Daisie D. Boettner, Margaret B. Bailey. Fundamentals of Engineering Thermodynamics(7th Edition). John Wiley & Sons, Inc. 2011

Chapter 8 : Vapour Power Systems 

* [EXAMPLE 8.1: Analyzing an Ideal Rankine Cycle, P438](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82-Step0-1.ipynb)

    * [Ideal Rankine Cycle of OOP](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-Step2.ipynb)

## The `JSON` File of Rankine Cycle Flowsheet

The importmant stage in the Rankine Cycle Simulator is to build the Textual Representation of Rankine Cycle Flowsheet.

We use `JSON` format for the Textual Representation Rankine of Cycle Flowsheet

The `JSON` files of Rankine Cycle Flowsheet describe the `nodes` and `components` present in a Rankine Cycle and describe how these components are `connected` to each other through `nodes`.

## JSON

[JSON (JavaScript Object Notation)](http://json.org/), specified by [RFC 7159]() (which obsoletes RFC 4627) and by ECMA-404, is a `lightweight data interchange` format inspired by [JavaScript](https://en.wikipedia.org/wiki/JavaScript) object literal syntax (although it is not a strict subset of JavaScript).

The [EXAMPLE 8.1: Analyzing an Ideal Rankine Cycle, P438](http://nbviewer.jupyter.org/github/PySEE/PyRankine/blob/master/notebook/RankineCycle81-82-Step0-1.ipynb) is used as the example to show the forms of `JSON` items 

![rankine81](./img/rankine81.jpg)

### `JSON` is built on `two` structures:

* 1 A collection of **name/value** pairs. 

   In various languages, this is realized as an `object`, `record`, `struct`, `dictionary`, `hash table`, `keyed list`, or `associative array`. **Python: dictionary**

* 2 An **ordered list** of values.

    In most languages, this is realized as an `array`, `vector`, `list`, or `sequence`. **Python: list**

#### 1 An `object` is an `unordered` set of **name/value** pairs.

* An `object` begins with `{` (left brace) and ends with `}` (right brace).

* **name/value** pairs.

   * The **name/value** pairs are `separated` by `, `(comma)

   * Each `name` is followed by `:` (colon) 

   *  The `value` can be a `string` in double quotes("), or a `number`, or `true` or `false` or `null`, or an `object` or an `array`，These structures can be **nested**.
      
      * The **string** is a sequence of zero or more `Unicode` characters, wrapped in `double` quotes(`"`), using backslash escapes(`\`)

        * The `character` is represented as a single character `string`. 

      * A `number` is very much like a `C`number, `except` that the `octal and hexadecimal` formats are not used.

The json object of node 0
```json
       {
            "name": "Main Steam",
            "id": 0,
            "p": 8.0,
            "t": null,
            "x": 1,
            "fdot": 1
        }
```
#### 2 An `array` is an `ordered` collection of **values**

* An array begins with `[` (left bracket) and ends with `]` (right bracket).

* Values are separated by `,` (comma).

The json array of node 0,1
```json
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
        }
   ]   
```

## The  Rankine Cycle is `drawn` in the json  files 

The Python Object of Rankine Cycle

```python   
{ 'name': 'NameString',
  'nodes':[{'name':None,'id':None,'p':None,'t':None,'x':None,'fot':None}],
  'comps':[{'name':None,'type':None,'inNode':None,'outNodet':None,...}]
}   
```

* `nodes` array

  The nodes array would have `unique ID `(**id**) for the nodes in the Rankine Cycle Flowsheet

* `components` array

   The components would have `unique symbols`(**type**) for the components in the Rankine Cycle Flowsheet

### the `JSON` representation of the Rankine Cycle 81 Flowsheet

the json file of the Rankine Cycle 81 Flowsheet: **rankine81.json**

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
            "inNode": 2,
            "outNode": 3
        },
        {
            "name": "Boiler",
            "type": "BOILER",
            "inNode": 3,
            "outNode": 0
        }
    ]
}
```

## Reference

* [Python3: json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)