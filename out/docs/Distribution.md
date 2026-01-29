# Distribution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**sub_type** | **str** |  | 
**var_date** | **str** |  | 
**re_release** | **bool** |  | 
**country** | [**Country**](Country.md) |  | 
**companies** | [**List[Company]**](Company.md) |  | 

## Example

```python
from openapi_client.models.distribution import Distribution

# TODO update the JSON string below
json = "{}"
# create an instance of Distribution from a JSON string
distribution_instance = Distribution.from_json(json)
# print the JSON string representation of the object
print(Distribution.to_json())

# convert the object into a dict
distribution_dict = distribution_instance.to_dict()
# create an instance of Distribution from a dict
distribution_from_dict = Distribution.from_dict(distribution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


