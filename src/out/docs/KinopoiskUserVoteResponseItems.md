# KinopoiskUserVoteResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**name_ru** | **str** |  | [optional] 
**name_en** | **str** |  | [optional] 
**name_original** | **str** |  | [optional] 
**countries** | [**List[Country]**](Country.md) |  | [optional] 
**genres** | [**List[Genre]**](Genre.md) |  | [optional] 
**rating_kinopoisk** | **float** |  | [optional] 
**rating_imbd** | **float** |  | [optional] 
**year** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**poster_url** | **str** |  | [optional] 
**poster_url_preview** | **str** |  | [optional] 
**user_rating** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.kinopoisk_user_vote_response_items import KinopoiskUserVoteResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of KinopoiskUserVoteResponseItems from a JSON string
kinopoisk_user_vote_response_items_instance = KinopoiskUserVoteResponseItems.from_json(json)
# print the JSON string representation of the object
print(KinopoiskUserVoteResponseItems.to_json())

# convert the object into a dict
kinopoisk_user_vote_response_items_dict = kinopoisk_user_vote_response_items_instance.to_dict()
# create an instance of KinopoiskUserVoteResponseItems from a dict
kinopoisk_user_vote_response_items_from_dict = KinopoiskUserVoteResponseItems.from_dict(kinopoisk_user_vote_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


