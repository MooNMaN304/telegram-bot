# RelatedFilmResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[RelatedFilmResponseItems]**](RelatedFilmResponseItems.md) |  | 

## Example

```python
from openapi_client.models.related_film_response import RelatedFilmResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedFilmResponse from a JSON string
related_film_response_instance = RelatedFilmResponse.from_json(json)
# print the JSON string representation of the object
print(RelatedFilmResponse.to_json())

# convert the object into a dict
related_film_response_dict = related_film_response_instance.to_dict()
# create an instance of RelatedFilmResponse from a dict
related_film_response_from_dict = RelatedFilmResponse.from_dict(related_film_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


