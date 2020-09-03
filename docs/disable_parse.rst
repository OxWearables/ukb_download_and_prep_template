# Disabling parsing
If for some reason you don't want to automatically parse the field ID and/or the categorical codes, you can explicitly set the keys `name` and/or `replace_values` to `None`. For example,

```
{
    # ...

    "1558-0.0":{
        "name": None,
        "replace_values": None,
    },

    # ...
}
```
will leave the column untouched:
| 1558-0.0 |
|----------|
| 2        |
| 5        |
| 4        |
| 4        |
| 1        |
| 6        |
| ...      |

