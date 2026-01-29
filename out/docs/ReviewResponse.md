# ReviewResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Суммарное кол-во пользовательских рецензий | 
**total_pages** | **int** |  | 
**total_positive_reviews** | **int** |  | 
**total_negative_reviews** | **int** |  | 
**total_neutral_reviews** | **int** |  | 
**items** | [**List[ReviewResponseItems]**](ReviewResponseItems.md) |  | 

## Example

```python
from openapi_client.models.review_response import ReviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewResponse from a JSON string
review_response_instance = ReviewResponse.from_json(json)
# print the JSON string representation of the object
print(ReviewResponse.to_json())

# convert the object into a dict
review_response_dict = review_response_instance.to_dict()
# create an instance of ReviewResponse from a dict
review_response_from_dict = ReviewResponse.from_dict(review_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


