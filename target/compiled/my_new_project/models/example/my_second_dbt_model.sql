-- Use the `ref` function to select from other models

select *
from `dtc-de-course-447820`.`trips_data_all`.`my_first_dbt_model`
where id = 1