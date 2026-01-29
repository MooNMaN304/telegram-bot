# DigitalReleaseResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** |  | 
**total** | **int** |  | 
**releases** | [**List[DigitalReleaseItem]**](DigitalReleaseItem.md) |  | 

## Example

```python
from openapi_client.models.digital_release_response import DigitalReleaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DigitalReleaseResponse from a JSON string
digital_release_response_instance = DigitalReleaseResponse.from_json(json)
# print the JSON string representation of the object
print(DigitalReleaseResponse.to_json())

# convert the object into a dict
digital_release_response_dict = digital_release_response_instance.to_dict()
# create an instance of DigitalReleaseResponse from a dict
digital_release_response_from_dict = DigitalReleaseResponse.from_dict(digital_release_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


