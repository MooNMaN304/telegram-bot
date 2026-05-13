# ReviewResponseItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | [optional] 
**type** | **str** |  | [optional] 
**var_date** | **str** |  | [optional] 
**positive_rating** | **int** |  | [optional] 
**negative_rating** | **int** |  | [optional] 
**author** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.review_response_items import ReviewResponseItems

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewResponseItems from a JSON string
review_response_items_instance = ReviewResponseItems.from_json(json)
# print the JSON string representation of the object
print(ReviewResponseItems.to_json())

# convert the object into a dict
review_response_items_dict = review_response_items_instance.to_dict()
# create an instance of ReviewResponseItems from a dict
review_response_items_from_dict = ReviewResponseItems.from_dict(review_response_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


