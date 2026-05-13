# FilmCollectionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**total_pages** | **int** |  | 
**items** | [**List[FilmCollectionResponseItems]**](FilmCollectionResponseItems.md) |  | 

## Example

```python
from openapi_client.models.film_collection_response import FilmCollectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FilmCollectionResponse from a JSON string
film_collection_response_instance = FilmCollectionResponse.from_json(json)
# print the JSON string representation of the object
print(FilmCollectionResponse.to_json())

# convert the object into a dict
film_collection_response_dict = film_collection_response_instance.to_dict()
# create an instance of FilmCollectionResponse from a dict
film_collection_response_from_dict = FilmCollectionResponse.from_dict(film_collection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


