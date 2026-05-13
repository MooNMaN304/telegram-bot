# FiltersResponseCountries


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**country** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.filters_response_countries import FiltersResponseCountries

# TODO update the JSON string below
json = "{}"
# create an instance of FiltersResponseCountries from a JSON string
filters_response_countries_instance = FiltersResponseCountries.from_json(json)
# print the JSON string representation of the object
print(FiltersResponseCountries.to_json())

# convert the object into a dict
filters_response_countries_dict = filters_response_countries_instance.to_dict()
# create an instance of FiltersResponseCountries from a dict
filters_response_countries_from_dict = FiltersResponseCountries.from_dict(filters_response_countries_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


