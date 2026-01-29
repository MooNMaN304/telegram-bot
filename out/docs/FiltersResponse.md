# FiltersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**genres** | [**List[FiltersResponseGenres]**](FiltersResponseGenres.md) |  | 
**countries** | [**List[FiltersResponseCountries]**](FiltersResponseCountries.md) |  | 

## Example

```python
from openapi_client.models.filters_response import FiltersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FiltersResponse from a JSON string
filters_response_instance = FiltersResponse.from_json(json)
# print the JSON string representation of the object
print(FiltersResponse.to_json())

# convert the object into a dict
filters_response_dict = filters_response_instance.to_dict()
# create an instance of FiltersResponse from a dict
filters_response_from_dict = FiltersResponse.from_dict(filters_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


