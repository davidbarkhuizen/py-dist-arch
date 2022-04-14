# sudo su - postgres

clear

createdb xapo_write_test_local
psql xapo_write_test_local -f write_model/001_base.sql
psql xapo_write_test_local -f write_model/002_base_seed_data.sql
psql xapo_write_test_local -f write_model/003_test_seed_data.sql
dropdb xapo_write_test_local