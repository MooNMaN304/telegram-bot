# MediaPostsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**total_pages** | **int** |  | 
**items** | [**List[MediaPostsResponseItems]**](MediaPostsResponseItems.md) |  | 

## Example

```python
from openapi_client.models.media_posts_response import MediaPostsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MediaPostsResponse from a JSON string
media_posts_response_instance = MediaPostsResponse.from_json(json)
# print the JSON string representation of the object
print(MediaPostsResponse.to_json())

# convert the object into a dict
media_posts_response_dict = media_posts_response_instance.to_dict()
# create an instance of MediaPostsResponse from a dict
media_posts_response_from_dict = MediaPostsResponse.from_dict(media_posts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


