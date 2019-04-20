# md_to_dict

##### Convert Markdown into python dictionary

* Installation:
	`$ pip install -r requirements.txt`
* Usage:
	`$ python md_to_dict.py test.md`

* Usage in code:
```python
	from md_to_dict import MarkdownParser

	md_parser = MarkdownParser(path_to_file)
	md_dict = md_parser.parse()
```

### Example
#### Input

    # Vendor
    
    * Vendor name: test vendor
    * Vendor website: www.test.com
    
    # Data
    
    this text is ignored
    
    * Data Description: awesome stuff
    * Asset class: Equity
    
    ## subheading 

#### Output

```
{
	'data': {
		'asset_class': 'equity',
		'data_description': 'awesome_stuff'
	},
	'vendor': {
		'vendor_website': 'www.test.com', 
		'vendor_name': 'test_vendor'
	}
}

```