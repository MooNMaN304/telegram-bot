# KinopoiskUserVoteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**total_pages** | **int** |  | 
**items** | [**List[KinopoiskUserVoteResponseItems]**](KinopoiskUserVoteResponseItems.md) |  | 

## Example

```python
from openapi_client.models.kinopoisk_user_vote_response import KinopoiskUserVoteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of KinopoiskUserVoteResponse from a JSON string
kinopoisk_user_vote_response_instance = KinopoiskUserVoteResponse.from_json(json)
# print the JSON string representation of the object
print(KinopoiskUserVoteResponse.to_json())

# convert the object into a dict
kinopoisk_user_vote_response_dict = kinopoisk_user_vote_response_instance.to_dict()
# create an instance of KinopoiskUserVoteResponse from a dict
kinopoisk_user_vote_response_from_dict = KinopoiskUserVoteResponse.from_dict(kinopoisk_user_vote_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


