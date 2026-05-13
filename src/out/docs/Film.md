# Film


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kinopoisk_id** | **int** |  | 
**kinopoisk_hdid** | **str** |  | 
**imdb_id** | **str** |  | 
**name_ru** | **str** |  | 
**name_en** | **str** |  | 
**name_original** | **str** |  | 
**poster_url** | **str** |  | 
**poster_url_preview** | **str** |  | 
**cover_url** | **str** |  | 
**logo_url** | **str** |  | 
**reviews_count** | **int** |  | 
**rating_good_review** | **float** |  | 
**rating_good_review_vote_count** | **int** |  | 
**rating_kinopoisk** | **float** |  | 
**rating_kinopoisk_vote_count** | **int** |  | 
**rating_imdb** | **float** |  | 
**rating_imdb_vote_count** | **int** |  | 
**rating_film_critics** | **float** |  | 
**rating_film_critics_vote_count** | **int** |  | 
**rating_await** | **float** |  | 
**rating_await_count** | **int** |  | 
**rating_rf_critics** | **float** |  | 
**rating_rf_critics_vote_count** | **int** |  | 
**web_url** | **str** |  | 
**year** | **int** |  | 
**film_length** | **int** |  | 
**slogan** | **str** |  | 
**description** | **str** |  | 
**short_description** | **str** |  | 
**editor_annotation** | **str** |  | 
**is_tickets_available** | **bool** |  | 
**production_status** | **str** |  | 
**type** | **str** |  | 
**rating_mpaa** | **str** |  | 
**rating_age_limits** | **str** |  | 
**has_imax** | **bool** |  | 
**has3_d** | **bool** |  | 
**last_sync** | **str** |  | 
**countries** | [**List[Country]**](Country.md) |  | 
**genres** | [**List[Genre]**](Genre.md) |  | 
**start_year** | **int** |  | 
**end_year** | **int** |  | 
**serial** | **bool** |  | [optional] 
**short_film** | **bool** |  | [optional] 
**completed** | **bool** |  | [optional] 

## Example

```python
from openapi_client.models.film import Film

# TODO update the JSON string below
json = "{}"
# create an instance of Film from a JSON string
film_instance = Film.from_json(json)
# print the JSON string representation of the object
print(Film.to_json())

# convert the object into a dict
film_dict = film_instance.to_dict()
# create an instance of Film from a dict
film_from_dict = Film.from_dict(film_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


