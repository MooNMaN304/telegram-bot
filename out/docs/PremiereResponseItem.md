# PremiereResponseItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**year** | **int** |  | 
**poster_url** | **str** |  | 
**poster_url_preview** | **str** |  | 
**countries** | [**List[Country]**](Country.md) |  | 
**genres** | [**List[Genre]**](Genre.md) |  | 
**duration** | **int** |  | 
**premiere_ru** | **str** |  | 

## Example

```python
from openapi_client.models.premiere_response_item import PremiereResponseItem

# TODO update the JSON string below
json = "{}"
# create an instance of PremiereResponseItem from a JSON string
premiere_response_item_instance = PremiereResponseItem.from_json(json)
# print the JSON string representation of the object
print(PremiereResponseItem.to_json())

# convert the object into a dict
premiere_response_item_dict = premiere_response_item_instance.to_dict()
# create an instance of PremiereResponseItem from a dict
premiere_response_item_from_dict = PremiereResponseItem.from_dict(premiere_response_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


