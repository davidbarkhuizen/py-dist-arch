# sudo su - postgres

clear

createdb pydist_write_test_local
psql pydist_write_test_local -f write_model/latest_base.sql
psql pydist_write_test_local -f write_model/002_base_seed_data.sql
psql pydist_write_test_local -f write_model/003_test_seed_data.sql
dropdb pydist_write_test_local