# AwardPerson


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | 
**web_url** | **str** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**sex** | **str** |  | 
**poster_url** | **str** |  | 
**growth** | **int** |  | 
**birthday** | **str** |  | 
**death** | **str** |  | 
**age** | **int** |  | 
**birthplace** | **str** |  | 
**deathplace** | **str** |  | 
**profession** | **str** |  | 

## Example

```python
from openapi_client.models.award_person import AwardPerson

# TODO update the JSON string below
json = "{}"
# create an instance of AwardPerson from a JSON string
award_person_instance = AwardPerson.from_json(json)
# print the JSON string representation of the object
print(AwardPerson.to_json())

# convert the object into a dict
award_person_dict = award_person_instance.to_dict()
# create an instance of AwardPerson from a dict
award_person_from_dict = AwardPerson.from_dict(award_person_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


