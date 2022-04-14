the last statemnt in a sql migration must NOT terminate in a semi-colon
otherwise the python yoyo-migration implementation ends up adding an extra null statement at the end
which causes the migration to fail