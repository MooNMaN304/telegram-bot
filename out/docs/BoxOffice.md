# BoxOffice


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**amount** | **int** |  | 
**currency_code** | **str** |  | 
**name** | **str** |  | 
**symbol** | **str** |  | 

## Example

```python
from openapi_client.models.box_office import BoxOffice

# TODO update the JSON string below
json = "{}"
# create an instance of BoxOffice from a JSON string
box_office_instance = BoxOffice.from_json(json)
# print the JSON string representation of the object
print(BoxOffice.to_json())

# convert the object into a dict
box_office_dict = box_office_instance.to_dict()
# create an instance of BoxOffice from a dict
box_office_from_dict = BoxOffice.from_dict(box_office_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


