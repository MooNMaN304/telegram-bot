# FilmSequelsAndPrequelsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**film_id** | **int** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**name_original** | **str** |  | 
**poster_url** | **str** |  | 
**poster_url_preview** | **str** |  | 
**relation_type** | **str** |  | 

## Example

```python
from openapi_client.models.film_sequels_and_prequels_response import FilmSequelsAndPrequelsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FilmSequelsAndPrequelsResponse from a JSON string
film_sequels_and_prequels_response_instance = FilmSequelsAndPrequelsResponse.from_json(json)
# print the JSON string representation of the object
print(FilmSequelsAndPrequelsResponse.to_json())

# convert the object into a dict
film_sequels_and_prequels_response_dict = film_sequels_and_prequels_response_instance.to_dict()
# create an instance of FilmSequelsAndPrequelsResponse from a dict
film_sequels_and_prequels_response_from_dict = FilmSequelsAndPrequelsResponse.from_dict(film_sequels_and_prequels_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


