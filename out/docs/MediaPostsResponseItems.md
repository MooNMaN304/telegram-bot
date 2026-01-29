# MediaPostsResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**image_url** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**published_at** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.media_posts_response_items import MediaPostsResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of MediaPostsResponseItems from a JSON string
media_posts_response_items_instance = MediaPostsResponseItems.from_json(json)
# print the JSON string representation of the object
print(MediaPostsResponseItems.to_json())

# convert the object into a dict
media_posts_response_items_dict = media_posts_response_items_instance.to_dict()
# create an instance of MediaPostsResponseItems from a dict
media_posts_response_items_from_dict = MediaPostsResponseItems.from_dict(media_posts_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


