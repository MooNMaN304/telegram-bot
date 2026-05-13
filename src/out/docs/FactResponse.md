# FactResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**items** | [**List[Fact]**](Fact.md) |  | 

## Example

```python
from openapi_client.models.fact_response import FactResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FactResponse from a JSON string
fact_response_instance = FactResponse.from_json(json)
# print the JSON string representation of the object
print(FactResponse.to_json())

# convert the object into a dict
fact_response_dict = fact_response_instance.to_dict()
# create an instance of FactResponse from a dict
fact_response_from_dict = FactResponse.from_dict(fact_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


