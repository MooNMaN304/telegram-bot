# VideoResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**site** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.video_response_items import VideoResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of VideoResponseItems from a JSON string
video_response_items_instance = VideoResponseItems.from_json(json)
# print the JSON string representation of the object
print(VideoResponseItems.to_json())

# convert the object into a dict
video_response_items_dict = video_response_items_instance.to_dict()
# create an instance of VideoResponseItems from a dict
video_response_items_from_dict = VideoResponseItems.from_dict(video_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


