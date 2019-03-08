run tests by going into parent directory:
/project-guppi/
and running:
python3 -m unittest discover -v
or for just one module:
python3 -m unittest test.test_module
or for just one method:
python3 -m unittest test.test_module.TestClass.test_method