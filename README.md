# md_to_dict

##### Convert Markdown into python dictionary

* Installation:
	`$ pip install -r requirements.txt`
* Usage:
	`$ python md_to_dict.py test.md`

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